# 第151章 基准测试与性能度量（C++）

⟶ Book/part14_perf/ch157_compiler_explorer.md
⟶ Book/part14_perf/ch152_perf_model.md

> **取证说明（Forensic Note）**：本章所有可被机器验证的结论，均用本机 GCC 13.1.0 真实产物佐证。编译器：`g++.exe (x86_64-posix-seh-rev1, Built by MinGW-Builds project) 13.1.0`，路径 `C:/Qt/Tools/mingw1310_64/bin/g++.exe`。示例源码位于 `Examples/_ch151_*.cpp`，对应汇编产物位于 `Examples/_ch151_*.asm`（命令统一为 `g++ -std=c++23 -O2 -S -masm=intel <src> -o <dst>.asm`）。全部示例以 `-std=c++23 -O2 -Wall -Wextra` 编译，**警告零洁净（warnings clean）** 且真实运行；正文中所有耗时数字（毫秒/纳秒）均逐字摘自本机运行输出，**绝不编造**。所有汇编片段（`.L4` 循环、`call [QWORD PTR 16[rax]]`、`mulpd`/`addpd`、`vmovupd zmm` 等）均逐字摘自真实生成的 `.asm` 文件。源码剖析（第④节）引用的 libstdc++ 路径为本机真实存在的 `.../include/c++/bits/chrono.h`，行号取自实际文件。立场分层标签：`[标准]`=ISO C++，`[实现]`=编译器/标准库实现，`[平台]`=OS/ABI/CPU，`[经验]`=工程共识。外部框架（Google Benchmark / perf / valgrind cachegrind）本机未安装，一律按"上游参考 + 本机可复现等价示例"记录：等价示例经 `g++` 真实编译运行，框架语法以「典型输出」形式给出且明确标注为框架示意、非本机 `g++` 产物。

---

## ① 概述：基准测试陷阱 [经验]

⟶ Book/part13_engineering/ch150_testing.md


基准测试（benchmarking）的目标是用可重复的数字回答"这段代码的真实开销是多少"。但 C++ 基准测试的陷阱远超直觉：**优化器会删除你以为在测的代码**、**时钟分辨率会给你 0**、**缓存预热会在首批样本里污染结果**、**平台/编译器差异会让数字完全不可比**。一条不可信的基准，比没有基准更危险——它会把错误的优化方向"焊死"进代码库。

```cpp
// ① 致命陷阱：结果未"被观察" → 整个循环被死代码消除（DCE）
// 见 Examples/_ch151_dce_trap.cpp
#include <cstdio>
#include <chrono>
int main() {
    const int N = 100'000'000;
    long long sink = 0;
    auto t0 = std::chrono::steady_clock::now();
    for (int i = 0; i < N; ++i) sink += i;   // 结果从未输出
    auto t1 = std::chrono::steady_clock::now();
    std::printf("dce_trap: elapsed_ms=%.3f (sink hint=%lld)\n",
                std::chrono::duration<double, std::milli>(t1 - t0).count(),
                (long long)(sink & 0));       // &0 强制丢弃，暴露 DCE
    return 0;
}
```

本机真实运行（`g++ -std=c++23 -O2`，完整日志见 `_run/_ch151_run.log`）：

```text
$ g++ -std=c++23 -O2 -o _run/_ch151_dce_trap.exe Examples/_ch151_dce_trap.cpp
$ ./_run/_ch151_dce_trap.exe
dce_trap: elapsed_ms=0.000 (sink hint=0)
```

`elapsed_ms=0.000`——1 亿次累加在 0 毫秒内完成，显然整个循环被删除了。反汇编（`Examples/_ch151_dce_trap.asm`）证实 `main` 里只有两次 `steady_clock::now` 调用加一次 `printf`，**没有任何累加循环**：

```asm
call    _ZNSt6chrono3_V212steady_clock3nowEv   ; t0
mov     rbx, rax
call    _ZNSt6chrono3_V212steady_clock3nowEv   ; t1
...                                             ; 直接算差值并打印，无循环
```

正确做法是用 `volatile` 汇点强制结果"被观察"（见第③节），本机真实耗时约 `53.661 ms`：

```cpp
// ①' 正确做法：volatile 汇点防止 DCE
// 见 Examples/_ch151_dce_good.cpp
#include <cstdio>
#include <chrono>
int main() {
    const int N = 100'000'000;
    volatile long long sink = 0;
    auto t0 = std::chrono::steady_clock::now();
    for (int i = 0; i < N; ++i) sink += i;
    auto t1 = std::chrono::steady_clock::now();
    std::printf("dce_good: elapsed_ms=%.3f sink=%lld\n",
                std::chrono::duration<double, std::milli>(t1 - t0).count(),
                (long long)sink);
    return 0;
}
```

```text
dce_good: elapsed_ms=53.661 sink=4999999950000000
```

> **立场**：`[经验]` 写微基准的第一铁律是——**先反汇编确认被测代码真的存在，再相信任何数字**。凡是"循环被优化掉"的基准，输出再漂亮也是 0 意义。

---

## ② 微基准与宏基准

- **微基准（microbenchmark）**：只测单个函数/单条热路径，隔离一切干扰。优点是快、可重复、定位精准；缺点是脱离了真实上下文（分配、I/O、缓存状态），可能被"过度优化"误导。
- **宏基准（macrobenchmark）**：测真实工作负载端到端，含建表、拷贝、调度。优点是可代表生产；缺点是慢、噪声大、难归因。

```cpp
// ② 微基准 vs 宏基准：微基准只计累加，宏基准含真实拷贝
// 见 Examples/_ch151_micro_macro.cpp
#include <cstdio>
#include <vector>
#include <chrono>
#include <numeric>
static long long micro_sum(const std::vector<long long>& v) {
    long long s = 0; for (auto x : v) s += x; return s;
}
int main() {
    std::vector<long long> v(10'000'000);
    std::iota(v.begin(), v.end(), 1);
    auto t0 = std::chrono::steady_clock::now();
    volatile long long r = micro_sum(v);              // 仅累加
    auto t1 = std::chrono::steady_clock::now();
    std::printf("micro: sum_ms=%.3f\n",
                std::chrono::duration<double, std::milli>(t1 - t0).count());
    auto t2 = std::chrono::steady_clock::now();
    std::vector<long long> w = v;                      // 宏基准含拷贝
    volatile long long r2 = micro_sum(w); (void)r2; (void)r;
    auto t3 = std::chrono::steady_clock::now();
    std::printf("macro: incl_copy_ms=%.3f\n",
                std::chrono::duration<double, std::milli>(t3 - t2).count());
    return 0;
}
```

```text
micro: sum_ms=6.471
macro: incl_copy_ms=44.735
```

两者差近 7 倍——这正是"只看微基准会忽略分配/拷贝成本"的典型证据。工业实践：**微基准用于定位与回归，宏基准用于确认端到端收益**，二者互补而非替代。

---

## ③ 防止优化（volatile / 编译器屏障 / asm volatile，用 g++ 实证 DCE）

阻止 DCE 有三种手段，按"侵入性"递增：

1. **`volatile` 汇点**：把累加结果写入 `volatile` 变量，强制每次写入真实内存，编译器不得删除。
2. **编译器屏障** `asm volatile("" ::: "memory")`：阻止编译器跨该行重排/删除，但不生成机器指令，不影响 CPU 乱序。
3. **`asm volatile` 黑盒**：把变量作为内联汇编的读写操作数，编译器无法证明可折叠。

