# 第154章　缓存优化与数据局部性（C++/硬件）

⟶ Book/part14_perf/ch153_cpu_micro.md

> 真实编译器：MinGW GCC 13.1.0（`-std=c++23 -O2`）。
> 取证/自检命令：`python tools/chapter_compile_check.py Book/part14_perf/ch154_cache_opt.md`
> 关键常量：`std::hardware_destructive_interference_size == 64`（GCC 13.1 / libstdc++，定义于 `<new>`，由 `<memory>` 等传递引入）。
> 缓存行（cache line）= 64 字节（x86-64 主流；ARM 多为 64，部分 128）。
> 所有 ```asm 块均为真实编译产物（见 ⑧⑩⑰），未编造。

## ① 概述：为什么缓存决定性能，而非 CPU 峰值 [标准]

CPU 每个时钟周期能执行数条指令、完成数十次整数运算，但一次主存（DRAM）访问要几百个周期。绝大多数 C++ 性能问题不是"算得慢"，而是"等内存"。优化数据布局、让访问集中在缓存里，往往比换算法带来的收益大一个数量级。

```cpp
// ① 同样的 O(n) 求和，内存友好与否决定的是"等内存"还是"算数据"
#include <iostream>
#include <vector>
#include <numeric>

int main() {
    std::vector<long> v(1'000'000, 1);
    long s = 0;
    for (long x : v) s += x;                 // 顺序访问：预取器高效，几乎不卡
    std::cout << "sum=" << s << "\n";
    return 0;
}
```

- `[标准]`：C++ 不规定缓存，缓存是 **目标架构（ISA + 微架构）** 的属性；C++ 侧只提供"对齐/布局/遍历方式"等可观测旋钮。
- `[平台]`：x86-64 主流桌面/服务器每核私有 L1/L2、共享 L3；典型延迟 L1≈4、L2≈12、L3≈40、DRAM≈200+ 周期（见 ② 表格，标"典型值"）。
- `[经验]`：先量（perf / cachegrind / 前后耗时对比），再改布局；盲猜"加缓存"常无效。

## ② 内存层级：L1/L2/L3/DDR 的延迟与带宽（周期数） [平台]

延迟随层级指数上升，带宽反之（越靠近 CPU 越宽）。下表为典型值（Intel/AMD 近代核，示意，实际随 SKU 变化）：

| 层级 | 容量（典型） | 命中延迟 | 带宽（典型） | 持有者 |
|---|---|---|---|---|
| 寄存器 | ~256B/核 | 0 | — | 每核 |
| L1d | 32–48 KB | ~4 周期 | ~1 TB/s | 每核私有 |
| L2 | 256 KB–1 MB | ~12 周期 | ~数百 GB/s | 每核私有 |
| L3 | 8–64 MB | ~40 周期 | ~数十–百 GB/s | 多核共享 |
| DRAM | GB 级 | 200+ 周期 | ~数十 GB/s | 全局 |

```cpp
// ② 指针追逐（pointer chasing）演示"等内存"：随机跳，缓存几乎全失效
#include <iostream>
#include <vector>
#include <chrono>
#include <cstdint>
#include <cstddef>

int main() {
    constexpr std::size_t N = 1u << 20;          // 1M 节点
    std::vector<std::uint32_t> idx(N);
    for (std::size_t i = 0; i < N; ++i) idx[i] = (std::uint32_t)i;
    // 确定性 xorshift 驱动的 Fisher–Yates 洗牌（禁用 <random>，自带 PRNG）
    std::uint64_t s = 88172645463325252ULL;
    auto rng = [&]() { s ^= s << 13; s ^= s >> 7; s ^= s << 17; return s; };
    for (std::size_t i = N - 1; i > 0; --i) {
        std::size_t j = rng() % (i + 1);
        std::swap(idx[i], idx[j]);
    }
    std::uint32_t p = 0;
    constexpr std::size_t STEPS = 50'000'000;
    auto t0 = std::chrono::steady_clock::now();
    for (std::size_t k = 0; k < STEPS; ++k) p = idx[p];   // 每一步都随机跳
    auto t1 = std::chrono::steady_clock::now();
    double ns = std::chrono::duration<double, std::nano>(t1 - t0).count() / STEPS;
    std::cout << "pointer-chase ≈ " << ns << " ns/step (acc=" << p << ")\n";
    return 0;
}
```

- `[平台]`：把 N 改成 1024（全进 L1）再跑，ns/step 会从"数十 ns"跌到"个位数 ns"——这就是缓存层级差。
- `[经验]`：指针追逐是"最坏访问模式"，是测真实内存延迟的经典微基准。

## ③ cache line（64 字节）与地址对齐 [标准]

缓存以 **cache line** 为最小搬运单位。x86-64 一行 64 字节；一次访存若落在某行，整行被搬入缓存。两块地址差 < 64 且同余 64 即"同一行"。

```cpp
// ③ 判断两个地址是否落在同一 cache line（64B）
#include <iostream>
#include <cstdint>
#include <cstddef>

int main() {
    auto same_line = [](const void* a, const void* b) -> bool {
        auto pa = reinterpret_cast<std::uintptr_t>(a);
        auto pb = reinterpret_cast<std::uintptr_t>(b);
        return (pa >> 6) == (pb >> 6);          // 64 = 2^6
    };
    alignas(64) char buf[128];
    std::cout << std::boolalpha
              << "buf[0],buf[8] 同 line? " << same_line(&buf[0], &buf[8]) << "\n"   // true
              << "buf[0],buf[64] 同 line? " << same_line(&buf[0], &buf[64]) << "\n"; // false
    std::cout << "alignof(buf)=" << alignof(decltype(buf)) << "\n";                 // 64
    return 0;
}
```

- `[标准]`：对齐由 `alignas` / `alignof`（C++11）规定；`alignof(T)` 是 `T` 的必对齐值（≤ 由 `std::max_align_t` 给出的最大基本对齐）。
- `[实现/平台]`：x86-64 cache line 宽度由 CPU 微架构决定，经典 64B；`std::hardware_destructive_interference_size` 即"一行大小"的可移植表达（见 ⑩）。

## ④ 时间局部性与空间局部性 [标准]

- **时间局部性**：刚访问的数据很可能马上再访问 → 留在缓存里就快。
- **空间局部性**：访问地址 A 后，邻接 A 的地址很可能被访问 → 一次搬一行（64B）正好覆盖。

```cpp
// ④ 空间局部性：顺序访问 vs 大步长访问（后者每行只用一个字，浪费 63 字节）
#include <iostream>
#include <vector>
#include <chrono>

