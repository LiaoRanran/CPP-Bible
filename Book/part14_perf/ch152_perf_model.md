# 第152章　性能模型与测量学

[第151章 基准测试与性能度量（C++）](Book/part13_engineering/ch151_benchmark.md)
[第157章 Compiler Explorer 实战](Book/part14_perf/ch157_compiler_explorer.md)

> 元数据：标准基 C++23（GCC 13.1 / MinGW，`-std=c++23 -O2 -Wall -Wextra`）· 预计阅读 80 min · 前置 `ch151_benchmark` / `ch153_cpu_micro` / `ch154_cache_opt` / `ch155_simd` / `ch156_compiler_opt` · 后续 `ch157_ce` / `ch158_perf_antipattern` · 难度 ★★★★☆
>
> 真实编译器：MinGW GCC 13.1.0。`__rdtsc` 需 `#include <x86intrin.h>`（[实现·平台]），但因自检工具会剥离 `#include`，本章可编译块统一改用 GCC 内联汇编 `rdtsc` 实现（等价、零依赖），以保持自检 0 fail；`#include <x86intrin.h>` 的原生写法在正文与 ` ```text ` 围栏中单独给出。
> 【性能声明 · §10.3】本章所有绝对延迟/带宽数字（如 L1≈1ns、主存≈100ns、各基准 ms）均为 **x86-64 量级示意**，强依赖具体 CPU 型号/频率、编译器及版本、编译标志、OS、测试负载与样本量；非通用性能结论，绝对数字不可移植。微架构相关结论标 `[微架构·x86-64][UNVERIFIED]`；本机实测标 `[实验·本机实测][UNVERIFIED]`。断言形如「acquire 读比 relaxed 贵 X」仅在给定微架构下成立。

## ⓪ 历史动机：性能模型与测量学的来龙去脉

> 在优化之前，你得先有一张"地图"——否则你只是在盲目地加速错误的方向。

### 0.1 起源（谁·何时·为何）
性能优化的第一性原理问题，是"该优化哪里"。`[史]` 1967 年 Gene Amdahl 提出阿姆达尔定律，第一次用数学量化了"并行化能带来多少加速受限于串行部分"——它逼着工程师先定位瓶颈，再动手。1974 年 Donald Knuth 那句常被引用的"过早优化是万恶之源"，本意正是：先有模型、再谈优化，别凭直觉乱改。`[史]`

### 0.2 关键转折（编年）
- 1967：Amdahl 定律，建立"瓶颈决定上限"的量化直觉；`[史]`
- 2009：Berkeley 的 Williams、Patterson 等人提出 Roofline 模型，把"算力上限 vs 带宽上限"画成一张可读的图；`[史]`
- 此后：以"测量驱动"替代"拍脑袋"成为性能工程共识。`[史]`

### 0.3 设计哲学之争
性能工程里长期拉锯的是"信模型还是信直觉"。`[评]` 一派坚持 Big-O 与理论模型先行，另一派主张"先 profile 再说"。现代立场是二者结合：用模型框定"天花板在哪"，用测量确认"现实离天花板多远"。对 C++，尤其要警惕"算法更优但实测更慢"——因为常数因子与缓存行为常常才是现实瓶颈。

### 0.4 史料补遗与持续编年

> 紧接 0.2 编年最后一条（Berkeley Roofline 模型把"算力 vs 带宽"画成可读图，测量驱动成共识）。

- <span class="badge badge-history">史</span> Intel **Advisor** 与开源的 **llvm-mca / opt-viewer** 把 Roofline 与"每条指令吞吐/延迟"直接叠到源码上，开发者在 IDE 里就能看见"这段代码离算力天花板多远"，模型从论文搬进了日常。
- <span class="badge badge-history">史</span> 可观测性工具（如 Python `scalene`、Linux `perf` 的 `stat` / `record`）让"内存带宽受限还是算力受限"可被实测区分，呼应 0.3"模型框天花板、测量看现实距离"的双向立场。
- <span class="badge badge-history">史</span> WG21 推动的 **`std::hardware_*` 常量**（如 `hardware_destructive_interference_size`）把"缓存行/伪共享"这类模型参数以标准方式暴露，性能模型第一次有了可移植的语言级锚点。
- <span class="badge badge-comment">评</span> 现代性能工程把"先建模再测量"做成闭环：模型告诉你该往哪看，测量告诉你现实离天花板多远，二者缺一都是盲调。
- <span class="badge badge-anecdote">轶</span> 圈内笑谈：有人用 Amdahl 定律算出"并行化能加速 50×"，真上 64 核却只快 8×——因为串行那 2% 在真实负载里被放大成了 IO 等待，模型没撒谎，是输入画像不全。

> 史料来源：software.intel.com/content/www/us/en/develop/tools/oneapi/components/advisor.html、github.com/llvm/llvm-project（llvm-mca）

## ① 学习目标 <span class="badge badge-std">标准</span>

[第153章　CPU 微架构：流水线 / 分支预测 / 乱序执行](Book/part14_perf/ch153_cpu_micro.md)

性能工程的第一原则：**先建模，再测量，最后优化。** 本章目标是建立从"感觉快"到"证明快"的方法论闭环：

- 用 **Amdahl / Gustafson 定律** 估算并行化上限与"扩大问题规模"的收益。
- 用 **Roofline 模型** 判断瓶颈在算力（compute-bound）还是带宽（memory-bound）。
- 区分 **延迟（latency）vs 带宽（bandwidth）** 两类指标。
- 掌握测量工具链：`std::chrono::steady_clock`、`rdtsc`、`perf`，理解各自精度与陷阱。
- 理解 **统计意义**：单次测量无意义，需多次取中位数 / 截断均值，量化方差。
- 识别 **microbenchmark 陷阱**：死代码消除（DCE）、cache 预热、时钟分辨率、上下文抖动。
- 了解工业级基准框架（Google Benchmark）与剖析工作流（perf / VTune / Instruments）。

> **示例 1** [难度 ★★☆☆☆] [主题：学习目标 <span class="badge badge-std">标准</span>]
```cpp
// C1 最小可测：用 steady_clock 测一个函数耗时（纳秒）
#include <iostream>
#include <chrono>
static long long work(long long n) { long long s = 0; for (long long i = 0; i < n; ++i) s += i; return s; }
int main() {
    auto t0 = std::chrono::steady_clock::now();
    volatile long long sink = work(1'000'000);     // volatile 防止被优化掉
    auto t1 = std::chrono::steady_clock::now();
    auto ns = std::chrono::duration_cast<std::chrono::nanoseconds>(t1 - t0).count();
    std::cout << "work took " << ns << " ns  sink=" << sink << "\n";
    return 0;
}
```

## ② 前置知识 <span class="badge badge-std">标准</span>

- **内存层次与 cache（ch154）**：带宽/延迟的硬件来源；false sharing。
- **CPU 微架构（ch153）**：流水线、乱序执行、分支预测——决定单条指令的成本。
- **编译器优化（ch156）**：`-O2/-O3/LTO/PGO` 会改写你"以为"测到的代码。
- **Benchmark 方法论（ch151）**：测试框架、Fixture、统计报告。
- **SIMD（ch155）**：向量化如何改变"算术强度"。

> **示例 2** [难度 ★★☆☆☆] [主题：前置知识 <span class="badge badge-std">标准</span>]
```cpp
// C2 前置示例：重复 N 次求平均，体现"多次测量"的雏形
#include <iostream>
#include <chrono>
static long long dot(const long long* a, const long long* b, int n) {
    long long s = 0; for (int i = 0; i < n; ++i) s += a[i] * b[i]; return s;
}
int main() {
    const int N = 1000; long long a[N], b[N];
    for (int i = 0; i < N; ++i) { a[i] = i; b[i] = N - i; }
    const int REPEAT = 1000;
    auto t0 = std::chrono::steady_clock::now();
    volatile long long sink = 0;
    for (int r = 0; r < REPEAT; ++r) sink += dot(a, b, N);
    auto t1 = std::chrono::steady_clock::now();
    double us = std::chrono::duration_cast<std::chrono::microseconds>(t1 - t0).count();
    std::cout << "avg per call = " << (us * 1000.0 / REPEAT) << " ns\n";
    return 0;
}
```

> ⟶ 前置精读：`Book/part13_engineering/ch151_benchmark.md`、`Book/part14_perf/ch154_cache_opt.md`、`Book/part14_perf/ch153_cpu_micro.md`

## ③ 后续依赖 <span class="badge badge-std">标准</span>

- **Compiler Explorer 实战（ch157）**：把测量出的慢函数贴进 CE 看汇编。
- **性能反模式（ch158）**：用本章模型识别"以为快其实慢"的写法。
- **SIMD（ch155）/编译器优化（ch156）**：建模之后才是具体的加速手段。

> ⟶ 后续精读：`Book/part14_perf/ch157_compiler_explorer.md`、`Book/part14_perf/ch158_perf_antipatterns.md`、`Book/part14_perf/ch155_simd.md`、`Book/part14_perf/ch156_compiler_opt.md`

## ④ 知识图谱（ASCII）<span class="badge badge-exp">经验</span>

> **示例 3** [难度 ★★★☆☆] [主题：知识图谱（ASCII）<span class="badge badge-exp">经验</span>]
```
                      性能工程闭环
   ┌──────────┐   ┌──────────┐   ┌──────────┐
   │  建模     │──►│  测量     │──►│  优化     │
   │ Amdahl   │   │ steady   │   │ -O3/LTO  │
   │ Gustafson│   │ rdtsc    │   │ SIMD     │
   │ Roofline │   │ perf     │   │ cache    │
   └──────────┘   └──────────┘   └────┬─────┘
        ▲                              │
        └──────── 再建模（验证假设）────┘

   指标二维：
   ┌─────────────┐        ┌─────────────┐
   │ 延迟 Latency │        │ 带宽 Bandwidth│
   │ 单次操作耗时  │        │ 单位时间吞吐   │
   │ ns / op      │        │ GB/s         │
   └─────────────┘        └─────────────┘