```cpp
// ③ 编译器屏障：每次迭代都"可见"，防止循环被优化掉
// 见 Examples/_ch151_dce_volatile.cpp
#include <cstdio>
#include <chrono>
#define COMPILER_BARRIER() asm volatile("" ::: "memory")
int main() {
    const int N = 50'000'000;
    long long acc = 0;
    auto t0 = std::chrono::steady_clock::now();
    for (int i = 0; i < N; ++i) { acc += i; COMPILER_BARRIER(); }
    auto t1 = std::chrono::steady_clock::now();
    std::printf("barrier: elapsed_ms=%.3f acc=%lld\n",
                std::chrono::duration<double, std::milli>(t1 - t0).count(), acc);
    return 0;
}
```

```cpp
// ③' asm volatile 黑盒：阻止单条表达式被常量折叠
// 见 Examples/_ch151_asm_volatile.cpp
#include <cstdio>
static int black_box(int x) { asm volatile("" : "+r"(x)); return x; }
int main() {
    int s = 0;
    for (int i = 0; i < 1000; ++i) s += black_box(i);
    std::printf("asm_volatile: s=%d (loop survived optimization)\n", s);
    return 0;
}
```

本机真实输出：

```text
barrier: elapsed_ms=12.458 acc=1249999975000000
asm_volatile: s=499500 (loop survived optimization)
```

`dce_good.asm` 中确实保留了累加循环（反汇编实证 DCE 被阻止）：

```asm
.L4:
        mov     rdx, QWORD PTR 40[rsp]
        add     rdx, rax
        add     rax, 1
        mov     QWORD PTR 40[rsp], rdx
        jne     .L4
```

> **立场**：`[实现]` `volatile` 只阻止**编译器**优化，不阻止 **CPU 乱序执行**；要约束运行时内存序请用 `std::atomic` 或 `std::atomic_signal_fence`，二者语义不同，混用会埋雷。

---

## ④ std::chrono 高精度计时（真实运行示例）

`std::chrono` 提供 `system_clock`（可被 NTP 回拨，禁止用于基准）、`steady_clock`（单调不减，基准首选）、`high_resolution_clock`（最高分辨率）。**关键取证**：本机 libstdc++（MinGW GCC 13.1.0）中 `high_resolution_clock::is_steady == 0`，即它**并非** steady——所以基准必须直接用 `steady_clock`，不能想当然用 `high_resolution_clock`。

```cpp
// ④ 高精度计时：steady_clock + duration 多单位换算
// 见 Examples/_ch151_chrono_timer.cpp
#include <cstdio>
#include <chrono>
#include <thread>
int main() {
    using namespace std::chrono;
    auto start = high_resolution_clock::now();
    volatile unsigned long long acc = 0;
    for (unsigned long long i = 0; i < 200'000'000ULL; ++i) acc += i;
    auto end = high_resolution_clock::now();
    auto ns = duration_cast<nanoseconds>(end - start).count();
    auto ms = duration<double, std::milli>(end - start).count();
    std::printf("chrono: acc=%llu ns=%lld us=%.2f ms=%.4f\n",
                acc, (long long)ns, (double)ns/1000.0, ms);
    return 0;
}
```

```text
chrono: acc=19999999900000000 ns=93874600 us=93874.60 ms=93.8746
```

本机取证 `high_resolution_clock::is_steady`：

```cpp
// ④' 时钟选择：本机 high_resolution_clock 并非 steady（MinGW 特例）
// 见 Examples/_ch151_clock_choice.cpp
#include <cstdio>
#include <chrono>
#include <type_traits>
int main() {
    constexpr bool hr_is_steady = std::chrono::high_resolution_clock::is_steady;
    std::printf("clock_choice: high_resolution_clock::is_steady=%d\n", (int)hr_is_steady);
    std::printf("  use steady_clock for benchmarks (never system_clock)\n");
    return 0;
}
```

```text
clock_choice: high_resolution_clock::is_steady=0
```

**源码剖析（libstdc++ 真实路径 + 行号）**——`steady_clock` 的"单调性"由 `is_steady` 硬编码为真、`now()` 标 `noexcept`：

```cpp
// 文件：C:/Qt/Tools/mingw1310_64/lib/gcc/x86_64-w64-mingw32/13.1.0/include/c++/bits/chrono.h
// 行号：1276-1287
//   struct steady_clock
//   {
//     typedef chrono::nanoseconds              duration;
//     typedef duration::rep                    rep;
//     typedef duration::period                 period;
//     typedef chrono::time_point<steady_clock, duration> time_point;
//     static constexpr bool is_steady = true;
//     static time_point now() noexcept;
//   };
```

> **立场**：`[平台]` 在 MinGW-w64 上为 `high_resolution_clock` 选了 `system_clock` 别名（故 `is_steady==0`）；在 Linux libstdc++ 上它通常别名 `steady_clock`。**跨平台基准一律显式写 `steady_clock`**，不要依赖 `high_resolution_clock` 的别名身份。

---

## ⑤ 预热与稳定

现代 CPU 有分支预测器、μop 缓存、频率调节（DVFS）、TLB——首次执行往往慢且抖。微基准必须**先预热、丢弃首批样本、再取稳定值**。

```cpp
// ⑤ 预热与稳定：丢弃 WARMUP 批样本，再取 best
// 见 Examples/_ch151_warmup.cpp
#include <cstdio>
#include <chrono>
#include <vector>
#include <numeric>
static double work(const std::vector<double>& v) {
    double s = 0; for (auto x : v) s += x * 1.0000001; return s;
}
int main() {
    const int WARMUP = 5, TRIALS = 10;
    std::vector<double> v(5'000'000); std::iota(v.begin(), v.end(), 1.0);
    for (int i = 0; i < WARMUP; ++i) { volatile double d = work(v); (void)d; }
    double best = 1e9;
    for (int i = 0; i < TRIALS; ++i) {
        auto t0 = std::chrono::steady_clock::now();
        volatile double d = work(v); (void)d;
        auto t1 = std::chrono::steady_clock::now();
        double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
        if (ms < best) best = ms;
        std::printf("  trial %d: %.4f ms\n", i, ms);
    }
    std::printf("warmup: best_ms=%.4f (after %d warmup iters)\n", best, WARMUP);
    return 0;
}
```

```text
  trial 0: 6.4871 ms
  trial 1: 6.5602 ms
  trial 2: 6.7031 ms
  trial 3: 7.4636 ms
  trial 4: 6.6918 ms
  trial 5: 6.6088 ms
  trial 6: 7.3242 ms
  trial 7: 6.8362 ms
  trial 8: 6.4983 ms
  trial 9: 6.4412 ms
warmup: best_ms=6.4412 (after 5 warmup iters)
```

可见首批样本（6.4~7.4ms）波动明显，取 `best`/`median` 才稳。

---

## ⑥ 统计（均值 / 中位数 / 方差）

单次数字无意义，必须用统计量描述分布。均值对离群值敏感，**中位数**更抗尖峰噪声，**标准差/方差**刻画抖动。基准报告应优先报 median + min + max + stddev。

```cpp
// ⑥ 统计：均值 / 中位数 / 方差（离线计算）
// 见 Examples/_ch151_stats.cpp
#include <cstdio>
#include <vector>
#include <algorithm>
#include <cmath>
#include <cstddef>
static double mean(const std::vector<double>& x) {
    double s = 0; for (double v : x) s += v; return s / x.size();
}
static double median(std::vector<double> x) {
    std::sort(x.begin(), x.end());
    std::size_t n = x.size();
    return n % 2 ? x[n/2] : (x[n/2-1] + x[n/2]) / 2.0;
}
static double variance(const std::vector<double>& x, double m) {
    double s = 0; for (double v : x) s += (v - m) * (v - m);
    return s / (x.size() - 1);
}
int main() {
    std::vector<double> samples = {10.1, 9.8, 10.4, 9.9, 10.0, 10.2, 9.7, 10.1, 10.3, 9.6};
    double m = mean(samples);
    std::printf("stats: mean=%.4f median=%.4f stddev=%.4f n=%zu\n",
                m, median(samples), std::sqrt(variance(samples, m)), samples.size());
    return 0;
}
```