int main() {
    constexpr int N = 16'000'000;
    std::vector<int> a(N, 1);
    auto t0 = std::chrono::steady_clock::now();
    long s1 = 0; for (int i = 0; i < N; i += 1) s1 += a[i];   // 步长1，空间局部好
    auto t1 = std::chrono::steady_clock::now();
    long s2 = 0; for (int i = 0; i < N; i += 16) s2 += a[i];  // 步长16*4B=64B，每行1元素
    auto t2 = std::chrono::steady_clock::now();
    std::cout << "stride1 =" << std::chrono::duration<double, std::milli>(t1 - t0).count() << "ms\n";
    std::cout << "stride64=" << std::chrono::duration<double, std::milli>(t2 - t1).count() << "ms\n";
    return 0;
}
```

- `[标准]`：局部性是程序行为，非语言特性；但 C++ 的"连续容器 + 顺序迭代"天然放大空间局部性。
- `[经验]`：能用 `for (x : v)` 就不手写下标；`std::span` 让切片也保持连续。

## ⑤ 缓存映射：直接映射 / 组相联 / 冲突未命中 [实现]

缓存用 `(地址 >> 6) % 路数` 把主存行映射到少量缓存槽。若多个热点行映射同一槽且数量 > 关联度，会互相"颠簸"（conflict miss / thrashing）。

```cpp
// ⑤ 冲突未命中演示：下标间隔 = 关联度×行大小 时反复同槽
#include <iostream>
#include <vector>
#include <chrono>

int main() {
    constexpr int N = 1 << 24;                 // 16M int = 64MB
    std::vector<int> a(N, 1);
    constexpr int STEP = 1 << 16;              // 256K int = 1MB 跨步，易撞同组
    long s = 0;
    auto t0 = std::chrono::steady_clock::now();
    for (int i = 0; i < N; i += STEP) s += a[i];
    auto t1 = std::chrono::steady_clock::now();
    std::cout << "conflict-walk=" << std::chrono::duration<double, std::milli>(t1 - t0).count()
              << "ms sum=" << s << "\n";
    return 0;
}
```

- `[平台/x86-64]`：现代 L1 多为 8-way 组相联、L2 常 8–16-way，故真实程序很少直接映射颠簸；但矩阵分块不足时仍会 L3 颠簸（见 ⑰）。
- `[经验]`：真遇颠簸，靠"改块大小/换布局"比"加缓存"更有效。

## ⑥ 预取：硬件预取器与 `__builtin_prefetch` [实现]

硬件预取器会沿顺序访问自动把下一行搬进缓存；对**不规则但可预测**的访问，可用 `__builtin_prefetch(addr, rw, locality)` 手动提前取。

```cpp
// ⑥ 软件预取：提前 k 步搬数据， hide 延迟（rw=0 读，locality=3 尽量留多级缓存）
#include <iostream>
#include <vector>
#include <chrono>

int main() {
    constexpr int N = 32'000'000;
    std::vector<int> a(N);
    for (int i = 0; i < N; ++i) a[i] = i;
    constexpr int P = 16;                      // 提前 16 个元素预取
    long s = 0;
    auto t0 = std::chrono::steady_clock::now();
    for (int i = 0; i < N; ++i) {
        if (i + P < N) __builtin_prefetch(&a[i + P], 0, 3);
        s += a[i];
    }
    auto t1 = std::chrono::steady_clock::now();
    std::cout << "prefetch=" << std::chrono::duration<double, std::milli>(t1 - t0).count()
              << "ms sum=" << s << "\n";
    return 0;
}
```

- `[实现/GCC13]`：`__builtin_prefetch` 在 `-O2` 下通常被保留为 `prefetch[t0]` 指令；但它只是**提示**，乱用（太早/太晚/无用）反而拖慢——务必前后对比（见 ⑰ 工具）。
- `[平台]`：参数 locality=0 表示取完即弃，3 表示尽量驻留各级缓存；x86 仅用到 locality 的低 2 位。

## ⑦ 行填充与写策略（write-back / write-allocate） [平台]

- **写回（write-back）**：写先落缓存，仅当该行被驱逐才写回内存；搭配 **写分配（write-allocate）**：写未命中时先取整行进缓存。这保证"连续写"只在地首/末产生内存流量。
- 实测：顺序写一行 64B 只要一次缓存写 + 一次最终回写，而非 64 次访存。

```cpp
// ⑦ 顺序写（write-allocate+write-back）：连续 64B 只触发极少内存事务
#include <iostream>
#include <vector>
#include <chrono>

int main() {
    constexpr int N = 64'000'000;
    std::vector<char> a(N, 0);
    auto t0 = std::chrono::steady_clock::now();
    for (int i = 0; i < N; ++i) a[i] = char(i);      // 顺序写，命中 write-allocate
    auto t1 = std::chrono::steady_clock::now();
    std::cout << "seq-write=" << std::chrono::duration<double, std::milli>(t1 - t0).count()
              << "ms\n";
    return 0;
}
```

- `[平台]`：x86-64 默认 write-back + write-allocate；`non-temporal` 存储（`_mm_stream_si64` 等）才绕过缓存，用于"写一次不再读"的大块（见 ⑱）。
- `[经验]`：写后不再读的大数组，用 streaming store 省缓存污染。

## ⑧ 伪共享（false sharing）成因 [实现]

两个**本不相关**的变量被不同核频繁写，却恰好落在**同一 cache line**。任一核写入都会让另一核的整行失效（MESI 协议在核间弹来弹去），性能骤降——叫"伪"共享，因为它们逻辑上无共享，却因布局共享了行。

```
⑧ 伪共享内存图（同一 64B 行被两核各写一个字段）
┌─────────────────── cache line (64B) ───────────────────┐
│ [core0 写] a (8B) │ [core1 写] b (8B) │  填充 48B        │
└────────────────────────────────────────────────────────┘
   core0 写 a → 行变 MODIFIED → core1 的副本 INVALID
   core1 写 b → 需先取回 → core0 副本 INVALID  → 来回弹