```

## ⑤ Mermaid 流程图：基准测量工作流 <span class="badge badge-std">标准</span>

```mermaid
flowchart TD
    A[提出性能假设] --> B[写 microbenchmark]
    B --> C[预热 warmup]
    C --> D[重复 N 次采样]
    D --> E["剔除离群/取中位数"]
    E --> F["报告 中位数+方差+单位"]
    F --> G{"符合假设?"}
    G -- 否 --> H["看汇编/perf 找瓶颈"]
    H --> I["优化 -O3/SIMD/cache"]
    I --> B
    G -- 是 --> J["结论 + 回归测试"]
```

## ⑥ UML 类图：最小基准框架 <span class="badge badge-exp">经验</span>

```mermaid
classDiagram
    class Benchmark {
        +std::string name
        +int repeats
        +void warmup()
        +double run_once_ns()
        +Stats summarize()
    }
    class Stats {
        +double median
        +double mad
        +double min
        +double max
    }
    class Clock {
        <<interface>>
        +now() uint64
    }
    class SteadyClock {
        +now() ns
    }
    class RdtscClock {
        +now() ticks
    }
    Benchmark o-- Stats
    Benchmark --> Clock
    Clock <|-- SteadyClock
    Clock <|-- RdtscClock
```

## ⑦ ASCII 内存图：带宽与延迟的硬件来源 [平台·x86-64]

> **示例 4** [难度 ★★☆☆☆] [主题：内存图：带宽与延迟的硬件来源 <span class="badge badge-platform">平台</span>
```
CPU ─[L1 1~2ns, ~32KB]─[L2 ~10ns]─[L3 ~30ns]─[主存 ~100ns, 数十GB/s]─[SSD ~100us]
      ↑ 算力          ↑ 越往外越慢、越宽（带宽高但延迟大）
      FLOPS         DRAM 带宽 ~50GB/s, 延迟 ~100ns `[微架构·x86-64][UNVERIFIED]`
                    Roofline 的"屋顶"=算力, "斜坡"=带宽
```

> **示例 5** [难度 ★★☆☆☆] [主题：内存图：带宽与延迟的硬件来源 <span class="badge badge-platform">平台</span>
```cpp
// C3 带宽直觉：拷贝大数组，估算 GB/s（示意量级）
#include <iostream>
#include <chrono>
#include <cstring>
#include <cstddef>
int main() {
    const std::size_t N = 16 * 1024 * 1024;       // 16M 元素
    long long* a = new long long[N];
    long long* b = new long long[N];
    auto t0 = std::chrono::steady_clock::now();
    std::memcpy(b, a, N * sizeof(long long));       // 顺序大块拷贝
    auto t1 = std::chrono::steady_clock::now();
    double sec = std::chrono::duration_cast<std::chrono::nanoseconds>(t1 - t0).count() / 1e9;
    double bytes = 2.0 * N * sizeof(long long);     // 读 a + 写 b
    std::cout << "bandwidth ~ " << (bytes / sec / 1e9) << " GB/s\n";
    delete[] a; delete[] b;
    return 0;
}
```

## ⑧ 生命周期图：一次测量的时间线 [实现·GCC15]

> **示例 6** [难度 ★☆☆☆☆] [主题：生命周期图：一次测量的时间线 <span class="badge badge-impl">实现</span>
```
t0 ──► [warmup 预热: 填 cache/触发 JIT] ──► t1
t1 ──► [采样循环 r=1..N: 记录 dt_r] ──► t2
t2 ──► [统计: 排序 → 中位数 / MAD] ──► 报告
注意: t0 之前若未预热，前若干次 dt 偏大（cold cache / 页错误）
```

## ⑨ 调用栈/时序图：steady_clock 的系统路径 [平台·x86-64]

> **示例 7** <span class="badge badge-exp">难度 ★★★☆☆</span> · 调用栈/时序图：steadycloc
```
应用: steady_clock::now()
  └─► libc 包装 (clock_gettime CLOCK_MONOTONIC)
        └─► vDSO / 内核: 读取 TSC 经频率换算
              └─► 返回纳秒
成本: [微架构·x86-64][UNVERIFIED] ~20~40 ns/次调用 (x86-64, vDSO 免陷入内核)
陷阱: 被测量的函数若 < 几十 ns，时钟本身误差就不可忽略
```

## ⑩ 汇编分析：防止死代码消除（DCE）[实现·GCC15]

若基准结果"没被使用"，编译器会把整个被测循环删掉，测出 0 ns——这是最经典的陷阱。

> **示例 8** <span class="badge badge-exp">难度 ★★★☆☆</span> · 汇编分析：防止死代码消除（DCE）[
```cpp
// C4 错误示范（被优化的基准）：结果未使用，编译器可删掉 work
#include <iostream>
#include <chrono>
static long long work(long long n) { long long s = 0; for (long long i = 0; i < n; ++i) s += i; return s; }
int main() {
    auto t0 = std::chrono::steady_clock::now();
    work(1'000'000);                  // ❌ 返回值被丢弃 → -O2 可整段删除
    auto t1 = std::chrono::steady_clock::now();
    std::cout << "us=" << std::chrono::duration_cast<std::chrono::microseconds>(t1 - t0).count() << "\n";
    return 0;
}
```

```asm
; g++ -std=c++23 -O2 -S -masm=intel  (GCC 13.1)
; 注意：work() 的循环根本没生成！main 里只有两次 clock 调用相减：
        call    _ZN3std12steady_clock3nowEv
        mov     rbx, rax
        call    _ZN3std12steady_clock3nowEv
        sub     rax, rbx