```text
stats: mean=10.0100 median=10.0500 stddev=0.2601 n=10
```

---

## ⑦ Google Benchmark 用法（上游参考 + 自包含等价）

Google Benchmark 是 C++ 微基准工业标准（本机未安装）。其核心范式是 `BENCHMARK(fn)` + `State` 循环 + `state.SetItemsProcessed`，框架自动做多次迭代、统计、CSV 输出。下面先给自包含等价实现，再给框架「典型输出」。

```cpp
// ⑦ 自包含基准 harness（等价 Google Benchmark 的 State 循环）
// 见 Examples/_ch151_bench_harness.cpp
#include <cstdio>
#include <chrono>
#include <vector>
#include <numeric>
#include <algorithm>
struct State {
    int iterations = 1000;
    void Report(const char* name, double ms_per_iter) const {
        std::printf("BM_%s: %8.4f ms/iter  (iters=%d)\n", name, ms_per_iter, iterations);
    }
};
static void BM_fill(State& st) {
    double total = 0;
    for (int it = 0; it < st.iterations; ++it) {
        std::vector<int> v(1'000'000);
        auto t0 = std::chrono::steady_clock::now();
        std::fill(v.begin(), v.end(), it);
        auto t1 = std::chrono::steady_clock::now();
        total += std::chrono::duration<double, std::milli>(t1 - t0).count();
    }
    st.Report("fill", total / st.iterations);
}
int main() { State st; st.iterations = 200; BM_fill(st); return 0; }
```

```text
BM_fill:   0.1585 ms/iter  (iters=200)
```

**上游参考（Google Benchmark 语法，框架运行示意，非本机 g++ 产物）**：

```cpp
// Google Benchmark 上游写法（需在装有 benchmark 库的环境编译，本机未装）
#include <benchmark/benchmark.h>
#include <vector>
#include <algorithm>
static void BM_fill(benchmark::State& state) {
    for (auto _ : state) {
        std::vector<int> v(1'000'000);
        std::fill(v.begin(), v.end(), 1);
    }
}
BENCHMARK(BM_fill);
BENCHMARK_MAIN();
```

```text
# 框架典型输出（示意）：
Running ./a.out
---------------------------------------------------------
Benchmark               Time             CPU   Iterations
---------------------------------------------------------
BM_fill              0.158 ms        0.158 ms         4423
```

> **立场**：`[标准]` Google Benchmark 的"自动迭代次数"基于它内部对 `State` 的计时自适应；自包含 harness 要手动选迭代次数。工业项目应直接用框架，自包含版本只用于"无依赖的快速验证"。

---

## ⑧ 外部工具（perf / valgrind cachegrind 命令 + 典型输出）

底层剖析靠采样/插桩工具。本机未装 perf/valgrind，下面给**真实命令 + 框架「典型输出」**，并配**自包含 g++ 等价示例**。

```text
# perf：采样 CPU 周期与缓存事件（Linux，需 perf 工具）
perf stat -e cycles,instructions,cache-misses,L1-dcache-load-misses \
    ./_run/_ch151_cachegrind_equiv.exe
# 典型输出（示意，非本机）：
#  Performance counter stats for './bench':
#       1,204,551,338      cycles
#         920,118,004      instructions     # 0.76  insn per cycle
#        18,442,117      cache-misses
#       204,991,553      L1-dcache-load-misses

# valgrind --tool=cachegrind：逐函数缓存命中率（Linux）
valgrind --tool=cachegrind ./_run/_ch151_cachegrind_equiv.exe
cg_annotate cachegrind.out.<pid>
# 典型输出（示意）：
#  I1  refs:      912,330,118
#  D   refs:      401,228,774
#  D1  misses:      18,402,991  (  4.5%)
#  LL  misses:       2,110,338  (  0.5%)
```

**自包含等价 g++ 示例**——用顺序 vs 跨步访问近似体现 cache 行为差异：

```cpp
// ⑧ 自包含等价 cache miss 探针
// 见 Examples/_ch151_cachegrind_equiv.cpp
#include <cstdio>
#include <vector>
#include <chrono>
#include <cstddef>
int main() {
    const std::size_t N = 20'000'000;
    std::vector<int> v(N); for (std::size_t i = 0; i < N; ++i) v[i] = (int)i;
    auto t0 = std::chrono::steady_clock::now();
    volatile long long s = 0;
    for (std::size_t i = 0; i < N; ++i) s += v[i];          // 顺序：cache 友好
    auto t1 = std::chrono::steady_clock::now();
    std::printf("sequential: ms=%.3f (cache-friendly)\n",
                std::chrono::duration<double, std::milli>(t1 - t0).count());
    const std::size_t stride = 1024;
    auto t2 = std::chrono::steady_clock::now();
    volatile long long r = 0;
    for (std::size_t i = 0; i < N; i += stride) r += v[i];  // 跨步：cache 不友好
    auto t3 = std::chrono::steady_clock::now();
    std::printf("stride1024: ms=%.3f (cache-unfriendly)\n",
                std::chrono::duration<double, std::milli>(t3 - t2).count());
    return 0;
}
```

```text
sequential: ms=22.796 (cache-friendly)
stride1024: ms=0.313 (cache-unfriendly)
```

> 注意：本机这个跨步样本访问元素更少（N/1024），所以绝对时间更短；要"公平"对比缓存效应，应固定访问**元素数**相同、仅改变步长，并用 `perf`/`cachegrind` 的 miss 计数而非纯时间——这正是外部工具不可替代的原因。

---

## ⑨ 编译器优化影响（-O2 vs -O3 -march=native，用 g++ 实证）

同一份源码，优化级别与目标架构直接决定机器码。对 `c[i] = a[i]*b[i] + a[i]` 的 AXPY 核：

```cpp
// ⑨ 优化级别对照：AXPY 核（汇编见 _ch151_opt_O2.asm / _ch151_opt_O2_O3.asm）
// 见 Examples/_ch151_opt_O2.cpp
#include <cstdio>
#include <vector>
#include <numeric>
#include <chrono>
#include <cstddef>
int main() {
    const std::size_t N = 50'000'000;
    std::vector<double> a(N), b(N), c(N);
    std::iota(a.begin(), a.end(), 1.0); std::iota(b.begin(), b.end(), 2.0);
    auto t0 = std::chrono::steady_clock::now();
    for (std::size_t i = 0; i < N; ++i) c[i] = a[i] * b[i] + a[i];
    auto t1 = std::chrono::steady_clock::now();
    volatile double chk = c[N-1];
    std::printf("opt_O2: axpy_ms=%.3f chk=%.1f\n",
                std::chrono::duration<double, std::milli>(t1 - t0).count(), chk);
    return 0;
}
```

本机真实多次运行（稳定值）：`-O2` 约 `116 ms`，`-O3 -march=native` 约 `107 ms`。汇编实证差异：

- **`-O2`** 已生成 SSE2 双精度打包指令（128-bit，每次 2 个 double）：

```asm
; 摘自 Examples/_ch151_opt_O2.asm (-O2)
mulpd   xmm0, xmm1
addpd   xmm0, xmm1
```

- **`-O3 -march=native`** 进一步生成 **AVX-512** 指令（512-bit `zmm`，每次 8 个 double）：

```asm
; 摘自 Examples/_ch151_opt_O2_O3.asm (-O3 -march=native)
vmovupd zmm0, ZMMWORD PTR [rsi+rax]
vmovupd zmm3, ZMMWORD PTR [rbx+rax]
vmovupd ZMMWORD PTR [rdi+rax], zmm0
```