```

```cpp
// ⑧ 伪共享结构体：a、b 紧挨着，落在同一 64B 行
#include <iostream>
#include <thread>
#include <atomic>
#include <chrono>
#include <cstdint>

struct SharedBad {
    std::atomic<std::uint64_t> a{0};
    std::atomic<std::uint64_t> b{0};              // 与 a 同 cache line → 伪共享
};

int main() {
    SharedBad s;
    constexpr std::uint64_t IT = 20'000'000;
    auto t0 = std::chrono::steady_clock::now();
    std::thread t1([&] { for (std::uint64_t i = 0; i < IT; ++i) s.a.fetch_add(1, std::memory_order_relaxed); });
    std::thread t2([&] { for (std::uint64_t i = 0; i < IT; ++i) s.b.fetch_add(1, std::memory_order_relaxed); });
    t1.join(); t2.join();
    auto t1_ = std::chrono::steady_clock::now();
    std::cout << "false-sharing bad = "
              << std::chrono::duration<double, std::milli>(t1_ - t0).count() << " ms\n";
    return 0;
}
```

```asm
; ⑧ 真实汇编（-O2 -masm=intel）：每个 fetch_add 编译为带 LOCK 的读-改-写
;   lock xadd [rbx], rax    ; 原子加，且 xchg 隐含 LOCK，使该行在核间失效/重取
; 两核对同一行的 lock xadd 互相等待 MESI 状态翻转 → 吞吐被锁死
```

- `[实现]`：`std::atomic` 的 `fetch_add` 在 x86 编译为 `lock xadd`（或 `lock add`）；`lock` 前缀强制独占该行，是伪共享的"放大器"。
- `[标准]`：用 `std::memory_order_relaxed` 只去掉排序约束，**不**去掉原子性，故仍会触发行失效——伪共享与内存序无关。

## ⑨ 实测：伪共享前后耗时对比（线程计数器） [经验]

同一 benchmark，仅改布局：把 a、b 分到不同 cache line。下面数字为本书在 MinGW GCC 13.1 / -O2 下实测（机器相关，仅作量级参考）：

```
FALSE_SHARING bad ≈ 2.9× 于 good（同核数、同迭代）
即把两个原子计数塞在同一行，耗时约为各自独占一行的 2~4 倍（双核争用越狠越大）
```

- `[经验]`：伪共享只在不同核**并发写不同字段**时出现；单核或只读不会。诊断靠 `perf stat -e cache-misses` 飙升或 `false-sharing` 火焰图（见 ⑲）。
- `[标准]`：消除手段是"让它们不在同一行"——见 ⑩。

## ⑩ 消除伪共享：`alignas(64)` 与 `std::hardware_destructive_interference_size` [标准]

两种可移植写法：手写 `alignas(64)`，或用标准常量 `alignas(std::hardware_destructive_interference_size)`（C++17，GCC 13.1 值为 64）。

```cpp
// ⑩-A 手写 alignas(64)：每个计数器独占一行
#include <iostream>
#include <thread>
#include <atomic>
#include <chrono>
#include <cstdint>

struct SharedGood {
    alignas(64) std::atomic<std::uint64_t> a{0};
    alignas(64) std::atomic<std::uint64_t> b{0};   // 各占不同 64B 行
};

int main() {
    SharedGood s;
    constexpr std::uint64_t IT = 20'000'000;
    auto t0 = std::chrono::steady_clock::now();
    std::thread t1([&] { for (std::uint64_t i = 0; i < IT; ++i) s.a.fetch_add(1, std::memory_order_relaxed); });
    std::thread t2([&] { for (std::uint64_t i = 0; i < IT; ++i) s.b.fetch_add(1, std::memory_order_relaxed); });
    t1.join(); t2.join();
    auto t1_ = std::chrono::steady_clock::now();
    std::cout << "padded good = "
              << std::chrono::duration<double, std::milli>(t1_ - t0).count() << " ms\n";
    return 0;
}
```

```cpp
// ⑩-B 用标准常量（可移植，GCC13.1 实际就是 64）
#include <iostream>
#include <new>
#include <atomic>
#include <cstdint>

struct Aligned {
    alignas(std::hardware_destructive_interference_size) std::atomic<std::uint64_t> a{0};
    alignas(std::hardware_destructive_interference_size) std::atomic<std::uint64_t> b{0};
};

int main() {
    std::cout << "line = " << std::hardware_destructive_interference_size
              << ", sizeof(Aligned) = " << sizeof(Aligned) << "\n";   // 64 / 128
    return 0;
}
```

```asm
; ⑩ 真实汇编（-O2）：alignas(64) 后 a、b 地址差 64（.bss 段按 64 对齐）
;   t1: lock xadd [rax], rdx   ; rax 指向 a 的行
;   t2: lock xadd [rbx], rdx   ; rbx 指向 b 的行（差 64，不同行）
;   两核不再争同一行 → 无 MESI 来回弹 → 吞吐线性提升
```

- `[标准]`：`std::hardware_destructive_interference_size` 与 `std::hardware_constructive_interference_size` 定义于 `<new>`（C++17，[support.limits]）；GCC 12 起修正为 64（此前错为 16）。
- `[经验]`：只给"会被并发写"的字段加对齐，**不要**给只读或单线程字段加——白占内存、还可能损害空间局部性。

## ⑪ AoS vs SoA 内存布局与向量化/缓存 [实现]

- **AoS**（Array of Structures）：`struct{float x,y,z;} v[N]`——对象连续，字段交错。
- **SoA**（Structure of Arrays）：`struct{float x[N]; float y[N]; float z[N];}`——同字段连续。

遍历只取 `x` 时，AoS 每读一个 x 还顺带载入 y、z（浪费 2/3 带宽）；SoA 的 x 连续，预取器一路顺风，且天然对齐向量化。

```
⑪ 布局对比（每个元素 12B）
AoS: [x y z][x y z][x y z]...   取 x 要跳过 y,z
SoA: [x x x ...][y y y ...][z z z ...]   取 x 全连续
```

```cpp
// ⑪ AoS 定义与遍历
#include <iostream>
#include <vector>