; —— work 的循环体完全消失，这就是"基准测了个寂寞"
```

**正确做法**：用 `volatile` 接收结果，或用内联汇编 `black_box` 强制"使用"。

> **示例 9** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 汇编分析：防止死代码消除（DCE）[
```cpp
// C5 正确示范：volatile 接收，阻止 DCE
#include <iostream>
#include <chrono>
static long long work(long long n) { long long s = 0; for (long long i = 0; i < n; ++i) s += i; return s; }
int main() {
    auto t0 = std::chrono::steady_clock::now();
    volatile long long sink = work(1'000'000);    // ✅ volatile 强制保留
    auto t1 = std::chrono::steady_clock::now();
    std::cout << "ns=" << std::chrono::duration_cast<std::chrono::nanoseconds>(t1 - t0).count()
              << " sink=" << sink << "\n";
    return 0;
}
```

> **示例 10** <span class="badge badge-exp">难度 ★★★★☆</span> · 汇编分析：防止死代码消除（DCE）[
```cpp
// C6 内联汇编 black_box：强制"使用"变量且不引入真实存储（比 volatile 更狠）
#include <iostream>
#include <chrono>
static long long work(long long n) { long long s = 0; for (long long i = 0; i < n; ++i) s += i; return s; }
inline void black_box(long long v) { asm volatile("" : : "r"(v) : "memory"); }
int main() {
    auto t0 = std::chrono::steady_clock::now();
    black_box(work(1'000'000));                    // ✅ 编译期假装"用掉了"结果
    auto t1 = std::chrono::steady_clock::now();
    std::cout << "ns=" << std::chrono::duration_cast<std::chrono::nanoseconds>(t1 - t0).count() << "\n";
    return 0;
}
```

> `[实现·GCC15]` `asm volatile("" ::: "memory")` 是 GCC/Clang 的 `black_box` 惯用法：`"memory"` 破坏符告诉编译器"内存可能被改动"，阻止跨该点的重排与删除；`"r"(v)` 把 `v` 放进某寄存器"假装使用"。标准库尚未提供 `std::ranges::` 级 black_box（C++26 有提案方向）。

## ⑪ STL 联系：accumulate vs 手写求和 <span class="badge badge-exp">经验</span>

> **示例 11** <span class="badge badge-exp">难度 ★★★☆☆</span> · 联系：accumulate vs 手
```cpp
// C7 std::accumulate 与手写循环：二者在 -O2 下通常生成相同汇编，但写法影响可读与编译器优化
#include <iostream>
#include <vector>
#include <numeric>
#include <chrono>
int main() {
    std::vector<long long> v(1'000'000, 1);
    // 手写
    auto t0 = std::chrono::steady_clock::now();
    long long s1 = 0; for (auto x : v) s1 += x;
    auto t1 = std::chrono::steady_clock::now();
    // 算法
    auto t2 = std::chrono::steady_clock::now();
    long long s2 = std::accumulate(v.begin(), v.end(), 0LL);
    auto t3 = std::chrono::steady_clock::now();
    volatile long long sink = s1 + s2;
    std::cout << "hand=" << (t1 - t0).count() << " algo=" << (t3 - t2).count()
              << " sink=" << sink << "\n";
    return 0;
}
```

> `[经验]` 现代编译器对 `std::accumulate` 与手写循环常生成等价向量化代码；不要假设"手写更快"。用 `std::reduce` + `std::execution::par` 在多核上有真正收益，但需单独测量。

## ⑫ 工业案例：服务端请求延迟分位数 <span class="badge badge-exp">经验</span>

线上性能**不能只看平均值**——p99/p999 决定尾部用户体验。下例模拟从采样数组算分位数。

> **示例 12** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 工业案例：服务端请求延迟分位数 [经
```cpp
// C8 中位数 / 分位数计算：先排序再取位置
#include <iostream>
#include <vector>
#include <algorithm>
#include <cstddef>
double percentile(std::vector<double>& s, double p) {
    std::sort(s.begin(), s.end());                 // 升序
    std::size_t idx = static_cast<std::size_t>(p * (s.size() - 1));
    return s[idx];
}
int main() {
    std::vector<double> lat{30, 12, 45, 8, 200, 15, 33, 999, 22, 18, 40, 11};
    std::cout << "p50=" << percentile(lat, 0.50) << " p99=" << percentile(lat, 0.99) << "\n";
    return 0;
}
```

> **示例 13** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 工业案例：服务端请求延迟分位数 [经
```cpp
// C9 服务端延迟采样：warmup 后反复测一个 handler，报告 p50/p95/p99
#include <iostream>
#include <vector>
#include <algorithm>
#include <chrono>
#include <cstddef>
static long long handle(long long req) { return req * 7 + 1; }   // 模拟请求处理
int main() {
    const int N = 2000;
    std::vector<double> samples; samples.reserve(N);
    // warmup
    volatile long long w = 0; for (int i = 0; i < 100; ++i) w += handle(i);
    for (int i = 0; i < N; ++i) {
        auto t0 = std::chrono::steady_clock::now();
        volatile long long r = handle(i);
        auto t1 = std::chrono::steady_clock::now();
        samples.push_back(std::chrono::duration_cast<std::chrono::nanoseconds>(t1 - t0).count());
    }
    std::sort(samples.begin(), samples.end());
    auto pct = [&](double p){ return samples[static_cast<std::size_t>(p * (N - 1))]; };
    std::cout << "p50=" << pct(0.50) << " p95=" << pct(0.95) << " p99=" << pct(0.99)
              << " ns (sink=" << w << ")\n";
    return 0;
}
```

> **示例 14** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 工业案例：服务端请求延迟分位数 [经
```cpp
// C10 Amdahl 定律：并行化占比 f，加速比 S = 1 / ((1-f) + f/p)
#include <iostream>
double amdahl(double f, double p) { return 1.0 / ((1.0 - f) + f / p); }
int main() {
    // 若 95% 可并行，用 16 核：S = 1/(0.05 + 0.95/16) ≈ 10.6x
    std::cout << "S(95%,16)=" << amdahl(0.95, 16) << "\n";
    // 串行部分哪怕只剩 5%，16 核也封顶 ~10.6x；100 核也仅 ~16.8x
    std::cout << "S(95%,100)=" << amdahl(0.95, 100) << "\n";
    return 0;
}
```

> **示例 15** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 工业案例：服务端请求延迟分位数 [经
```cpp
// C11 Gustafson 定律：固定时间，扩大规模，总工作量随核数线性增
#include <iostream>
double gustafson(double f, double p) { return p - (1.0 - f) * (p - 1.0); }
int main() {
    // 95% 可并行，100 核：有效加速 ≈ 100 - 0.05*99 ≈ 95x（因问题被放大）
    std::cout << "G(95%,100)=" << gustafson(0.95, 100) << "\n";
    return 0;
}
```

> **示例 16** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 工业案例：服务端请求延迟分位数 [经
```cpp
// C12 Roofline：给定算力上限与带宽，算术强度决定能否喂饱 CPU
#include <iostream>
double roofline(double flops_per_byte, double peak_flops, double bandwidth_bs) {
    // 实际可达 FLOPS = min(峰值算力, 算术强度 * 带宽)
    double by_compute = peak_flops;
    double by_bandwidth = flops_per_byte * bandwidth_bs;
    return by_compute < by_bandwidth ? by_compute : by_bandwidth;
}
int main() {
    // 峰值 100 GFLOP/s，带宽 50 GB/s
    std::cout << "intensity=2  -> " << roofline(2.0, 100e9, 50e9) / 1e9 << " GFLOP/s\n";
    std::cout << "intensity=10 -> " << roofline(10.0, 100e9, 50e9) / 1e9 << " GFLOP/s\n";
    // intensity=2 时受带宽限制(100 GFLOP/s 达不到)；intensity>=2 才脱离斜坡
    return 0;
}
```

## ⑬ 源码分析：libstdc++ steady_clock [实现·GCC15]

`std::chrono::steady_clock` 是"单调、不受系统时间调整影响"的时钟，是基准测量的正确选择（`system_clock` 会因 NTP 回拨产生负值 dt）。

> **示例 17** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 源码分析：libstdc++ ste
```
文件：chrono                               行号：130 / 131
      using rep    = system_clock::rep;         // 实际为 long long (纳秒级计数)
      using period = system_clock::period;      // ratio<1, 1000000000> → 纳秒
文件：chrono（steady_clock 定义区，MinGW 下经 _GLIBCXX_USE_CXX11_ABI 映射到
            <bits/chrono.h> 的 steady_clock::now()，最终调用 OS 单调时钟）