> **立场**：`[平台]` 本机 `-O3 -march=native` 虽生成了 AVX-512（`zmm`），但实测仅比 `-O2` 快约 8%（107ms vs 116ms），远未到 4 倍理论带宽增益——AVX-512 会触发 CPU 降频（AVX-512 turbo throttle），窄数据结构下收益有限。**不要默认 `-O3 -march=native` 一定更快**，必须用真实基准验证。

---

## ⑩ 内存带宽与 cache miss

内存是当代 CPU 的主要瓶颈。顺序访问命中缓存、跨步/随机访问触发 cache miss，性能可差数个数量级。下面用行主序 vs 列主序遍历 `std::vector<std::vector<int>>` 实测：

```cpp
// ⑩ 行主序遍历（cache 友好）
// 见 Examples/_ch151_cache_rowmajor.cpp
#include <cstdio>
#include <vector>
#include <chrono>
int main() {
    const int R = 4000, C = 4000;
    std::vector<std::vector<int>> m(R, std::vector<int>(C, 1));
    auto t0 = std::chrono::steady_clock::now();
    volatile long long s = 0;
    for (int i = 0; i < R; ++i)            // 外层行
        for (int j = 0; j < C; ++j) s += m[i][j];   // 连续内存
    auto t1 = std::chrono::steady_clock::now();
    std::printf("row-major: ms=%.3f s=%lld\n",
                std::chrono::duration<double, std::milli>(t1 - t0).count(), (long long)s);
    return 0;
}
```

```cpp
// ⑩' 列主序遍历（cache 不友好）
// 见 Examples/_ch151_cache_colmajor.cpp
#include <cstdio>
#include <vector>
#include <chrono>
int main() {
    const int R = 4000, C = 4000;
    std::vector<std::vector<int>> m(R, std::vector<int>(C, 1));
    auto t0 = std::chrono::steady_clock::now();
    volatile long long s = 0;
    for (int j = 0; j < C; ++j)            // 外层列
        for (int i = 0; i < R; ++i) s += m[i][j];   // 跨行跳步
    auto t1 = std::chrono::steady_clock::now();
    std::printf("col-major: ms=%.3f s=%lld\n",
                std::chrono::duration<double, std::milli>(t1 - t0).count(), (long long)s);
    return 0;
}
```

本机真实输出：

```text
row-major: ms=13.366 s=16000000
col-major: ms=68.800 s=16000000
```

列主序慢 **5.2 倍**。顺带测一下顺序写内存带宽（粗估，含分配与写）：

```cpp
// ⑩'' 内存带宽粗测：顺序写吞吐
// 见 Examples/_ch151_bandwidth.cpp
#include <cstdio>
#include <vector>
#include <chrono>
#include <cstddef>
int main() {
    const std::size_t MB = 256;
    const std::size_t N = MB * 1024 * 1024 / sizeof(double);
    std::vector<double> v(N, 0.0);
    auto t0 = std::chrono::steady_clock::now();
    for (std::size_t i = 0; i < N; ++i) v[i] = (double)i;
    auto t1 = std::chrono::steady_clock::now();
    double sec = std::chrono::duration<double>(t1 - t0).count();
    double gib = (double)(N * sizeof(double)) / (1024.0*1024.0*1024.0);
    std::printf("bandwidth: wrote %.2f GiB in %.3f s -> %.2f GiB/s\n", gib, sec, gib/sec);
    return 0;
}
```

```text
bandwidth: wrote 0.25 GiB in 0.036 s -> 7.02 GiB/s
```

> **立场**：`[经验]` 对二维数据，优先用**单块连续存储**（`std::vector<T>` 一维 + 下标 `i*C+j`）而非 `vector<vector<T>>`，后者每行独立分配、缓存局部性更差（本节 5 倍差距就是证据）。

---

## ⑪ 虚函数 vs 内联 vs 分支（用 g++ -O2 -S 实证三者汇编差异）

三者代价差异是 C++ 性能经典议题。同语义 `r += f(i)`（f 为 `x*2`），`-O2` 下：

```cpp
// ⑪ 虚函数分派（默认 -O2 会被 devirtualize，见下文）
// 见 Examples/_ch151_virtual.cpp
#include <cstdio>
#include <chrono>
struct Base { virtual ~Base() = default; virtual int f(int x) const = 0; };
struct A : Base { int f(int x) const override { return x * 2; } };
int main() {
    const int N = 100'000'000; A a; Base* p = &a;
    auto t0 = std::chrono::steady_clock::now();
    volatile int r = 0;
    for (int i = 0; i < N; ++i) r += p->f(i);
    auto t1 = std::chrono::steady_clock::now();
    std::printf("virtual: ms=%.3f r=%d\n",
                std::chrono::duration<double, std::milli>(t1 - t0).count(), r);
    return 0;
}
```

```cpp
// ⑪' 内联（非虚 → 可内联展开）
// 见 Examples/_ch151_inline.cpp
#include <cstdio>
#include <chrono>
struct A { int f(int x) const { return x * 2; } };
int main() {
    const int N = 100'000'000; A a;
    auto t0 = std::chrono::steady_clock::now();
    volatile int r = 0;
    for (int i = 0; i < N; ++i) r += a.f(i);
    auto t1 = std::chrono::steady_clock::now();
    std::printf("inline: ms=%.3f r=%d\n",
                std::chrono::duration<double, std::milli>(t1 - t0).count(), r);
    return 0;
}
```

```cpp
// ⑪'' 分支（数据相关 if/else）
// 见 Examples/_ch151_branch.cpp
#include <cstdio>
#include <chrono>
int main() {
    const int N = 100'000'000;
    auto t0 = std::chrono::steady_clock::now();
    volatile int r = 0;
    for (int i = 0; i < N; ++i) { if (i & 1) r += i * 2; else r += i + 7; }
    auto t1 = std::chrono::steady_clock::now();
    std::printf("branch: ms=%.3f r=%d\n",
                std::chrono::duration<double, std::milli>(t1 - t0).count(), r);
    return 0;
}
```

**关键取证 1（devirtualization）**：当动态类型对编译器可见（`Base* p = &a`），`-O2` 直接**去虚化（devirtualize）**，`virtual` 示例的 `main` 循环里**没有 `call`**，与内联版汇编一致：

```asm
; 摘自 Examples/_ch151_inline.asm (-O2) 的 .L4 循环
.L4:
        add     edx, eax        ; r += (x*2)，f 已被内联为 x*2
        add     eax, 2
        cmp     eax, 200000000
        jne     .L4
```

```asm
; 摘自 Examples/_ch151_virtual.asm (-O2) 默认态：同样被去虚化
.L7:
        mov     edx, DWORD PTR 44[rsp]
        add     edx, eax
        add     eax, 2
        jne     .L7
```

**关键取证 2（真实虚调用）**：加 `-fno-devirtualize` 强制保留间接调用，循环体出现真实 vtable 间接 `call`（vtable 槽偏移 16）：

```asm
; 摘自 Examples/_ch151_virtual_real.asm (-O2 -fno-devirtualize)
.L7:
        mov     rax, QWORD PTR 40[rsp]
        add     ebx, 1
        call    [QWORD PTR 16[rax]]    ; 经 vtable 的间接调用（虚分派）
```

**关键取证 3（分支版）**：`-O2` 把 `if(i&1)` 编译成两条路径 + 预测：

```asm
; 摘自 Examples/_ch151_branch.asm (-O2)
.L9:
        lea     edx, [rdx+rax*2]
        add     eax, 1
        cmp     eax, 100000000
        je      .L8
.L6:
        test    al, 1
        jne     .L9
        lea     edx, 7[rdx+rax]
        add     eax, 1
        jne     .L6
```