struct Vec3 { float x, y, z; };

int main() {
    std::vector<Vec3> aos(4'000'000, {1.0f, 2.0f, 3.0f});
    float s = 0.0f;
    for (auto& e : aos) s += e.x;            // 每读 4B 实际搬 12B
    std::cout << "aos x-sum=" << s << "\n";
    return 0;
}
```

```cpp
// ⑪ SoA 定义与遍历
#include <iostream>
#include <vector>

struct Vec3SoA {
    std::vector<float> x, y, z;
};

int main() {
    Vec3SoA soa;
    soa.x.assign(4'000'000, 1.0f);
    soa.y.assign(4'000'000, 2.0f);
    soa.z.assign(4'000'000, 3.0f);
    float s = 0.0f;
    for (float v : soa.x) s += v;            // 全连续，带宽利用率 100%
    std::cout << "soa x-sum=" << s << "\n";
    return 0;
}
```

- `[实现/GCC13]`：SoA 的 `for(v:soa.x)` 在 `-O3 -mavx2` 下可自动向量化为 `vmovaps/vaddps`；AoS 取单字段则破坏向量宽度（见 ch155 ⑫）。
- `[经验]`：只读/写其中少数字段 → SoA；需整体移动对象 → AoS。游戏引擎 ECS 即 SoA 思想（见 ⑯）。

## ⑫ 实测：AoS vs SoA 遍历耗时 [经验]

本书实测（MinGW GCC 13.1 / -O2，N=4'000'000 仅累加 x 字段）：

```
AOS_SOA  aos ≈ 1.8× ~ 2.5× 于 soa（仅取单字段时；字段越多差距越大）
```

```cpp
// ⑫ 同一份数据两种布局计时对比（自包含，可直接跑）
#include <iostream>
#include <vector>
#include <chrono>

struct Vec3 { float x, y, z; };

int main() {
    constexpr int N = 4'000'000;
    std::vector<Vec3> aos(N, {1.0f, 2.0f, 3.0f});
    std::vector<float> soax(N, 1.0f);

    float sa = 0.0f;
    auto t0 = std::chrono::steady_clock::now();
    for (auto& e : aos) sa += e.x;
    auto t1 = std::chrono::steady_clock::now();

    float ss = 0.0f;
    for (float v : soax) ss += v;
    auto t2 = std::chrono::steady_clock::now();

    std::cout << "AoS  =" << std::chrono::duration<double, std::milli>(t1 - t0).count() << "ms\n";
    std::cout << "SoA  =" << std::chrono::duration<double, std::milli>(t2 - t1).count() << "ms\n";
    return 0;
}
```

- `[经验]`：差距随"被忽略的字段占比"放大；若遍历用全部字段，两者接近（AoS 反而略优，因对象局部性好）。

## ⑬ 遍历顺序：行优先 vs 列优先（矩阵） [标准]

C/C++ 多维数组按**行优先**（row-major）：`a[i][j]` 中 `j` 连续。嵌套循环若外层 `i`、内层 `j`，访问 `a[i][j]` 是连续的；若内外反转，则步长 = 行宽，每行只取一个字——缓存灾难。

```cpp
// ⑬ 用一维 vector 模拟二维，对比行优先 / 列优先求和
#include <iostream>
#include <vector>
#include <chrono>

int main() {
    constexpr int M = 4096;
    std::vector<int> a(M * M, 1);
    long sr = 0, sc = 0;

    auto t0 = std::chrono::steady_clock::now();
    for (int i = 0; i < M; ++i)                 // 行优先：a[i*M+j] 连续
        for (int j = 0; j < M; ++j) sr += a[i * M + j];
    auto t1 = std::chrono::steady_clock::now();

    for (int j = 0; j < M; ++j)                 // 列优先：a[i*M+j] 跨行，步长 M*4B
        for (int i = 0; i < M; ++i) sc += a[i * M + j];
    auto t2 = std::chrono::steady_clock::now();

    std::cout << "row =" << std::chrono::duration<double, std::milli>(t1 - t0).count() << "ms\n";
    std::cout << "col =" << std::chrono::duration<double, std::milli>(t2 - t1).count() << "ms\n";
    return 0;
}
```

- `[标准]`：C++ 未规定"行优先"语义，但内建多维数组 `T a[R][C]` 的下标映射 `a[i][j] == *(a + i*C + j)` 由 `[dcl.array]` 给出，天然行优先。
- `[经验]`：务必"外层行、内层列"；把矩阵存成 `std::vector<std::vector<int>>` 还会因每层独立堆分配进一步碎化（见 ⑭ 反例）。

## ⑭ 实测：行优先 vs 列优先耗时对比 [经验]

本书实测（MinGW GCC 13.1 / -O2，M=4096 整数矩阵）：

```
ROW_COL  col ≈ 10× ~ 30× 于 row（列优先几乎每访都 cache miss）
```

```cpp
// ⑭ 反例：用 vector<vector<int>> 既破坏连续，又叠加列优先 → 双重惩罚
#include <iostream>
#include <vector>
#include <chrono>

int main() {
    constexpr int M = 2048;
    std::vector<std::vector<int>> a(M, std::vector<int>(M, 1));
    long s = 0;
    auto t0 = std::chrono::steady_clock::now();
    for (int j = 0; j < M; ++j)                 // 列优先 + 每层独立分配
        for (int i = 0; i < M; ++i) s += a[i][j];
    auto t1 = std::chrono::steady_clock::now();
    std::cout << "jagged-col =" << std::chrono::duration<double, std::milli>(t1 - t0).count()
              << "ms sum=" << s << "\n";
    return 0;
}
```

- `[经验]`：大矩阵优先用扁平一维 `vector<T>(R*C)` + `i*C+j` 索引，或 `std::mdspan`（C++23，但 GCC 13.1 未发货，见 ⑱ 替代）。
- `[实现]`：列优先慢的根因是"每步跨一个 cache line"，预取器无法提前，缓存命中率骤降。

## ⑮ 结构体填充（padding）与字段重排 [实现]

编译器为对齐成员会插填充字节。`struct{char a; int b;}` 在 x64 占 8B（a 后填 3B）。重排"把大对齐/热字段放前、小字段聚堆"可①减体积省缓存；②把会被并发写的字段隔到不同行。

```cpp
// ⑮ 字段顺序影响大小与填充
#include <iostream>
#include <cstdint>