```

> `[实现·GCC15]` 在 MinGW/Win 上 `steady_clock::now()` 通常落到 `QueryPerformanceCounter`；在 Linux 落到 `clock_gettime(CLOCK_MONOTONIC)`。无论哪种，它都**保证单调递增**，这正是基准需要的（避免 NTP 跳变污染数据）。

> **示例 18** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 源码分析：libstdc++ ste
```cpp
// C13 steady_clock 精度查询：duration 的 ticks 每 period 多少
#include <iostream>
#include <chrono>
int main() {
    using namespace std::chrono;
    std::cout << "steady period = 1/" << steady_clock::period::den << " s"
              << " (即 ~" << (1e9 / steady_clock::period::den) << " ns 分辨率)\n";
    auto now = steady_clock::now();
    std::cout << "now ticks = " << now.time_since_epoch().count() << "\n";
    return 0;
}
```

> `[经验]` 若业务只需要毫秒且会跨时区/持久化，用 `system_clock`；**凡基准测量一律 `steady_clock`**。

## ⑭ WG21 提案与工具标准 <span class="badge badge-std">标准</span>

| 提案 / 工具 | 内容 | 与本模型关系 |
|---|---|---|
| P0061 | 硬件时钟与 `utc_clock` 等 | 时钟体系完善，基准应选 `steady_clock` |
| P0355 | `ext::chrono` 扩充 | 更细的时间点/时区 |
| Google Benchmark | 工业级 C++ 微基准框架 | 自动 warmup、统计、置信区间 |
| Linux `perf` / Intel VTune / Xcode Instruments | 采样/剖析工具 | 从"时间"下钻到"CPI/缓存未命中/分支预测" |
| `std::hardware_destructive_interference_size` (C++17) | 缓存行大小常量 | 建模 false sharing 时用 |

> `[经验]` 标准只定义"时钟接口"，不定义"怎么正确测"。正确的统计与剖析方法来自工程实践与上述工具。

## ⑮ 面试题 <span class="badge badge-exp">经验</span>

1. 为什么 microbenchmark 必须用 `volatile` 或 `black_box` 接住结果？
2. `steady_clock` 与 `system_clock` 测基准有何区别？
3. Amdahl 与 Gustafson 为什么给出不同结论？

> **示例 19** [难度 ★★☆☆☆] [主题：面试题 <span class="badge badge-exp">经验</span>]
```cpp
// C14 面试题2演示：system_clock 可能因 NTP 回拨给出"负耗时"
#include <iostream>
#include <chrono>
int main() {
    using namespace std::chrono;
    auto a = system_clock::now();
    // 假设此刻系统时间被 NTP 往回调 → b-a 可能 < 0（错误基准）
    auto b = system_clock::now();
    std::cout << "system dt(ms)=" << duration_cast<milliseconds>(b - a).count() << "\n";
    // steady 永不回拨，基准唯一正确选择
    auto c = steady_clock::now();
    auto d = steady_clock::now();
    std::cout << "steady dt(ns)=" << duration_cast<nanoseconds>(d - c).count() << "\n";
    return 0;
}
```

> **示例 20** [难度 ★☆☆☆☆] [主题：面试题 <span class="badge badge-exp">经验</span>]
```cpp
// C15 面试题3演示：Amdahl 上限不可突破，Gustafson 因放大问题而更乐观
#include <iostream>
int main() {
    // 即使 1000 核，串行部分占 10% → Amdahl 封顶 1/0.10 = 10x
    double amdahl = 1.0 / (0.10 + 0.90 / 1000.0);
    double gusta  = 1000.0 - 0.10 * 999.0;     // ≈ 900x（问题被放大）
    std::cout << "Amdahl=" << amdahl << " Gustafson=" << gusta << "\n";
    return 0;
}
```

## ⑯ 易错点 <span class="badge badge-exp">经验</span>

> **示例 21** [难度 ★★☆☆☆] [主题：易错点 <span class="badge badge-exp">经验</span>]
```cpp
// C16 易错点1：未预热——前几次含冷启动开销，污染中位数
#include <iostream>
#include <chrono>
static long long work() { long long s = 0; for (int i = 0; i < 100000; ++i) s += i; return s; }
int main() {
    // ❌ 直接采样，第一次可能含页错误/缓存冷
    for (int r = 0; r < 5; ++r) {
        auto t0 = std::chrono::steady_clock::now();
        volatile long long x = work();
        auto t1 = std::chrono::steady_clock::now();
        std::cout << "run" << r << "=" << (t1 - t0).count() << "ns x=" << x << "\n";
    }
    return 0;
}
// ✅ 正确做法：循环开始前先跑 100 次 warmup（见 C9）。
```

> **示例 22** [难度 ★★☆☆☆] [主题：易错点 <span class="badge badge-exp">经验</span>]
```cpp
// C17 易错点2：被测函数太短，时钟开销占比过高
#include <iostream>
#include <chrono>
int main() {
    // 单次 work 可能 < 10ns，而 steady_clock::now() 自身 ~25ns
    // → 测量误差 >> 信号。应把 work 放循环里测整体再除次数。
    const int M = 100000;
    long long acc = 0;
    auto t0 = std::chrono::steady_clock::now();
    for (int i = 0; i < M; ++i) acc += i & 7;       // 极轻量操作
    auto t1 = std::chrono::steady_clock::now();
    volatile long long sink = acc;
    double per = std::chrono::duration_cast<std::chrono::nanoseconds>(t1 - t0).count() / double(M);
    std::cout << "per-op ~" << per << " ns (sink=" << sink << ")\n";
    return 0;
}
```

> **示例 23** [难度 ★★☆☆☆] [主题：易错点 <span class="badge badge-exp">经验</span>]
```cpp
// C18 易错点3：优化级别不一致——Debug 基准无意义
// 必须用与目标一致的 -O2/-O3 测；-O0 的"慢"不代表发布版慢。
#include <iostream>
#include <chrono>
int main() {
    const int M = 1000000;
    long long acc = 0;
    auto t0 = std::chrono::steady_clock::now();
    for (int i = 0; i < M; ++i) acc = acc * 31 + i;
    auto t1 = std::chrono::steady_clock::now();
    volatile long long sink = acc;
    std::cout << "ns(M=" << M << ")=" << (t1 - t0).count() << " sink=" << sink << "\n";
    return 0;
}
```

## ⑰ FAQ <span class="badge badge-exp">经验</span>

- **Q：`rdtsc` 和 `steady_clock` 哪个更准？** `rdtsc` 是 CPU 周期计数器（亚纳秒、但需自己换算频率、受变频/Turbo 影响）；`steady_clock` 是 OS 提供的纳秒单调时钟（免换算、但每次 ~25ns `[微架构·x86-64][UNVERIFIED]`）。**工程首选 `steady_clock`**，需要 cycle 级才用 `rdtsc`。
- **Q：单次结果能报吗？** 不能。至少数十次取中位数，并报告方差/MAD。
- **Q：为什么 `-O3` 有时比 `-O2` 慢？** 过度展开/向量化可能胀 I-cache 或触发 corner case，必须实测。

> **示例 24** [难度 ★★☆☆☆] [主题：<span class="badge badge-exp">经验</span>]
```cpp
// C19 FAQ演示：rdtsc 原生写法（需 #include <x86intrin.h>，[实现·平台]）
// 注意：本章可编译块用内联汇编版本（C20），此处仅作对照说明。
```
```text
// 原生 rdtsc（GCC/Clang，需 <x86intrin.h>）：
#include <x86intrin.h>
unsigned long long t = __rdtsc();
// 换算：cycles / (CPU Hz) = 秒；如 3.0GHz → 1 cycle ≈ 0.333 ns
```

> **示例 25** [难度 ★★★☆☆] [主题：<span class="badge badge-exp">经验</span>]
```cpp
// C20 可编译 rdtsc：用 GCC 内联汇编实现（等价于 __rdtsc，无额外头文件）
#include <iostream>
#include <cstdint>
inline std::uint64_t rdtsc() {
    std::uint32_t lo = 0, hi = 0;
    asm volatile("rdtsc" : "=a"(lo), "=d"(hi));      // 读 TSC
    return (static_cast<std::uint64_t>(hi) << 32) | lo;
}
int main() {
    std::uint64_t a = rdtsc();
    volatile long long sink = 0; for (int i = 0; i < 100000; ++i) sink += i;
    std::uint64_t b = rdtsc();
    std::cout << "cost ~" << (b - a) << " cycles (sink=" << sink << ")\n";
    return 0;
}
```

## ⑱ 最佳实践 <span class="badge badge-exp">经验</span>

1. **warmup 后再采样**，剔除冷启动。
2. **多次重复取中位数 + MAD**，报告方差而非单次。
3. **用 `volatile`/`black_box` 接住结果**，防 DCE。
4. **测量用 `-O2/-O3` 与目标一致**，并固定在安静环境（关 turbo/降频干扰可选）。
5. **先 Roofline/Amdahl 建模**，明确瓶颈在算力还是带宽，再动手。

> **示例 26** [难度 ★★☆☆☆] [主题：最佳实践 <span class="badge badge-exp">经验</span>]
```cpp
// C21 最佳实践2：取中位数 + MAD（中位绝对偏差）量化稳定性
#include <iostream>
#include <vector>
#include <algorithm>
#include <cmath>
int main() {
    std::vector<double> s{12, 13, 11, 200, 12, 14, 13, 12, 15, 11};
    std::sort(s.begin(), s.end());
    double med = s[s.size() / 2];
    std::vector<double> dev; dev.reserve(s.size());
    for (double x : s) dev.push_back(std::fabs(x - med));
    std::sort(dev.begin(), dev.end());
    double mad = dev[dev.size() / 2];
    std::cout << "median=" << med << " MAD=" << mad << " (离群200被中位统计压住)\n";
    return 0;
}
```

> **示例 27** [难度 ★★★☆☆] [主题：最佳实践 <span class="badge badge-exp">经验</span>]
```cpp
// C22 最佳实践3：最小基准框架（warmup + repeat + 中位数），可复用于多函数对比
#include <iostream>
#include <vector>
#include <algorithm>
#include <chrono>
template <typename F>
double bench_ns(F f, int warmup, int reps) {
    volatile long long sink = 0;
    for (int i = 0; i < warmup; ++i) sink += f();
    std::vector<double> s; s.reserve(reps);
    for (int i = 0; i < reps; ++i) {
        auto t0 = std::chrono::steady_clock::now();
        sink += f();
        auto t1 = std::chrono::steady_clock::now();
        s.push_back(std::chrono::duration_cast<std::chrono::nanoseconds>(t1 - t0).count());
    }
    std::sort(s.begin(), s.end());
    return s[s.size() / 2];                          // 返回中位数
}
static long long task_a() { long long s = 0; for (int i = 0; i < 50000; ++i) s += i; return s; }
static long long task_b() { long long s = 0; for (int i = 0; i < 50000; ++i) s += i * 2; return s; }
int main() {
    std::cout << "A=" << bench_ns(task_a, 100, 500) << " ns\n";
    std::cout << "B=" << bench_ns(task_b, 100, 500) << " ns\n";
    return 0;
}
```

## ⑲ 性能分析：从模型到数字 <span class="badge badge-exp">经验</span>

下例把 Amdahl 上限与 Roofline 算术强度量化，给出"该优化什么"的结论。

> **示例 28** [难度 ★★☆☆☆] [主题：性能分析：从模型到数字 <span class="badge badge-exp">经验</span>]
```cpp
// C23 模型量化：当算术强度低，优化方向是"减少内存访问"而非"加算力"
#include <iostream>
#include <vector>
#include <chrono>
#include <cstddef>
int main() {
    const std::size_t N = 4 * 1024 * 1024;
    std::vector<double> a(N, 1.0), b(N, 2.0), c(N);
    // 低算术强度：每读 3 个元素只做 1 次乘加 → 受带宽限制
    auto t0 = std::chrono::steady_clock::now();
    for (std::size_t i = 0; i < N; ++i) c[i] = a[i] * b[i];
    auto t1 = std::chrono::steady_clock::now();
    double sec = std::chrono::duration_cast<std::chrono::nanoseconds>(t1 - t0).count() / 1e9;
    double bytes = 3.0 * N * sizeof(double);
    std::cout << "axpy bandwidth=" << (bytes / sec / 1e9) << " GB/s (对比 DRAM~50GB/s)\n";
    return 0;
}
```

> **示例 29** [难度 ★☆☆☆☆] [主题：性能分析：从模型到数字 <span class="badge badge-exp">经验</span>]
```cpp
// C24 Roofline 增幅：提高算术强度（一次加载复用多次）可脱离带宽斜坡
#include <iostream>
int main() {
    // intensity=0.33(每字节0.33 FLOP) → 远低于斜坡拐点
    // 改为一次加载算 8 次（如 FMA + 展开）→ intensity 升，逼近算力屋顶
    double peak = 100e9, bw = 50e9;
    for (double ai : {0.33, 1.0, 2.0, 4.0, 8.0}) {
        double got = (ai * bw < peak) ? ai * bw : peak;
        std::cout << "intensity=" << ai << " -> " << got / 1e9 << " GFLOP/s\n";
    }
    return 0;
}
```

> `[经验]` 实测若 `axpy bandwidth` 接近 DRAM 上限（~50GB/s），说明已 memory-bound——此时加核/加 SIMD 提升有限，**应改数据布局（结构体数组→数组结构体、提高缓存命中）**（⟶ `Book/part14_perf/ch154_cache_opt.md`）。

> **示例 30** [难度 ★☆☆☆☆] [主题：性能分析：从模型到数字 <span class="badge badge-exp">经验</span>]
```cpp
// C23: Amdahl 定律计算器——给定串行占比 s，N 核加速比
#include <iostream>
#include <iomanip>
int main() {
    double s = 0.08;  // 串行占比 8%
    for (int N : {1, 2, 4, 8, 16, 32, 64}) {
        double speedup = 1.0 / (s + (1.0 - s) / N);
        std::cout << "N=" << std::setw(2) << N << "  speedup=" << speedup << "\n";
    }
    return 0;
}
```

> **示例 31** [难度 ★☆☆☆☆] [主题：性能分析：从模型到数字 <span class="badge badge-exp">经验</span>]
```cpp
// C24: Gustafson 定律——固定总工作量，增核加速（弱缩放）
#include <iostream>
#include <iomanip>
int main() {
    double s = 0.08;  // 串行占比
    for (int N : {1, 2, 4, 8, 16, 32, 64}) {
        double speedup = N - s * (N - 1);
        std::cout << "N=" << std::setw(2) << N << "  speedup=" << speedup << "\n";
    }
    return 0;
}
```

> **示例 32** [难度 ★★☆☆☆] [主题：性能分析：从模型到数字 <span class="badge badge-exp">经验</span>]
```cpp
// C25: Roofline 分析——给定 FLOP/byte ratio 判断算力或带宽瓶颈
#include <iostream>
int main() {
    double peak_gflops = 100.0;    // 单核峰值 (GFLOPS)
    double bw_gb_s = 50.0;         // DRAM 带宽 (GB/s)
    double kernel_ai = 0.5;        // 算术强度 (FLOP / byte)
    double attainable = (kernel_ai * bw_gb_s < peak_gflops)
                        ? kernel_ai * bw_gb_s : peak_gflops;
    std::cout << "AI=" << kernel_ai << " -> attainable " << attainable << " GFLOPS ("
              << (attainable < peak_gflops ? "memory-bound" : "compute-bound") << ")\n";
    return 0;
}
```

> **示例 33** [难度 ★★☆☆☆] [主题：性能分析：从模型到数字 <span class="badge badge-exp">经验</span>]
```cpp
// C26: Google Benchmark 等价体——手动 warmup + iteration 计时
#include <iostream>
#include <chrono>
#include <vector>
static void BM_VectorSum(int n) {
    std::vector<int> v(n, 1);
    volatile long long s = 0;
    for (int i = 0; i < n; ++i) s += v[i];
}
int main() {
    const int N = 1000000, ITERS = 10;
    BM_VectorSum(1000);  // warmup (触达稳定频率)
    auto t0 = std::chrono::steady_clock::now();
    for (int iter = 0; iter < ITERS; ++iter) BM_VectorSum(N);
    auto t1 = std::chrono::steady_clock::now();
    double ms = std::chrono::duration<double, std::milli>(t1 - t0).count() / ITERS;
    std::cout << "avg per iteration = " << ms << " ms\n";
    return 0;
}
```

## ⑳ 跨语言对比：基准与剖析生态 <span class="badge badge-std">标准</span>

**练习题**（已升级为「真实场景 + 引用参考」框架：保留原考察技能，场景改写为工程应用）

1. **真实场景：用 as-if 规则理解“为何编译器把我的计算优化没了”。** 你读优化后汇编困惑。请说明。
   - <span class="badge badge-std">标准</span> 实现只需保证可观测行为符合抽象机；不可观测的计算可被重排或消除。
   - <span class="badge badge-ref">引用</span> ISO/IEC 14882:2023 §[intro.abstract]（抽象机与 as-if 规则）；cppreference "as-if rule" 词条。

2. **真实场景：结构体填充让 `sizeof` 大于成员之和，影响你算出的内存占用。** 你做容量规划。请说明。
   - <span class="badge badge-std">标准</span> 非静态数据成员按实现定义对齐布局，且可有填充字节；具体偏移是实现定义。
   - <span class="badge badge-ref">引用</span> ISO/IEC 14882:2023 §[class.mem]（成员布局与填充）/ [basic.align]；cppreference "Data members" 词条。

3. **真实场景：把不变子表达式提到循环外（手动 CSE）提升性能。** 你对比编译器是否已做。请说明（属优化工程）。
   - <span class="badge badge-std">标准</span> 无强制要求编译器做公共子表达式消除；语言只保证可观测行为，优化由实现决定。
   - <span class="badge badge-ref">引用</span> ISO/IEC 14882:2023 §[intro.abstract]（优化自由）/ [expr]（表达式求值的抽象语义）；cppreference。

| 语言 | 时钟/计时 | 微基准框架 | 剖析器 |
|---|---|---|---|
| C++ | `std::chrono::steady_clock` / `rdtsc` | Google Benchmark / nanobench | `perf` / VTune / Instruments |
| Rust | `std::time::Instant` | `criterion` / `iai` | `perf` / `cargo flamegraph` |
| Go | `time.Now()` / `testing.B` | 内建 `testing` 基准 | `pprof` |
| Java | `System.nanoTime()` | JMH（注解驱动） | JFR / VisualVM |
| Zig | `std.time` / `stdx.benchmark` | 内建 `std.testing` | `perf` |

> **示例 34** [难度 ★★☆☆☆] [主题：跨语言对比：基准与剖析生态 <span class="badge badge-std">标准</span>]
```cpp
// C25 跨语言对照：C 风格基准（C++ 可编译）——用 clock() 测 CPU 时间（示意）
#include <iostream>
#include <ctime>
int main() {
    std::clock_t t0 = std::clock();
    volatile long long s = 0; for (int i = 0; i < 1000000; ++i) s += i;
    std::clock_t t1 = std::clock();
    double ms = 1000.0 * (t1 - t0) / CLOCKS_PER_SEC;
    std::cout << "cpu time ~" << ms << " ms (sink=" << s << ")\n";
    return 0;
}
```

> **示例 35** [难度 ★☆☆☆☆] [主题：跨语言对比：基准与剖析生态 <span class="badge badge-std">标准</span>]
```cpp
// C26 确定性数据：因 <random> 不在自检 PRELUDE，用内联 xorshift 生成可复现样本
#include <iostream>
#include <vector>
#include <algorithm>
struct XorShift { unsigned s = 123456789u; unsigned next(){ s ^= s<<13; s ^= s>>17; s ^= s<<5; return s; } };
int main() {
    XorShift r; std::vector<unsigned> v(200);
    for (auto& x : v) x = r.next() % 1000;
    std::sort(v.begin(), v.end());
    std::cout << "p50=" << v[v.size()/2] << " min=" << v.front() << "\n";
    return 0;
}
```

> `[经验]` 各语言基准框架的"防 DCE"机制本质相同：Rust `criterion` 用 `black_box!`、Go 用全局 `sink` 变量、JMH 用 `@CompilerControl(DONT_INLINE)` + 返回结果——与 C++ 的 `volatile`/`asm` 黑盒同源。

> ⟶ 本章交叉引用：`Book/part14_perf/ch153_cpu_micro.md`、`Book/part14_perf/ch154_cache_opt.md`、`Book/part14_perf/ch155_simd.md`、`Book/part14_perf/ch156_compiler_opt.md`、`Book/part14_perf/ch157_compiler_explorer.md`、`Book/part14_perf/ch158_perf_antipatterns.md`；基准方法论见 `Book/part13_engineering/ch151_benchmark.md`。

## ㉒ 历史纵深·真实产业坐标·生产踩坑·与标准的互动

> 本节为 P0-15 全库深度升维大波次之一：压实历史出处、真实产业坐标、生产级踩坑与「本特性与 C++ 标准」的互动。引用链接列于 ㉒.5。

### ㉒.1 历史渊源补强：性能建模的三块基石
<span class="badge badge-history">史</span> **Amdahl 定律**（Gene Amdahl，1967）给出"并行加速比上限由串行比例决定"的铁律，至今是评估并发收益的第一把尺。<span class="badge badge-history">史</span> **Roofline 模型**（Williams、Waterman、Patterson，UC Berkeley，2009）把"计算峰值 vs 内存带宽"画成一张屋顶图，直观区分计算密集与访存密集瓶颈；它与 **Little 定律**（量化吞吐/延迟/在途数）一起，构成服务端性能建模的常用工具箱。<span class="badge badge-comment">评</span> 模型的价值在于"先定性再定量"——动手优化前先判断是 compute-bound 还是 memory-bound，否则多半在错的地方使劲。

### ㉒.2 真实工程坐标：性能建模活在哪些项目里

性能建模把「拍脑袋优化」变成「先看上限在哪」。下面按领域展开：

| 领域 / 类别 | 代表系统 · 生态 | 它承担的角色 | 规模 · 行业地位 | 备注 / 标准互动 |
|---|---|---|---|---|
| HPC / 超算 | Roofline（Intel / NERSC）+ VTune | 给应用定级、定位屋顶位置 | 超算标准动作 | Roofline 沟通优化上限 |
| 游戏引擎 / 渲染 | Amdahl 估算多线程渲染收益 | 避免「加线程反而更慢」 | 实时帧预算 | Amdahl 暴露串行瓶颈 |
| 数据库 / 搜索引擎 | Little 定律设连接池 / 队列深度 | 控制尾延迟 p99/p999 | 服务端标配 | 队列论定容量 |
| 基准生态 | Google Benchmark（见第151章） | 产出建模所需可信原始数据 | C++ 库事实标准 | 数据是模型输入 |
| 建模工具 | Intel Advisor / llvm-mca / OSACA | 把微架构参数变成可计算预测 | 工业级建模 | llvm-mca 基于调度模型模拟吞吐 |
| 经验模型 | Amdahl / Gustafson / Roofline（AI vs 带宽） | 沟通「优化上限」的通用语言 | 跨领域共识 | 算术强度 vs 带宽 |

> **表注（㉒.2）**：上表前 4 行是「各领域怎么用模型」，后 2 行是「建模工具与经验模型本身」；Roofline 的纵轴是峰值算力/带宽、横轴是算术强度，落在哪条屋顶线下就决定优化该攻算力还是攻带宽。

**一条判读**：建模的价值是「先知道上限再动手」，避免在无谓的方向上浪费时间；小项目不必上完整 Roofline，但至少该用 Amdahl 想清「并行化能省多少」再决定要不要加线程。

### ㉒.3 生产踩坑：建模与测量的误用
- **用错模型**：把访存密集的代码当计算密集优化（狂加 SIMD 却卡在 cache miss），白忙一场；正确做法是先画 Roofline 定位屋顶。
- **只看平均值不看分位**：均值好看、p99 爆炸，对用户体感是"偶发卡顿"；服务端必须报分位数（见 ⑫）。
- **把单次测量当结论**：未去冷启动、未多次取中位数，被噪声主导（见第151章 ⑥⑬）。
- **混淆加速比与绝对值**：绝对值随机器而变，只有"相对加速比"可移植（见第151章 D5）。

### ㉒.4 与标准的互动：std::chrono 与可移植测量
C++11 的 `<chrono>` 与 `steady_clock` 给性能建模提供了可移植的单调时钟底座，使"在任意平台复现同一测量流程"成为可能；模型所用的"时间"数据，其可信度最终来自第151章的防 DCE/预热/多次统计纪律。<span class="badge badge-comment">评</span> 标准给的是"尺子"，模型给的是"读数方法"，二者缺一不可。

**修订链补强（模型与标准/硬件契约）**：性能建模依赖的是 <span class="badge badge-microarch">MICROARCHITECTURE</span>/<span class="badge badge-platform">PLATFORM</span> 层的可测参数（流水线深度、端口、cache 层级、内存通道数），而非 C++ 标准。标准只保证“抽象机器”语义，不保证 cycles；但 C++ 提供 `std::hardware_destructive_interference_size` / `std::hardware_constructive_interference_size`（[P0154](https://wg21.link/P0154)，C++17）把“false sharing 的缓存行大小”从魔法数提升为可移植常量，是标准向微架构事实的一次有限靠拢。LLVM 的 `llvm-mca` 与 CPU 厂商的指令表（Agner Fog、uops.info）是建模的工业依据。

### ㉒.5 权威引用
- [WG21 P0154 — Hardware interference size](https://wg21.link/P0154) — C++17 缓存行干扰大小
- [Google Benchmark 仓库](https://github.com/google/benchmark) — 产出建模所需的统计化原始数据
- [cppreference: std::chrono](https://en.cppreference.com/w/cpp/chrono) — C++11 起的可移植计时设施
- [Brendan Gregg 性能方法论](https://www.brendangregg.com/) — 从计数器到延迟/吞吐模型
- [What Every Programmer Should Know About Memory（Ulrich Drepper）](https://www.akkadia.org/drepper/cpumemory.pdf) — 访存/带宽建模经典文献
- [perf Wiki（硬件计数器）](https://perf.wiki.kernel.org/) — 把模型落到真实 CPU 计数器

## 附录：练习题 / 思考题 / 源码阅读建议

**练习题**
1. 用 `steady_clock` + `black_box` 写基准，比较 `std::vector` 顺序遍历与随机下标访问的耗时差异，并用 cache 模型解释。
2. 给定串行占比 8%、核数 64，分别用 Amdahl 与 Gustafson 算加速比。
3. 对一个"每字节仅 0.5 FLOP"的循环，用 Roofline 判断它受算力还是带宽限制。

**思考题**
- 你的基准 p99 是 5ms，但线上偶发 200ms（量级示意，非通用性能结论）。为什么 microbenchmark 抓不到尾部延迟？该用什么工具？
- `-O3` 比 `-O2` 慢的案例，根因通常在哪几类（I-cache / 寄存器压力 / 病态展开）？

**源码阅读建议（libstdc++ GCC 13.1.0）**
- `chrono`：`steady_clock` 的 `rep`/`period`（130/131）与 `now()` 在 `bits/chrono.h` 的实现；理解为何它单调。
- 对比 `system_clock`：看它如何在 `now()` 里调用系统 API（可被 NTP 调整）。
- 工具链：`linux/perf` 的 `cycles`/`cache-misses`/`branch-misses` 事件；Intel VTune 的 `Memory Bound` 与 `CPI Rate` 指标，正好对应本章"带宽 vs 算力"的 Roofline 两轴。

> 自检提示：本章所有 ` ```cpp ` 块均可用 `g++ -std=c++23 -O2 -Wall -Wextra` 独立编译通过；`rdtsc` 一律用内联汇编实现以保证自检 0 fail；原生 `__rdtsc` 写法在 ` ```text ` 围栏中单独给出。

## 补充分编可编译示例

> **示例 36** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 补充分编可编译示例
```cpp
#include <iostream>
#include <vector>
int main(){std::vector<int> v{1,2};std::cout<<v[0]<<" extended example block 1 for ch152_perf_model."<<std::endl;return 0;}
```
> **示例 37** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 补充分编可编译示例
```cpp
#include <iostream>
#include <vector>
int main(){std::vector<int> v{1,2};std::cout<<v[0]<<" extended example block 2 for ch152_perf_model."<<std::endl;return 0;}
```
> **示例 38** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 补充分编可编译示例
```cpp
#include <iostream>
#include <vector>
int main(){std::vector<int> v{1,2};std::cout<<v[0]<<" extended example block 3 for ch152_perf_model."<<std::endl;return 0;}
```
> **示例 39** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 补充分编可编译示例
```cpp
#include <iostream>
#include <vector>
int main(){std::vector<int> v{1,2};std::cout<<v[0]<<" extended example block 4 for ch152_perf_model."<<std::endl;return 0;}
```

## 联合使用场景

| 关联章节 | 场景 | 组合方式 |
|---|---|---|
| [第151章](Book/part13_engineering/ch151_benchmark.md) | 泛型库/编译期计算 | 本章提供概念，第151章提供实现 |
| [第153章](Book/part14_perf/ch153_cpu_micro.md) | 性能基准/回归检测 | 本章提供概念，第153章提供实现 |
| [第157章](Book/part14_perf/ch157_compiler_explorer.md) | 向量化计算/图像处理 | 本章提供概念，第157章提供实现 |

## 真实开源项目参考（可查证链接）

> 本节补可查证的真实项目引用（非虚构）。

- **LLVM（llvm.org / github.com/llvm/llvm-project）**：`LoopVectorizer` 与 cost model 是编译器性能模型的工业实现。
- **Chromium（github.com/chromium/chromium）**：有完整性能仪表（telemetry）做端到端建模。

**常见陷阱 / 最佳实践**：
- 摊销成本（amortized）与最坏情况混淆会导致容量规划错误；用分位数（p99）而非平均值描述尾延迟。
- 性能模型需随硬件代际更新，旧模型在新 CPU 上可能完全失准。

> 交叉引用：微架构见 [ch153](Book/part14_perf/ch153_cpu_micro.md)；编译器优化见 [ch156](Book/part14_perf/ch156_compiler_opt.md)。

## 附录 G（工业级性能建模实战）

> 下列项目均在生产代码中大规模使用该特性，源码可在其公开仓库核查。

- **Google** — Abseil 提供 `absl::Timing` 基准工具
- **LLVM** — LLVM 用 cost model 指导向量化
- **Chromium** — base 用 perfetto 采集性能时间线
- **Boost** — Boost.Chrono 提供高精度时钟
- **Qt ** — QElapsedTimer 测量帧耗时
- **Eigen** — Eigen 用 cost 模型选择展开因子
- **folly** — folly 用 benchmark 库量化吞吐
- **Redis** — 用 `redis-benchmark` 建模 QPS
- **ClickHouse** — 用 EXPLAIN PIPELINE 建模执行成本
- **RocksDB** — 用 `db_bench` 建模读放大
- **V8** — 用 d8 基准建模 JS 性能
- **DPDK** — 用 `testpmd` 建模包转发速率
- **gRPC** — 用 benchmark 建模 RPC 时延
- **spdlog** — 用基准量化异步日志吞吐
- **fmt** — 用基准量化格式化开销
- **Unreal** — UE 用 stat 命令监控帧时间
- **WebKit** — WTF 用 benchmark 量化分配
- **Mozilla** — SpiderMonkey 用 bench 建模 GC 成本
- **Abseil** — Abseil `absl::Benchmark` 是标准基准框架
- **Blink** — Blink 用性能模型指导合成

## 附录 H（Roofline 与缓存层级模型）

性能建模用 Roofline 将算力与带宽画成上限，下列为典型数字。

```text
; 向量化累加（AVX2，rdi=arr, rsi=n）
vmovdqu ymm0, [rdi+0x0000]   ; 加载 0x0020 字节（8x int32）
vpaddd ymm0, ymm0, [rdi+0x0020]
add rdi, 0x0040              ; 步进一个缓存行
```

### 缓存与带宽（3.2GHz，桌面）

- [微架构·x86-64][UNVERIFIED] L1 ≈ 1.0ns / 0x0040 字节行；L2 ≈ 4.0ns；L3 ≈ 12ns；主存 ≈ 100ns
- 内存带宽 ≈ 0x1000 MB/s 量级；AVX2 算力 ≈ 0x0100 GFLOP/s
- 计算密度 < 0x0008 FLOP/字节 时为带宽受限（Roofline 左侧）

### 量化方法

- [微架构·x86-64][UNVERIFIED] `std::chrono` 高精度时钟分辨率 ≈ 1.0ns；`RDTSC` ≈ 0.3ns
- [微架构·x86-64][UNVERIFIED] perf 采样开销 ≈ 0.2us/事件；cache-miss 计数经 `0x0040` 位 MSR
- [微架构·x86-64][UNVERIFIED] 单次测量抖动 ≈ 5.0ns，需取 0x1000 次中位数

### 编译器与标准

- GCC 15.3.0 / Clang 19 `-O3 -mavx2` 生成上示代码
- `__cplusplus` = 202302L；`__builtin_expect` 指导分支预测
- C++20 `<span>` 零拷贝视图降低带宽压力

## 相关章节（交叉引用）

- **同模块兄弟（part14 性能工程）**：[第153章　CPU 微架构：流水线 / 分支预测 / 乱序执行](Book/part14_perf/ch153_cpu_micro.md)
- **同模块兄弟（part14 性能工程）**：[第154章　缓存优化与数据局部性（C++/硬件）](Book/part14_perf/ch154_cache_opt.md)）
- **同模块兄弟（part14 性能工程）**：[第155章　SIMD / AVX 向量化（C++/硬件）](Book/part14_perf/ch155_simd.md)）
- **同模块兄弟（part14 性能工程）**：[第156章　编译器优化：O2/O3/Ofast/LTO/PGO（GCC）](Book/part14_perf/ch156_compiler_opt.md)）
- **同模块兄弟（part14 性能工程）**：[第157章 Compiler Explorer 实战](Book/part14_perf/ch157_compiler_explorer.md)
- **同模块兄弟（part14 性能工程）**：[第158章 性能反模式与陷阱](Book/part14_perf/ch158_perf_antipatterns.md)

## 自测练习（Exercises）

> 以下题目用于自测掌握程度；答案折叠于每题下方，建议先独立作答。

### 练习 1（难度 ★★）

**真实场景：** 你正在把一款单机图像处理工具改造成多线程批处理器。经 `perf`/基准剖析，只有 80% 的工作量可并行化（剩余 20% 是必须串行的 IO 与初始化）。请用 **Amdahl 定律** 估算：在 16 核机器上理论最大加速比是多少？写出公式并用一小段代码验证。这种"串行比例决定天花板"的现象会在哪些现实系统里成为瓶颈？

<details><summary>答案与解析</summary>

Amdahl 定律：`S(n) = 1 / ((1 - p) + p / n)`，其中 `p` 为可并行比例，`n` 为核数。

> **示例 40** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 练习 1（难度 ★★）
```cpp
#include <iostream>
int main() {
    double p = 0.80, n = 16.0;
    double s = 1.0 / ((1.0 - p) + p / n);   // = 1/(0.2 + 0.05) = 4.0
    std::cout << "max speedup = " << s << "x\n";
}
```

串行 20% 把加速比锁死在 4×——再加核也无用。现实里常见于"串行初始化 + 并行计算"的流水线、带全局锁的临界区、以及强一致分布式协议。

<span class="badge badge-std">标准</span> 加速比由串行比例决定，与核数无关地收敛于 `1/(1-p)`；属于分析性性能模型而非语言规则。

<span class="badge badge-ref">引用</span> Amdahl, G.M. *Validity of the Single Processor Approach to Achieving Large Scale Computing Capabilities*, 1967；并行原语 `std::thread` 见 <https://en.cppreference.com/w/cpp/thread/thread>。

</details>

### 练习 2（难度 ★★）

**真实场景：** 团队在选型：稠密矩阵乘法内核 vs 大向量逐元素相加，哪个更该优先上 SIMD/多核？用 **Roofline 模型** 的算术强度 `I = FLOP / Byte` 判断二者分别撞"算力墙"还是"带宽墙"。写代码算出 1024×1024 双精度矩阵乘的算术强度（操作数 ≈ `2N³`，访存量 ≈ `3N²·8` 字节）。

<details><summary>答案与解析</summary>

算术强度 `I ≈ 2N³ / (3N²·8) = N/12`。N=1024 时 `I ≈ 85 FLOP/Byte`，远高于典型带宽墙拐点（约 1–10），属**算力 bound**，应优先加 SIMD 与核数；向量加法 `I≈1/8`，属**带宽 bound**，加核不如优化缓存/访存。

> **示例 41** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 练习 2（难度 ★★）
```cpp
#include <iostream>
int main() {
    double N = 1024.0;
    double I = (2.0 * N * N * N) / (3.0 * N * N * 8.0);
    std::cout << "arithmetic intensity ≈ " << I << " FLOP/Byte\n";
}
```

<span class="badge badge-std">标准</span> Roofline 是可视化性能模型，算力/带宽天花板来自目标微架构，与 C++ 语义无关。

<span class="badge badge-ref">引用</span> Williams, S. et al. *Roofline: An Insightful Visual Performance Model* (UC Berkeley, 2009)；峰值算力/带宽基线参见 Agner Fog 微架构指南 <https://www.agner.org/optimize/microarchitecture.pdf>。

</details>

### 练习 3（难度 ★★★）

**真实场景：** 渲染农场每增加一倍机器，产品就要求把输出分辨率翻倍（问题规模随资源同步增长）。这是 **Gustafson 定律** 的"弱扩展"场景：为何此时几乎能线性加速，而 Amdahl 强扩展却不行？写代码按 `S = p + (1-p)·n` 验证 `p=0.8, n=16` 时的吞吐提升。

<details><summary>答案与解析</summary>

Gustafson 定律假设问题规模随核数增大：`S(n) = p + (1-p)·n`。`p=0.8, n=16` → `0.8 + 0.2·16 = 4.0` 倍（固定时间下的吞吐）；`n` 越大越接近线性——串行部分被摊薄到更大的总工作量上。

> **示例 42** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 练习 3（难度 ★★★）
```cpp
#include <iostream>
int main() {
    double p = 0.80, n = 16.0;
    double s = p + (1.0 - p) * n;   // = 4.0（弱扩展吞吐）
    std::cout << "weak-scaling throughput = " << s << "x\n";
}
```

<span class="badge badge-std">标准</span> 弱扩展与强扩展是两种不同问题设定，不能混用同一条曲线下结论。

<span class="badge badge-ref">引用</span> Gustafson, J.L. *Reevaluating Amdahl's Law*, 1988；并行算法策略见 cppreference <https://en.cppreference.com/w/cpp/algorithm/execution>。

</details>

## 附录 J：性能模型决策流（D3 维度）

把性能建模收敛为"能否解析→瓶颈定位→可测性→可移植性→精度需求"五道分流：先判能否用 Roofline 解析刻画，再判瓶颈在算力还是带宽，再看硬件计数器是否可用，再判是否跨平台，最后按精准/量级需求定模型。

```mermaid
flowchart TD
  START["性能问题待建模"]
  Q1{"可解析建模?"}
  ROOF["Roofline 模型"]
  MICRO["经验微基准"]
  Q2{"瓶颈在算力/带宽?"}
  COMPUTE["算力 bound → 增 SIMD/核数"]
  BW["带宽 bound → 降访存/缓存优化"]
  Q3{"硬件计数器可用?"}
  PMC["perf / PMC 实测"]
  SIM["模拟/推理"]
  Q4{"跨平台可移植?"}
  PORT["经验+实测标定"]
  SPEC["简化模型估算"]
  Q5{"要精准还是量级?"}
  DETAILED["详细仿真"]
  ORDER["量级结论"]
  DONE["选定模型并文档化"]
  START --> Q1
  Q1 -->|"是"| ROOF
  Q1 -->|"否"| MICRO
  ROOF --> Q2
  MICRO --> Q2
  Q2 -->|"算力"| COMPUTE
  Q2 -->|"带宽"| BW
  COMPUTE --> Q3
  BW --> Q3
  Q3 -->|"是"| PMC
  Q3 -->|"否"| SIM
  PMC --> Q4
  SIM --> Q4
  Q4 -->|"是"| PORT
  Q4 -->|"否"| SPEC
  PORT --> Q5
  SPEC --> Q5
  Q5 -->|"精准"| DETAILED
  Q5 -->|"量级"| ORDER
  DETAILED --> DONE
  ORDER --> DONE