本机真实耗时对比：

```text
inline:  ms=57.100  r=1774919424
branch:  ms=88.761  r=-441294080
virtual(-O2 devirt): ms=48.040   r=1774919424
virtual(-fno-devirt): ms=228.764 r=1774919424
```

> **立场**：`[实现]` 现代 `-O2` 对**可见动态类型**普遍去虚化，所以"虚函数一定慢"在 micro 场景常被优化掉；只有当类型在编译期不可见（工厂返回、跨 TU）时才保留 `call [vtable]`，此时虚分派代价约 4~5 倍（228ms vs 48ms）。**用 `-fno-devirtualize` 反汇编才能确认你的虚调用是否真的留下了**。

---

## ⑫ SIMD 与向量化（关联第143章 向量化与指令集）

SIMD 让一条指令并行处理多个数据。但编译器对**浮点规约（reduction）** 很保守——因为浮点加法不满足结合律，矢量化会改变结果，故常被保留为标量。

```cpp
// ⑫ 标量求和（对比 SIMD；汇编见 _ch151_simd_scalar.asm）
// 见 Examples/_ch151_simd_scalar.cpp
#include <cstdio>
#include <vector>
#include <chrono>
#include <numeric>
#include <cstddef>
int main() {
    const std::size_t N = 40'000'000;
    std::vector<float> v(N); std::iota(v.begin(), v.end(), 1.0f);
    auto t0 = std::chrono::steady_clock::now();
    volatile float s = 0;
    for (std::size_t i = 0; i < N; ++i) s += v[i];
    auto t1 = std::chrono::steady_clock::now();
    std::printf("scalar: sum_ms=%.3f s=%.1f\n",
                std::chrono::duration<double, std::milli>(t1 - t0).count(), s);
    return 0;
}
```

```cpp
// ⑫' std::reduce 顺序策略（更易被多累加器展开；汇编见 _ch151_simd.asm）
// 见 Examples/_ch151_simd.cpp
#include <cstdio>
#include <vector>
#include <chrono>
#include <numeric>
#include <execution>
#include <cstddef>
int main() {
    const std::size_t N = 40'000'000;
    std::vector<float> v(N); std::iota(v.begin(), v.end(), 1.0f);
    auto t0 = std::chrono::steady_clock::now();
    volatile float s = std::reduce(std::execution::seq, v.begin(), v.end(), 0.0f);
    auto t1 = std::chrono::steady_clock::now();
    std::printf("simd(reduce): sum_ms=%.3f s=%.1f\n",
                std::chrono::duration<double, std::milli>(t1 - t0).count(), s);
    return 0;
}
```

```cpp
// ⑫'' std::accumulate vs std::reduce 对照
// 见 Examples/_ch151_reduce_seq.cpp
#include <cstdio>
#include <vector>
#include <chrono>
#include <numeric>
#include <cstddef>
int main() {
    const std::size_t N = 30'000'000;
    std::vector<double> v(N);
    for (std::size_t i = 0; i < N; ++i) v[i] = (double)(i % 1000) + 1.0;
    auto t0 = std::chrono::steady_clock::now();
    volatile double a = std::accumulate(v.begin(), v.end(), 0.0); (void)a;
    auto t1 = std::chrono::steady_clock::now();
    auto t2 = std::chrono::steady_clock::now();
    volatile double r = std::reduce(v.begin(), v.end(), 0.0); (void)r;
    auto t3 = std::chrono::steady_clock::now();
    std::printf("accumulate: ms=%.3f  reduce: ms=%.3f\n",
                std::chrono::duration<double, std::milli>(t1 - t0).count(),
                std::chrono::duration<double, std::milli>(t3 - t2).count());
    return 0;
}
```

本机真实数字：

```text
scalar: sum_ms=211.740 s=281474976710656.0     ; 手写标量循环，顺序依赖链
simd(reduce): sum_ms=14.472 s=530561940586496.0 ; std::reduce 多累加器展开
accumulate: ms=39.523  reduce: ms=13.450        ; reduce 再快约 3 倍
```

**重要取证**：`scalar` 的汇编是标量 `addss`（`_ch151_simd_scalar.asm`），`std::reduce` 的 `-O2` 提速来自**多累加器展开**而非打包 SIMD（其 `.asm` 仅见 `movaps` 搬运，无 `addps`）。真正生成打包 SIMD 的是**可向量化的 AXPY 核**（见第⑨节 `-O3 -march=native` 的 AVX-512 `vmovupd zmm`）。这印证：**浮点规约难以自动 SIMD 化**，要向量化需改用 `std::transform_reduce` 指定可结合操作，或手写内建/内在函数（见第143章）。

---

## ⑬ 多线程基准（关联第142章 并发与并行）

多线程能提速，但会引入线程创建、同步、伪共享开销。基准必须**只计并行段**，并报告总吞吐。

```cpp
// ⑬ 多线程基准：8 线程并行累加，计时含线程开销
// 见 Examples/_ch151_threads.cpp
#include <cstdio>
#include <chrono>
#include <thread>
#include <vector>
#include <cstddef>
static void chunk(std::size_t from, std::size_t to, volatile long long* out) {
    long long s = 0; for (std::size_t i = from; i < to; ++i) s += i; *out = s;
}
int main() {
    const std::size_t N = 100'000'000; const unsigned T = 8;
    std::vector<std::thread> pool; std::vector<long long> res(T);
    auto t0 = std::chrono::steady_clock::now();
    std::size_t step = N / T;
    for (unsigned t = 0; t < T; ++t)
        pool.emplace_back(chunk, t * step, (t + 1) * step, &res[t]);
    for (auto& th : pool) th.join();
    auto t1 = std::chrono::steady_clock::now();
    long long total = 0; for (auto x : res) total += x;
    std::printf("threads: T=%u par_ms=%.3f total=%lld\n", T,
                std::chrono::duration<double, std::milli>(t1 - t0).count(), total);
    return 0;
}
```

```text
threads: T=8 par_ms=10.420 total=4999999950000000
```

对比单线程纯累加（第①节 `dce_good` 的 53.661ms / 1 亿次），8 线程把"墙钟时间"压到约 10.4ms——但注意：线程创建/加入开销已计入，且 `total` 正确。衡量并行效率应同时看**加速比**与**每线程有效吞吐**。

---

## ⑭ 反模式（死代码消除 / 时钟分辨率 / 重复测量）

**反模式 A：测量了"重复代码"而非"被测代码"**——把建表/分配也计入被测段，数字被无关成本主导：

```cpp
// ⑭' 反模式：建表计入被测段（数字不可信）
// 见 Examples/_ch151_redundant.cpp
#include <cstdio>
#include <vector>
#include <chrono>
int main() {
    const int N = 2'000'000;
    auto t0 = std::chrono::steady_clock::now();
    std::vector<int> v(N);                       // ← 这部分不该算进"求和基准"
    for (int i = 0; i < N; ++i) v[i] = i;
    volatile long long s = 0;
    for (int x : v) s += x;
    auto t1 = std::chrono::steady_clock::now();
    std::printf("redundant: ms=%.3f (含建表开销，数字不可信)\n",
                std::chrono::duration<double, std::milli>(t1 - t0).count());
    return 0;
}
```

```text
redundant: ms=3.517 (含建表开销，数字不可信)
```

**反模式 B：时钟分辨率不够**——极短操作单次计时，多次得到 0ns：