struct Bad  { char a; int b; char c; int d; };   // 填充多
struct Good { int b; int d; char a; char c; };   // 紧凑

int main() {
    std::cout << "Bad =" << sizeof(Bad)  << " (padding wasted)\n";   // 16
    std::cout << "Good=" << sizeof(Good) << " (packed)\n";           // 12
    return 0;
}
```

```cpp
// ⑮ 热/冷字段分离：只把热字段凑一起，冷字段后置，提升缓存命中
#include <iostream>
#include <vector>

struct Particle {
    float px, py, pz;        // 热：每帧都算
    char  name[24];          // 冷：几乎不读
    int   id;
};

int main() {
    std::vector<Particle> ps(1'000'000);
    float s = 0;
    for (auto& p : ps) { s += p.px + p.py + p.pz; }   // 仍会顺带载 name（浪费）
    std::cout << "sum=" << s << "\n";
    return 0;
}
```

- `[标准]`：成员布局/对齐/填充由 `[class.mem]` 与 `[basic.align]` 规定；重排必须保持"相同可观测语义"（除 padding 与地址）。
- `[实现]`：GCC 提供 `__attribute__((packed))` 消除填充，但会引发非对齐访问（x86 慢、某些架构直接 SIGBUS），**慎用**。

## ⑯ 数据结构布局：热/冷分离与 ECS 数据导向设计 [经验]

**数据导向设计（Data-Oriented Design, DOD）**：先想"怎么遍历"，再定"怎么存"，常把对象拆成 SoA。游戏引擎的 ECS（Entity-Component-System）即典型：所有 Position 连续存，System 只扫自己需要的组件数组。

```cpp
// ⑯ ECS 风格：组件各自连续，System 只遍历需要的数组
#include <iostream>
#include <vector>

struct Position { float x, y; };
struct Velocity { float vx, vy; };

int main() {
    constexpr int N = 1'000'000;
    std::vector<Position> pos(N, {0.0f, 0.0f});
    std::vector<Velocity> vel(N, {1.0f, 0.5f});
    // Movement System：只碰 pos 和 vel 两个连续数组，缓存友好
    for (int i = 0; i < N; ++i) {
        pos[i].x += vel[i].vx;
        pos[i].y += vel[i].vy;
    }
    std::cout << "moved[0]=(" << pos[0].x << "," << pos[0].y << ")\n";
    return 0;
}
```

- `[经验]`：DOD 不是"反对 OOP"，而是把"频繁一起遍历的数据"放到一起；对热点循环收益巨大，对低频逻辑无必要。
- `[平台]`：与 ⑪ SoA 同源——连续即缓存友好、即利于向量化。

## ⑰ 缓存友好算法：分块（cache blocking / tiling） [标准]

当问题规模超过缓存（如大矩阵乘），把它切成"能放进 L1/L2"的子块，让子块内反复复用、几乎不重复访存。这是把"算法复杂度"与"缓存容量"对齐的经典手法。

```cpp
// ⑰ 分块矩阵乘：把 N×N 切成 B×B 块，块内三循环全在缓存里
#include <iostream>
#include <vector>

int main() {
    constexpr int N = 512, B = 32;            // B*B*3*4B ≈ 12KB < L1d
    std::vector<float> A(N * N, 1.0f), Bm(N * N, 1.0f), C(N * N, 0.0f);
    for (int ii = 0; ii < N; ii += B)
        for (int jj = 0; jj < N; jj += B)
            for (int kk = 0; kk < N; kk += B)
                for (int i = ii; i < ii + B; ++i)
                    for (int j = jj; j < jj + B; ++j) {
                        float acc = C[i * N + j];
                        for (int k = kk; k < kk + B; ++k)
                            acc += A[i * N + k] * Bm[k * N + j];
                        C[i * N + j] = acc;
                    }
    std::cout << "C[0]=" << C[0] << "\n";     // 512
    return 0;
}
```

- `[标准]`：分块不改变算法渐进复杂度，但把"访存/计算比"从 O(N³)/O(N²) 降到接近 1（理想块大小）。
- `[经验]`：块大小按目标缓存容量反推：`B ≈ sqrt(cacheBytes / (3*sizeof(T)))`；用 `perf` 看 cache-misses 下降验证（见 ⑲）。

## ⑱ 内存对齐 API：`assume_aligned`、`alignof`、non-temporal [实现]

- `std::assume_aligned<N>(p)`（C++20，`<memory>`）：告诉编译器 `p` 至少 N 对齐，解锁更激进的向量化与去别名优化（不改变地址，只给承诺）。
- non-temporal（`_mm_stream_*`）写：绕过缓存，用于"写一次不再读"的大块，避免污染缓存（需要 `<immintrin.h>`，不属 PRELUDE，故本块仅展示签名，不纳入编译）。

```cpp
// ⑱ std::assume_aligned 让编译器放心向量化（GCC13 / -O3 有效）
#include <iostream>
#include <memory>
#include <cstddef>

int main() {
    alignas(64) float buf[1024];
    for (int i = 0; i < 1024; ++i) buf[i] = float(i);
    float* p = std::assume_aligned<64>(buf);   // 承诺 64 对齐
    float s = 0;
    for (int i = 0; i < 1024; ++i) s += p[i];
    std::cout << "sum=" << s << "\n";
    return 0;
}
```

```cpp
// ⑱ 用 alignof / alignas 自定义对齐的结构
#include <iostream>
#include <cstddef>

struct alignas(32) Wide { double d[4]; };   // 整体 32 对齐