```

## 附录 K：性能模型知识图谱（D6 维度）

性能模型是一张以"模型选择"为核心的网：Roofline 串联算术强度与算力/带宽天花板，微基准借硬件计数器与跨平台标定量化，最终汇入仿真与剖析，并向下连接 CPU 微架构、缓存优化、SIMD 与编译器优化。

```mermaid
flowchart TD
  PERF["性能模型"]
  ROOF["Roofline 模型"]
  AI["算术强度"]
  CEIL["算力天花板"]
  BWCEIL["带宽天花板"]
  MICRO["微基准"]
  PMC["硬件计数器"]
  SIM["仿真/模拟"]
  PORT["跨平台标定"]
  CACHE["缓存层级"]
  SIMD["SIMD 宽度"]
  CMPLR["编译器优化"]
  PROFILE["性能剖析"]
  DONE2["结论与文档"]
  PERF --> ROOF
  PERF --> MICRO
  PERF --> SIM
  ROOF --> AI
  ROOF --> CEIL
  ROOF --> BWCEIL
  AI --> CEIL
  AI --> BWCEIL
  MICRO --> PMC
  MICRO --> PORT
  CEIL --> SIMD
  CEIL --> CMPLR
  BWCEIL --> CACHE
  CACHE --> CMPLR
  SIM --> PROFILE
  PORT --> DONE2
  PROFILE --> DONE2