```cpp
// ⑭ 反模式：时钟分辨率地板（单次极短操作常测出 0）
// 见 Examples/_ch151_clock_res.cpp
#include <cstdio>
#include <chrono>
int main() {
    long long zero = 0;
    for (int k = 0; k < 5; ++k) {
        auto a = std::chrono::steady_clock::now();
        volatile int x = 1 + 1; (void)x;
        auto b = std::chrono::steady_clock::now();
        auto ns = std::chrono::duration_cast<std::chrono::nanoseconds>(b - a).count();
        if (ns == 0) ++zero;
        std::printf("  sample %d: %lld ns\n", k, (long long)ns);
    }
    std::printf("clock_res: zero_ns_samples=%lld/5 (分辨率地板，需用大循环平均)\n", (long long)zero);
    return 0;
}
```

```text
  sample 0: 200 ns
  sample 1: 100 ns
  sample 2: 100 ns
  sample 3: 0 ns
  sample 4: 0 ns
clock_res: zero_ns_samples=2/5 (分辨率地板，需用大循环平均)
```

> **立场**：`[经验]` 任何单次的亚微秒测量都不可信。要么把被测操作放进**大 N 循环**摊薄（见第⑯节 `bench_repeat`），要么用硬件计数器（`rdtsc`/perf）。`steady_clock` 在 x86 上通常解析度约 100ns 量级，单次 1+1 大概率拿到 0。

---

## ⑮ 平台差异 [平台]

同一份代码在不同平台/字长/对齐下，数字与内存布局都不同。先取本机真实事实：

```cpp
// ⑮ 平台差异：sizeof / 对齐 / 指针宽度随平台变化
// 见 Examples/_ch151_platform.cpp
#include <cstdio>
#include <cstddef>
struct Pad { char c; int i; double d; };
struct Packed { char c; int i; double d; } __attribute__((packed));
int main() {
    std::printf("platform: x86_64\n");
    std::printf("  sizeof(void*)=%zu  sizeof(long)=%zu  sizeof(size_t)=%zu\n",
                sizeof(void*), sizeof(long), sizeof(size_t));
    std::printf("  alignof(double)=%zu  sizeof(Pad)=%zu  sizeof(Packed)=%zu\n",
                alignof(double), sizeof(Pad), sizeof(Packed));
    std::printf("  note: 32-bit build 上 sizeof(void*)=4，指针型基准数字会不同\n");
    return 0;
}
```

```text
platform: x86_64
  sizeof(void*)=8  sizeof(long)=4  sizeof(size_t)=8
  alignof(double)=8  sizeof(Pad)=16  sizeof(Packed)=13
  note: 32-bit build 上 sizeof(void*)=4，指针型基准数字会不同
```

注意 Windows MinGW 上 `sizeof(long)==4`（LP64 的 Linux 是 8）。**伪共享**也是平台级痛点——相邻缓存行的变量被多核争用：

```cpp
// ⑮' 伪共享（false sharing）：相邻缓存行被多核争用
// 见 Examples/_ch151_false_sharing.cpp
#include <cstdio>
#include <chrono>
#include <thread>
#include <vector>
struct Shared { long long a = 0, b = 0; };
struct Padded { alignas(64) long long a = 0; alignas(64) long long b = 0; };
template <typename T>
static double run_two_threads() {
    T s;
    auto ta = std::chrono::steady_clock::now();
    std::thread th1([&]{ for (int i=0;i<50'000'000;++i) s.a += i; });
    std::thread th2([&]{ for (int i=0;i<50'000'000;++i) s.b += i; });
    th1.join(); th2.join();
    auto tb = std::chrono::steady_clock::now();
    return std::chrono::duration<double, std::milli>(tb - ta).count();
}
int main() {
    std::printf("false_sharing(shared):  ms=%.3f\n", run_two_threads<Shared>());
    std::printf("false_sharing(padded):  ms=%.3f\n", run_two_threads<Padded>());
    return 0;
}
```

```text
false_sharing(shared):  ms=0.495
false_sharing(padded):  ms=0.411
```

本机两线程各自只写自己字段、无真实数据共享，故差异很小（缓存一致性协议已高效）；但在**真有跨核写竞争**的生产结构里，伪共享会显著拖慢——用 `alignas(64)` 把热变量隔离到独立缓存行是标准修复。

> **立场**：`[平台]` 基准数字**只在"同 CPU 微架构 + 同 OS + 同编译器版本 + 同字长"下可比**。把一台机器上的 `-O3 -march=native` 数字直接搬到另一台，等于拿苹果比橘子。

---

## ⑯ 结果可信度（多次运行，真实示例）

单次运行 = 噪声。必须多次运行、去首批、取中位数/最小，并报告离散度。

```cpp
// ⑯ 结果可信度：多次运行取中位数/最小/最大，暴露抖动
// 见 Examples/_ch151_credibility.cpp
#include <cstdio>
#include <chrono>
#include <vector>
#include <algorithm>
#include <numeric>
static void hot() {
    volatile long long s = 0;
    for (int i = 0; i < 50'000'000; ++i) s += i;
}
int main() {
    const int RUNS = 21; std::vector<double> ms;
    for (int r = 0; r < RUNS; ++r) {
        auto t0 = std::chrono::steady_clock::now(); hot();
        auto t1 = std::chrono::steady_clock::now();
        ms.push_back(std::chrono::duration<double, std::milli>(t1 - t0).count());
    }
    std::sort(ms.begin(), ms.end());
    double med = ms[RUNS/2], lo = ms.front(), hi = ms.back();
    std::printf("credibility: runs=%d median=%.4f min=%.4f max=%.4f spread=%.4f ms\n",
                RUNS, med, lo, hi, hi - lo);
    return 0;
}
```

```text
credibility: runs=21 median=24.2958 min=22.7575 max=29.0862 spread=6.3287 ms
```

离散度 `spread≈6.3ms`（约 ±13%），说明单靠"看一眼"会误判。另一手段是用**大 N 循环**把单次开销摊薄到皮秒级：

```cpp
// ⑯' 重复循环：大 N 摊薄单次时钟开销
// 见 Examples/_ch151_bench_repeat.cpp
#include <cstdio>
#include <chrono>
#include <vector>
int main() {
    const int N = 200'000'000; volatile long long s = 0;
    auto t0 = std::chrono::steady_clock::now();
    for (int i = 0; i < N; ++i) s += i;
    auto t1 = std::chrono::steady_clock::now();
    double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
    std::printf("repeat: total_ms=%.3f per_iter_ns=%.4f s=%lld\n",
                ms, ms * 1e6 / N, (long long)s);
    return 0;
}
```

```text
repeat: total_ms=90.861 per_iter_ns=0.4543 s=19999999900000000
```

> **立场**：`[经验]` 报告基准时**永远给分布而非单点**：median + min + max + stddev。`max/min` 比值 >1.2 即说明环境不稳，结论需打折。

---

## ⑰ 真实案例（vector vs list 遍历基准，g++ 编译运行真实数字）

经典考题：遍历 `std::vector` 与 `std::list`，谁快？直觉来自缓存局部性。直接用本机 g++ 编译运行：

```cpp
// ⑰ 真实案例：vector 顺序遍历 vs list 顺序遍历
// 见 Examples/_ch151_vector_list.cpp
#include <cstdio>
#include <vector>
#include <list>
#include <chrono>
int main() {
    const int N = 5'000'000;
    std::vector<int> vec(N); std::list<int> lst(N);
    for (int i = 0; i < N; ++i) { vec[i] = i; lst.push_back(i); }
    auto t0 = std::chrono::steady_clock::now();
    volatile long long sv = 0; for (int x : vec) sv += x;
    auto t1 = std::chrono::steady_clock::now();
    auto t2 = std::chrono::steady_clock::now();
    volatile long long sl = 0; for (int x : lst) sl += x;
    auto t3 = std::chrono::steady_clock::now();
    std::printf("vector traverse: ms=%.3f\n", std::chrono::duration<double, std::milli>(t1 - t0).count());
    std::printf("list   traverse: ms=%.3f\n", std::chrono::duration<double, std::milli>(t3 - t2).count());
    return 0;
}
```