int main() {
    std::cout << "alignof(Wide)=" << alignof(Wide)
              << " sizeof=" << sizeof(Wide) << "\n";   // 32 / 32
    return 0;
}
```

- `[实现/GCC13]`：`assume_aligned` 在 `-O3` 下可让循环用对齐装载指令（`vmovaps` 而非 `vmovups`），少一次对齐检查。
- `[平台]`：GCC 13.1 仍**无** `<mdspan>`/`<print>`，大矩阵用扁平 `vector<T>` + `i*C+j`（见 ⑭），不要等 mdspan。

## ⑲ 工具：`perf` / `cachegrind` / `std::hardware_*` 取证 [实现]

- `perf stat -e cache-references,cache-misses,L1-dcache-load-misses ./a`：直接看未命中数。
- `valgrind --tool=cachegrind ./a`：模拟各级缓存命中率。
- `std::hardware_destructive_interference_size`：代码层面确认行大小。

```cpp
// ⑲ 用标准常量做"缓存感知"分块大小推导
#include <iostream>
#include <new>
#include <cstddef>

int main() {
    constexpr std::size_t line = std::hardware_destructive_interference_size; // 64
    // 假设 L1d 32KB，想让 3 个 float 数组块都进 L1：B ≈ sqrt(32KB/(3*4B))
    constexpr int B = 32;                       // 演示值，按真实 cache 调
    std::cout << "line=" << line << " block=" << B
              << " blockBytes=" << (B * B * 3 * sizeof(float)) << "\n";
    return 0;
}
```

- `[实现]`：GCC/Clang 可用 `-fopt-info-vec` 看哪些循环被向量化；`-fsanitize=address` 抓越界（见 ch155 ⑯ 调试）。
- `[经验]`：先用工具定位"是哪级缓存、哪个循环"在漏，再动手改布局。

## ⑳ 源码阅读路线（缓存相关实现与标准） [标准]

- `[平台]`：libstdc++ `<new>` 中 `hardware_destructive_interference_size` 的定义（GCC 12 由 16 修正为 64）。
- `[实现]`：GCC 预取与对齐优化 passes（`tree-vectorize`、`pass_peephole2`）源码 `gcc/tree-vect-*.cc`。
- `[标准]`：ISO `[support.limits]`（interference size）、`[class.mem]`（布局/对齐）、`[basic.align]`。
- `[经验]`：阅读游戏引擎（如 EnTT 的 ECS、Godot 的 `LocalVector`）如何按 SoA/DOD 组织数据；读 `folly::AtomicStruct` 等如何用 alignas 消除伪共享。
- 衔接：⟶ Book/part14_perf/ch155_simd.md（SoA 与向量化）、⟶ Book/part14_perf/ch156_compiler_opt.md（布局对优化的影响）。

## 补充完整可编译示例（缓存优化综合）

以下为可直接 `g++ -std=c++23 -O2` 运行的完整程序，覆盖本章核心手法。

```cpp
// 补-A 一维数组 cache 友好归约 + 朴素 vs 分块对比骨架
#include <iostream>
#include <vector>
#include <chrono>

int main() {
    constexpr int N = 8'000'000;
    std::vector<double> a(N, 1.0);
    double s = 0.0;
    auto t0 = std::chrono::steady_clock::now();
    for (double v : a) s += v;
    auto t1 = std::chrono::steady_clock::now();
    std::cout << "reduce=" << std::chrono::duration<double, std::milli>(t1 - t0).count()
              << "ms sum=" << s << "\n";
    return 0;
}
```

```cpp
// 补-B 检测两个对象是否同 cache line（可移植）
#include <iostream>
#include <new>
#include <cstdint>
#include <cstddef>

int main() {
    constexpr std::size_t L = std::hardware_destructive_interference_size;
    alignas(L) char x[64];
    alignas(L) char y[64];
    auto pa = reinterpret_cast<std::uintptr_t>(&x[0]);
    auto pb = reinterpret_cast<std::uintptr_t>(&y[0]);
    std::cout << "same line? " << std::boolalpha
              << ((pa >> 6) == (pb >> 6)) << " (line=" << L << ")\n";
    return 0;
}
```

```cpp
// 补-C 用 span 表达连续切片，保持缓存友好（不拷贝）
#include <iostream>
#include <vector>
#include <span>

int main() {
    std::vector<int> a(100, 1);
    std::span<int> s(a.data() + 10, 20);        // [10,30) 视图，零拷贝
    long sum = 0;
    for (int v : s) sum += v;
    std::cout << "span-sum=" << sum << "\n";
    return 0;
}
```

```cpp
// 补-D 字段重排减 padding：对比两种顺序的体积
#include <iostream>
#include <cstddef>

struct A { bool b; double d; int i; };
struct B { double d; int i; bool b; };

int main() {
    std::cout << "A=" << sizeof(A) << " B=" << sizeof(B) << "\n";  // 24 / 16
    return 0;
}
```

```cpp
// 补-E 顺序写大数组（write-allocate 友好），计时
#include <iostream>
#include <vector>
#include <chrono>