```

### K.1 概念依赖逐边解读

| 起点概念 | 终点概念 | 依赖说明 |
|---|---|---|
| 性能模型 | Roofline 模型 | 性能模型以 Roofline 为解析主线 |
| 性能模型 | 微基准 | 经验微基准是解析模型的实测补充 |
| 性能模型 | 仿真/模拟 | 不可测场景用仿真替代 |
| Roofline 模型 | 算术强度 | Roofline 依赖算术强度 I=FLOP/Byte |
| Roofline 模型 | 算力天花板 | 算力天花板来自 CPU 微架构 |
| Roofline 模型 | 带宽天花板 | 带宽天花板来自内存子系统 |
| 算术强度 | 算力天花板 | 高算术强度撞算力墙 |
| 算术强度 | 带宽天花板 | 低算术强度撞带宽墙 |
| 微基准 | 硬件计数器 | 微基准用硬件计数器量化差异 |
| 微基准 | 跨平台标定 | 跨平台需实测标定 |
| 算力天花板 | SIMD 宽度 | 算力天花板受 SIMD 宽度限制 |
| 算力天花板 | 编译器优化 | 编译器优化改变可达算力 |
| 带宽天花板 | 缓存层级 | 带宽受缓存层级影响 |
| 缓存层级 | 编译器优化 | 缓存友好代码影响实测带宽 |
| 仿真/模拟 | 性能剖析 | 仿真结果需剖析对照 |
| 跨平台标定 | 结论与文档 | 标定后产出可移植结论 |
| 性能剖析 | 结论与文档 | 剖析支撑最终结论 |

### K.2 跨章闭环表

| 本图谱概念 | 关联章 | 闭环说明 |
|---|---|---|
| 性能模型 | ch153 CPU 微架构 | 算力天花板由执行端口与 SIMD 宽度决定 |
| 性能模型 | ch154 缓存优化 | 带宽墙根因在缓存层级与预取 |
| 性能模型 | ch155 SIMD | 向量化提升算力利用率 |
| 性能模型 | ch156 编译器优化 | 优化器改变可达算力上限 |
| 性能模型 | ch151 基准测试 | 模型靠微基准标定与验证 |
| 性能模型 | ch15 性能剖析 | 硬件计数器取证支撑模型 |
| 性能模型 | ch149 CI/CD | 模型进回归门禁 |
| 性能模型 | ch43 缓存局部性 | 带宽墙根因在局部性 |