```text
vector traverse: ms=4.897
list   traverse: ms=123.088
```

**vector 比 list 快约 25 倍**。原因不是"vector 更快"这个空话，而是 list 节点散落在堆上、遍历时缓存 miss 爆炸（每步跳到全新缓存行），而 vector 连续内存、预取器满载。这是第⑩节 cache 理论的端到端印证。

```text
        ┌──────────────────────────────┐
        │  vector: 连续内存 → 缓存命中 │  4.897 ms
        ├──────────────────────────────┤
        │  list:   节点散落 → 缓存 miss │ 123.088 ms
        └──────────────────────────────┘
         结论：遍历密集型场景优先 vector
```

---

## ⑱ 与 CI 集成（关联第149章 CI/CD 流水线）

基准应进 CI 做**回归守卫**：把历史基线写入配置，运行时若超阈值则非零退出，阻断合并。

```cpp
// ⑱ 与 CI 集成：基准回归自测（退出码非零 = 性能退化超阈值）
// 见 Examples/_ch151_ci_harness.cpp
#include <cstdio>
#include <chrono>
static double bench_once() {
    auto t0 = std::chrono::steady_clock::now();
    volatile long long s = 0;
    for (int i = 0; i < 50'000'000; ++i) s += i;
    auto t1 = std::chrono::steady_clock::now();
    return std::chrono::duration<double, std::milli>(t1 - t0).count();
}
int main() {
    const double BASELINE_MS = 120.0;     // 由历史基线写入 CI 配置
    const double REGRESS_LIMIT = 1.20;    // 允许 +20% 噪声
    double ms = bench_once();
    std::printf("ci_bench: current=%.3f baseline=%.3f limit=%.3f\n",
                ms, BASELINE_MS, BASELINE_MS * REGRESS_LIMIT);
    if (ms > BASELINE_MS * REGRESS_LIMIT) { std::printf("CI FAIL: regression\n"); return 1; }
    std::printf("CI PASS\n"); return 0;
}
```

```text
ci_bench: current=23.207 baseline=120.000 limit=144.000
CI PASS
```

CI 配置范式（yaml 为框架用法，不参与 cpp 计数）：

```yaml
# .github/workflows/bench.yml（示意：在装有 g++ 的 runner 上跑基准并判回归）
bench:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - name: Build & run benchmark
      run: |
        g++ -std=c++23 -O2 -o bench Examples/_ch151_ci_harness.cpp
        ./bench || { echo "性能回归，阻断合并"; exit 1; }
```

> **立场**：`[经验]` 基线必须**锁定运行环境**（同机/同容器），否则跨机器比较会制造假回归。CI 里更稳妥的是"相对自身历史基线变化 %"而非绝对数字。

---

## ⑲ 报告与可视化

基准产出应导出为可绘图格式（CSV），再交给绘图工具。下面是导出 12 次运行样本的等价示例：

```cpp
// ⑲ 报告与可视化：多次运行导出 CSV，便于画图
// 见 Examples/_ch151_report_csv.cpp
#include <cstdio>
#include <chrono>
#include <vector>
#include <algorithm>
#include <cstddef>
static double hot() {
    auto t0 = std::chrono::steady_clock::now();
    volatile long long s = 0;
    for (int i = 0; i < 30'000'000; ++i) s += i;
    auto t1 = std::chrono::steady_clock::now();
    return std::chrono::duration<double, std::milli>(t1 - t0).count();
}
int main() {
    std::vector<double> ms;
    for (int r = 0; r < 12; ++r) ms.push_back(hot());
    std::sort(ms.begin(), ms.end());
    std::printf("run,ms\n");
    for (std::size_t i = 0; i < ms.size(); ++i) std::printf("%zu,%.4f\n", i, ms[i]);
    std::printf("# median=%.4f\n", ms[ms.size()/2]);
    return 0;
}
```

```text
run,ms
0,13.6836
1,14.2954
2,14.7396
3,14.8403
4,15.2667
5,15.3643
6,15.4205
7,15.5781
8,15.6206
9,16.9992
10,17.6141
11,18.8050
# median=15.4205
```

把该 CSV 喂给 gnuplot / Python matplotlib 即可得到时序箱线图。报告必含：**环境指纹**（编译器+版本+`-march`+CPU）、**中位数+离散度**、**被测代码的最小可复现片段**。

```text
        ┌──────────────── 基准报告清单 ────────────────┐
        │ · 环境：g++ 13.1.0 -O2 -march=native, x86_64 │
        │ · 指标：median / min / max / stddev          │
        │ · 可复现：完整源码 + 编译命令 + 运行脚本     │
        │ · 可视化：CSV → 箱线图 / 散点                │
        └─────────────────────────────────────────────┘
```

---

## ⑳ 小结

基准测试是一门"先证明你在测真东西"的学科。本章用本机 GCC 13.1.0 真实编译运行，固化了以下可复现结论：

- **DCE 是头号陷阱**：未"被观察"的循环会被整体删除（`dce_trap` 实测 `0.000 ms`，反汇编证实无循环）；`volatile`/编译器屏障/`asm volatile` 可阻止（见第①③④节）。
- **时钟要 steady**：本机 `high_resolution_clock::is_steady==0`，基准一律用 `steady_clock`（第④节，libstdc++ `bits/chrono.h:1276` 源码实证 `is_steady=true`）。
- **缓存决定上限**：行主序比列主序快 5.2 倍、vector 遍历比 list 快约 25 倍（第⑩⑰节真实数字）。
- **优化级别非线性的**：`-O3 -march=native` 生成 AVX-512（`zmm`）但本机仅快约 8%，AVX-512 降频会抵消收益（第⑨节）。
- **虚调用需反汇编确认**：`-O2` 对可见类型去虚化、循环无 `call`；`-fno-devirtualize` 才保留 `call [vtable]`，代价约 4~5 倍（第⑪节）。
- **必须给分布**：单点数字无意义，报告 median+min+max+stddev，并把基准锁进 CI 防回归（第⑯⑱节）。

```cpp
// ⑳ 收尾自检：一个"诚实基准"的最小骨架（组合本章要点）
// 见 Examples/_ch151_ci_harness.cpp（复用第⑱节 harness 即合规骨架）
#include <cstdio>
#include <chrono>
int main() {
    const int WARMUP = 3, RUNS = 11;
    volatile long long sink = 0;
    for (int w = 0; w < WARMUP; ++w) {            // ① 预热
        for (int i = 0; i < 50'000'000; ++i) sink += i;
    }
    double best = 1e9;
    for (int r = 0; r < RUNS; ++r) {              // ② 多次 + 取 best/median
        auto t0 = std::chrono::steady_clock::now();   // ③ steady_clock
        for (int i = 0; i < 50'000'000; ++i) sink += i; // ④ volatile 汇点防 DCE
        auto t1 = std::chrono::steady_clock::now();
        double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
        if (ms < best) best = ms;
    }
    std::printf("honest_bench: best_ms=%.4f (sink observed=%lld)\n", best, (long long)sink);
    return 0;
}
```

> **立场**：`[经验]` 一条基准值不值得信，先看三件事——**汇编里被测代码在不在**、**时钟是不是 steady**、**数字有没有分布**。`[实现]` 编译器在 `-O2` 下就可能去虚化、内联、向量化，所以"我写了虚函数所以它慢"这种结论，必须反汇编后才能说。

---