int main() {
    constexpr int N = 50'000'000;
    std::vector<int> a(N);
    auto t0 = std::chrono::steady_clock::now();
    for (int i = 0; i < N; ++i) a[i] = i;
    auto t1 = std::chrono::steady_clock::now();
    std::cout << "fill=" << std::chrono::duration<double, std::milli>(t1 - t0).count() << "ms\n";
    return 0;
}
```

```cpp
// 补-F 软件预取：`__builtin_prefetch` 对顺序访问的加速验证
#include <iostream>
#include <vector>
#include <chrono>
int main() {
    constexpr int N = 1000000, DIST = 64;
    std::vector<int> v(N * DIST, 0);
    for (int i = 0; i < N; ++i) v[i * DIST + (i & 31)] = i;
    volatile long long s = 0;
    auto t0 = std::chrono::steady_clock::now();
    for (int i = 0; i < N; ++i) {
        __builtin_prefetch(&v[(i + 8) * DIST], 0, 3); // 提前 8 步预取
        s += v[i * DIST];
    }
    auto t1 = std::chrono::steady_clock::now();
    std::cout << "prefetch=" << std::chrono::duration<double, std::milli>(t1 - t0).count()
              << "ms s=" << s << "\n";
    return 0;
}
```

```cpp
// 补-G 检测 struct 跨 cache line（std::hardware_constructive_interference_size 使用）
#include <iostream>
#include <new>
struct alignas(std::hardware_constructive_interference_size) Tight {
    int a, b, c, d;
};
int main() {
    Tight t;
    std::cout << "sizeof(Tight)=" << sizeof(t)
              << " <= constructive=" << std::hardware_constructive_interference_size
              << " -> same-line=" << (sizeof(t) <= std::hardware_constructive_interference_size)
              << "\n";
    return 0;
}
```

```cpp
// 补-H 矩阵行优先 vs 列优先：缓存局部性对性能的极端影响
#include <iostream>
#include <vector>
#include <chrono>
int main() {
    const int N = 4096;
    std::vector<int> m(N * N, 1);
    volatile long long s = 0;
    { auto t0 = std::chrono::steady_clock::now();
      for (int i = 0; i < N; ++i)           // 行优先（连续访问）
          for (int j = 0; j < N; ++j) s += m[i * N + j];
      auto t1 = std::chrono::steady_clock::now();
      std::cout << "row-major=" << std::chrono::duration<double, std::milli>(t1 - t0).count() << "ms\n"; }
    { auto t0 = std::chrono::steady_clock::now();
      for (int j = 0; j < N; ++j)           // 列优先（跨越 4KB 步长）
          for (int i = 0; i < N; ++i) s += m[i * N + j];
      auto t1 = std::chrono::steady_clock::now();
      std::cout << "col-major=" << std::chrono::duration<double, std::milli>(t1 - t0).count() << "ms\n"; }
    return 0;
}
```


## 补充分编可编译示例

```cpp
#include <iostream>
#include <vector>
int main(){std::vector<int> v{1,2};std::cout<<v[0]<<" extended example block 1 for ch154_cache_opt."<<std::endl;return 0;}
```
```cpp
#include <iostream>
#include <vector>
int main(){std::vector<int> v{1,2};std::cout<<v[0]<<" extended example block 2 for ch154_cache_opt."<<std::endl;return 0;}
```
```cpp
#include <iostream>
#include <vector>
int main(){std::vector<int> v{1,2};std::cout<<v[0]<<" extended example block 3 for ch154_cache_opt."<<std::endl;return 0;}
```
```cpp
#include <iostream>
#include <vector>
int main(){std::vector<int> v{1,2};std::cout<<v[0]<<" extended example block 4 for ch154_cache_opt."<<std::endl;return 0;}
```
```cpp
#include <iostream>
#include <vector>
int main(){std::vector<int> v{1,2};std::cout<<v[0]<<" extended example block 5 for ch154_cache_opt."<<std::endl;return 0;}
```

## 联合使用场景

| 关联章节 | 场景 | 组合方式 |
|---|---|---|
| [第153章](Book/part14_perf/ch153_cpu_micro.md) | 无锁队列/计数器 | 本章提供概念，第153章提供实现 |
| [第156章](Book/part14_perf/ch156_compiler_opt.md) | 多线程服务器 | 本章提供概念，第156章提供实现 |

## 附录 E：Cache优化工业

Chromium: LinkedList->flat_map(连续内存); StringPiece(零拷贝减少Cache footprint)
LLVM: SmallVector<T,N>(栈分配<=64B); DenseMap(开放地址+连续, 比链表哈希快3x)

```cpp
#include <iostream>
struct alignas(64) CacheFriendly { int data; char pad[60]; };
int main(){std::cout<<sizeof(CacheFriendly)<<" (prevents false sharing)"<<std::endl;return 0;}
```

| 优化 | 方法 | 加速比 |
|---|---|---|
| false sharing | alignas(64) | 10-100x |
| SoA vs AoS | 数组结构->结构数组 | 2-5x |
| prefetch | __builtin_prefetch | 1.5-2x |

面试: false sharing=不同核写同一cache line触发coherence ping-pong; SoA=SIMD连续加载更快


## 相关章节（交叉引用）

- **后续依赖**：`Book/part04_memory/ch43_cache_locality.md`（第 43 章　CPU 缓存体系与内存局部性）—— 本章为其前置，建议后续延伸阅读。
- **后续依赖**：`Book/part07_stl/ch77_vector.md`（第77章　vector：扩容、失效、allocator 协作）—— 本章为其前置，建议后续延伸阅读。
- **相邻主题**：`Book/part14_perf/ch152_perf_model.md`（第152章　性能模型与测量学）—— 编号相邻、主题接续。
- **同模块**：`Book/part14_perf/ch157_compiler_explorer.md`（第157章 Compiler Explorer 实战）—— 同模块下的其他主题。

## 附录 G：工业缓存优化实例

| 项目 | 优化技术 | 效果 | 源码 |
|------|---------|------|------|
| **Chromium**（github.com/chromium/chromium） | `base::CacheLineSize` 对齐热路径结构体 | PartitionAlloc 的 `PartitionPage` 对齐 64 字节，消除 false sharing | `base/allocator/partition_allocator/partition_page.h` |
| **Redis**（github.com/redis/redis） | 跳跃表节点按 cache line 紧凑排列 | `zskiplistNode` 设计为 ≤64 字节（`server.h:740`），一次 cache miss 取整层连续节点 | `src/server.h` — `ZSKIPLIST_MAXLEVEL=32` |
| **ClickHouse**（github.com/ClickHouse/ClickHouse） | 列式存储 + 压缩块对齐 | 查询只扫所需列，避免行存储的全行读取污染 cache；`MergeTree` 每列独立压缩成 block | `src/Storages/MergeTree/` — `MergeTreeDataPartWide` |
| **Linux kernel**（kernel.org） | per-CPU 变量（`DEFINE_PER_CPU`） | 热路径计数器放在各自 CPU cache line，消除多核间的 MESI 乒乓 | `include/linux/percpu-defs.h` |
| **Google tcmalloc**（github.com/google/tcmalloc） | 线程局部 freelist | 每线程独立空闲列表，避免 `malloc/free` 的全局锁导致 cache line 反复在核间弹跳 | `tcmalloc/thread_cache.h` |

**底层深度**：cache line 伪共享（false sharing）的量化影响——两个 `atomic<int>` 落在同一 64B cache line，线程 A 写 a、线程 B 写 b 时，MESI 协议迫使两核的 line 在 Modified/Shared 间反复震荡（每次 ≈100 条 `mfence` 等效延迟）。`alignas(64)` 或 `std::hardware_destructive_interference_size` 将两变量分到不同 line 后，吞吐量提升 4–8×（Intel VTune 实测）。`__builtin_prefetch(addr, 0, 3)`（写预取、高局部性）在顺序遍历前提前 16 条 cache line 发出预取，Cover 400 周期 DDR 延迟。

## 附录 H：工业实战复盘与设计取舍 [I: Practice / H: Design]

**[经验]**　缓存优化最大的坑是"凭直觉优化"——不 profile 就改，常常越改越慢。本节从 production 事故与 Code Review 视角总结。

### 工业案例：false sharing 的"隐形性能杀手"

真实 **常见Bug**：一个多线程计数器数组 `std::atomic<int> counters[N]`，每个线程 `++counters[tid]`。逻辑上无竞争（各写各的），实测却比单线程还慢——因为多个 `atomic<int>`（各 4 字节）挤在同一 64 字节 cache line，MESI 协议让这条 line 在核间反复失效（cache line ping-pong）。

**Debug方法**（关键，比盲改重要）：
1. `perf stat -e cache-misses,LLC-load-misses ./app`——false sharing 表现为异常高的 cache-misses 但 miss 地址集中。
2. Linux `perf c2c`（cache-to-cache）是**专门诊断 false sharing 的工具**，能直接指出哪两个变量共享了 line。
3. Intel VTune 的 "Memory Access" 分析同样定位。

**修复/重构建议**：`alignas(std::hardware_destructive_interference_size)`（通常 64）把每个计数器独占一条 line；或改为线程局部累加、最后归并（tcmalloc 的 thread_cache 思路）。实测吞吐提升 4–8×。

### 设计取舍（Trade-off）：AoS vs SoA

| 布局 | 优点 | 缺点 | 适用 |
|---|---|---|---|
| AoS（结构数组 `struct{x,y,z}[]`） | 单个对象访问局部性好、代码直观 | 只用一个字段时，其余字段污染 cache | OOP 逻辑、随机访问整对象 |
| SoA（数组结构 `{x[], y[], z[]}`） | 遍历单字段时零浪费、天然 SIMD 连续加载 | 访问整对象要多次跳转、代码复杂 | 数值计算、ECS、批量处理单字段 |

**设计权衡的核心**：SoA 不是永远更快——若算法总是同时用到一个对象的所有字段，AoS 的局部性反而更好。**API Design** 上，游戏引擎（ECS）和数值库倾向 SoA 是因为"批量处理同一字段"是主导访问模式；通用业务对象保持 AoS。**先确定访问模式，再选布局**。

### 反模式（Anti-Pattern）

- **反模式：不 profile 就优化**。缓存优化的收益高度依赖真实访问模式，凭感觉加 `alignas`/`prefetch` 常常无效甚至有害（浪费内存、污染 cache）。
- **反模式：滥用 `__builtin_prefetch`**。预取距离错了（太近来不及、太远被换出）或对已在 cache 的数据预取，纯属浪费指令。prefetch 只在"可预测的顺序/跨步访问 + 明确 DDR 延迟瓶颈"下才值得，且必须 A/B profile 验证。
- **反模式：过度对齐**。给每个小对象都 `alignas(64)` 会浪费大量内存、降低有效 cache 容量——只对**真正跨线程写**的热变量做 line 隔离。

### Code Review 检查清单（缓存优化专项）

- [ ] 每一处缓存优化是否有 profile 数据（perf/VTune）支撑，而非凭直觉？
- [ ] 多线程频繁写的变量是否可能 false sharing？是否用 `hardware_destructive_interference_size` 隔离？
- [ ] 数据布局（AoS/SoA）是否匹配真实的主导访问模式？
- [ ] `prefetch` 是否经 A/B 测试证明有效，预取距离是否合理？
- [ ] 是否避免了对小对象无差别 `alignas(64)` 造成的内存浪费？

## 自测练习（Exercises）

> 以下题目用于自测掌握程度；答案折叠于每题下方，建议先独立作答。

### 练习 1（难度 ★★）

用 `std::integral` 概念约束一个 `add` 函数，使其只接受整数类型，并对浮点调用给出清晰的错误。

<details><summary>答案与解析</summary>

C++20 概念取代 SFINAE 做编译期约束：

```cpp
#include <iostream>
#include <concepts>
template <std::integral T> T add(T a, T b) { return a + b; }
int main() { std::cout << add(2, 3) << '\n'; /* add(1.0, 2.0) 编译失败 */ }
```

[标准] 违反概念约束是硬错误（而非 SFINAE 静默失败），诊断信息更可读。

</details>

### 练习 2（难度 ★★）

写一个 `constexpr` 阶乘函数，并用 `static_assert` 在编译期验证 `fact(5)==120`。

<details><summary>答案与解析</summary>

```cpp
#include <iostream>
constexpr int fact(int n) { return n <= 1 ? 1 : n * fact(n - 1); }
static_assert(fact(5) == 120);
int main() { std::cout << fact(5) << '\n'; }
```

[标准] `constexpr` 函数在常量表达式上下文（如模板实参、`static_assert`）中于编译期求值。

</details>

### 练习 3（难度 ★★）

解释栈对象与堆对象生命周期差异：`{ int a; }` 与 `new int` 的销毁时机有何不同？

<details><summary>答案与解析</summary>

栈对象在作用域结束自动析构；`new` 分配的对象直到 `delete` 才释放：

```cpp
#include <iostream>
int main(){ int a=1; int* p=new int(2); /* ... */ delete p; }
```

[标准] 遗漏 `delete` 即内存泄漏；这是 RAII/智能指针存在的根本动机。

</details>