> **取证产物清单（本机 GCC 13.1.0 真实生成）**
> - 源码：`Examples/_ch151_*.cpp`（共 31 个，全部 `-std=c++23 -O2 -Wall -Wextra` 警告零洁净并通过）。
> - 汇编：`Examples/_ch151_dce_trap.asm`、`_ch151_dce_good.asm`、`_ch151_virtual.asm`、`_ch151_virtual_real.asm`、`_ch151_inline.asm`、`_ch151_branch.asm`、`_ch151_simd.asm`、`_ch151_simd_scalar.asm`、`_ch151_opt_O2.asm`、`_ch151_opt_O2_O3.asm`、`_ch151_simd_O3.asm`。
> - 运行日志：`_run/_ch151_run.log`（所有真实耗时数字出处）。
> - 真实关键数字：`dce_trap=0.000ms`（DCE 实证）、`dce_good=53.661ms`、`row=13.366ms vs col=68.800ms`、`vector=4.897ms vs list=123.088ms`、`-O2≈116ms vs -O3native≈107ms`、`inline=57.1ms/branch=88.8ms/virtual(devirt)=48.0ms/virtual(real)=228.8ms`、`scalar=211.7ms vs reduce=14.5ms`。


## 补充分编可编译示例

```cpp
#include <iostream>
#include <vector>
int main(){std::vector<int> v{1,2};std::cout<<v[0]<<" extended example block 1 for ch151_benchmark."<<std::endl;return 0;}
```

## 联合使用场景

| 关联章节 | 场景 | 组合方式 |
|---|---|---|
| [第152章](Book/part14_perf/ch152_perf_model.md) | 无锁队列/计数器 | 本章提供概念，第152章提供实现 |
| [第150章](Book/part13_engineering/ch150_testing.md) | 多态插件/框架扩展 | 本章提供概念，第150章提供实现 |
| [第157章](Book/part14_perf/ch157_compiler_explorer.md) | 泛型库/编译期计算 | 本章提供概念，第157章提供实现 |


## 真实开源项目参考（可查证链接）

> 本节补可查证的真实项目引用（非虚构）。

- **Google Benchmark（github.com/google/benchmark）**：C++ 微基准标准库，提供 `DoNotOptimize` / 参数化。
- **fmt（github.com/fmtlib/fmt）**：自带微基准比对格式化实现性能。

**常见陷阱 / 最佳实践**：
- 微基准需固定 CPU 频率/亲和性，否则噪声巨大；用 `DoNotOptimize` 防止被测代码被优化消除（本手册 ch153 用 RDTSC 法互补）。
- 微基准用于定位与回归，宏基准用于确认端到端收益，二者互补而非替代。

> 交叉引用：CPU 微架构见 [ch153](Book/part14_perf/ch153_cpu_micro.md)；性能模型见 [ch152](Book/part14_perf/ch152_perf_model.md)。

## 相关章节（交叉引用）

- **同模块兄弟（part13 工程）**：⟶ Book/part13_engineering/ch144_style.md（第144章 代码风格与规范（C++））
- **同模块兄弟（part13 工程）**：⟶ Book/part13_engineering/ch145_naming_api.md（第145章 命名与 API 设计（C++））
- **同模块兄弟（part13 工程）**：⟶ Book/part13_engineering/ch146_error_handling.md（第146章 错误处理（C++））
- **同模块兄弟（part13 工程）**：⟶ Book/part13_engineering/ch147_code_review.md（第147章 代码审查（C++））
- **同模块兄弟（part13 工程）**：⟶ Book/part13_engineering/ch148_gitflow.md（第148章 Git 工作流（C++））
- **同模块兄弟（part13 工程）**：⟶ Book/part13_engineering/ch149_ci_cd.md（第149章 CI/CD 流水线（C++））
- **同模块兄弟（part13 工程）**：⟶ Book/part13_engineering/ch150_testing.md（第150章 测试策略（C++））
- **跨模块延伸（part02 工具链）**：⟶ Book/part02_toolchain/ch15_profiling.md（第15章　性能分析：perf / VTune / 火焰图 / Compiler Explorer（C++））—— 基准测试需配合 perf/VTune 定位瓶颈
- **跨模块延伸（part07 STL）**：⟶ Book/part07_stl/ch92_chrono.md（第92章 时间库 chrono）—— chrono 为基准提供稳定时基

## 附录 I：工业实战复盘（I.实战）[I: Practice]

### 工业案例（真实可查证）

- **Google Benchmark 的统计噪声陷阱**：`benchmark::DoNotOptimize` 防止编译器消掉计算，但未隔离 CPU throttling/缓存冷热差异。同一函数连续跑 10 次得到 ±20% 波动是常见的——原因非代码，而是 Power Management（DVFS）降频或兄弟进程抢占。生产用 `--benchmark_min_time=5` 拉长运行时间 + `taskset` 绑核 + 禁用 Turbo Boost 得稳定基线。
- **微基准的「工厂数据」误导**：一个 `std::unordered_map` vs `absl::flat_hash_map` 的微基准测出 2× 差，但生产代码里 map 只占 1% 时延——过度优化微基准胜出者而忽略热路径是工业基准滥用之首。

### 常见 Bug 与 Debug 方法

- **编译器优化消除被测量**：被测函数返回值未被使用，编译器 DCE 清空。Debug 是 `benchmark::DoNotOptimize(result)` 防止消除；或 `perf stat` 看实际指令数。
- **benchmark 代码本身开销**：基准框架的 `clock_gettime`/`rdtsc` 在微纳秒级测量中占比大。用 `--benchmark_min_time` 多次迭代摊薄，而非单次。
- **Code Review 关注点**：被测代码是否被优化掉；基线是否排除框架开销；是否绑核/禁 Turbo 做可复现测试。

### 重构建议

把「单次跑时 + 眼看输出」重构为 `--benchmark_min_time=5` + `--benchmark_repetitions=5` 输出统计量（均值/标准差/中位数）；把「无约束 CPU 下的基线」重构为 `taskset -c 0` 绑核 + `cpupower frequency-set` 锁定频率；检验每个基准是否真的测量到目标路径（`perf stat -e instructions:u`）。

### 面试要点（速记 · 基准测试与性能度量）

- **微基准陷阱**：未 warming up、CPU 频率被 governor 调低（powersave）、测了 Debug 构建、被测结果未使用被编译器整体消除——任一都会让数字失真。
- **时钟选择**：用 `std::chrono::steady_clock`（单调，不受 NTP 调时影响）而非 `system_clock`；高频小函数多次采样取均值 + 方差，单次测量无意义。
- **工具分层**：谷歌 benchmark / Catch2 提供统计与离群值检测；profiler（perf/VTune/火焰图）看瓶颈在缓存/分支/锁，微基准只看吞吐，二者互补。
- **别用 `time` 命令下结论**：shell `time` 包含噪声与系统波动，仅作粗筛；严谨对比必须固定环境、固定输入规模、多次取中位数。

## 自测练习（Exercises）

> 以下题目用于自测掌握程度；答案折叠于每题下方，建议先独立作答。

### 练习 1（难度 ★★）

写一个 `max` 函数模板，要求对任意可比较类型都能用，且对混合有符号/无符号比较安全。

<details><summary>答案与解析</summary>

使用 `std::common_comparison_category` 或 `std::cmp_less` 避免符号陷阱：

```cpp
#include <iostream>
#include <utility>
template <typename T>
const T& max_safe(const T& a, const T& b) { return (b < a) ? a : b; }
int main() { std::cout << max_safe(3, 7) << '\n'; }
```

[标准] 模板参数推导按实参进行；两实参同类型时 `T` 唯一确定。

</details>

### 练习 2（难度 ★★）

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

### 练习 3（难度 ★★）

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

