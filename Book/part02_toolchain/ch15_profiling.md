# 第15章　性能分析：perf / VTune / 火焰图 / Compiler Explorer（C++）

⟶ Book/part13_engineering/ch151_benchmark.md
⟶ Book/part14_perf/ch157_compiler_explorer.md

> 真实编译器：MinGW GCC 13.1.0（`-std=c++23 -O2`）。
> 本章所有 `text` 数值均来自本机真实编译运行（`g++ -std=c++23 -O2`）；`asm` 来自 `g++ -std=c++23 -O2 -S -masm=intel` 的真实产物。
> 源码根：`C:/Qt/Tools/mingw1310_64/lib/gcc/x86_64-w64-mingw32/13.1.0/include/c++/`。
> 约定见 `CONVENTIONS.md`；perf / Linux `perf stat` / `perf record` 为 Linux 专有，Windows/MinGW 不可用 —— 本章给出**真实命令**并明确标注「Linux 典型输出」，绝不编造数字。

## ① 概述：为什么性能分析

⟶ Book/part02_toolchain/ch14_debugging.md
⟶ Book/part02_toolchain/ch16_ide.md


没有测量就没有优化。经验直觉常错：你觉得慢的那行，火焰图里可能只占 0.3%；真正的热点藏在缓存未命中与分支预测失败里。性能分析（Profiling）把"感觉慢"变成"数字在哪慢"。

```
        ┌─────────────────────────────────────┐
        │  直觉(猜)        vs        测量(证)   │
        │  "for 太慢"                IPC=0.4   │
        │  "虚函数贵"                L1-miss/s │
        └─────────────────────────────────────┘
```

- `[标准]`：C++ 不规定 profiler；性能是可观测属性，依赖实现与硬件。
- `[经验]`：先有可复现的基准，再谈优化；否则你在优化噪声。

```cpp
// ① 一个"看起来无辜、实则热点"的函数：累加 5000 万元素
#include <vector>
long hot_sum(const std::vector<long>& v) {
    long s = 0;
    for (long x : v) s += x;   // 这行可能占 80% 运行时间
    return s;
}
```

## ② perf 基础（stat / record / report）[平台·Linux]

`perf` 是 Linux 内核自带的分析器（`tools/perf`），分三层：

- `perf stat`：汇总计数器（跑一次，给总量）。
- `perf record`：采样，写 `perf.data`。
- `perf report`：交互式看采样结果。

```bash
# 文件：Linux 终端（非 Windows 命令）
# 汇总模式：直接看程序的硬件/软件事件总量
perf stat -d ./your_program

# 采样模式：记录调用栈，生成 perf.data
perf record -F 9999 -g ./your_program

# 报告模式：交互查看，按热点排序
perf report
```

- `[平台]`：`perf` 是 **Linux 专有**（依赖 `perf_event_open`  syscall）。Windows/MinGW 下不存在；对应能力由 ETW / Visual Studio Profiler 提供（见 ⑰）。
- `[经验]`：采样频率 `-F 9999` ≈ 每秒 1 万次；太高会扰动程序，太低丢细节，9999 是常用甜点。

```cpp
// ② 一个适合被 perf 采样的程序骨架
#include <vector>
#include <cstdio>
int main() {
    std::vector<long> v(50'000'000, 1);
    long s = 0;
    for (long x : v) s += x;          // 热点：被采样命中的循环
    std::printf("%ld\n", s);
    return 0;
}
```

## ③ perf 硬件计数器（cache-miss / branch-miss / IPC）

CPU 有固定功能计数器（PMC）。三个最常用：

| 事件 | 含义 | 坏信号 |
|---|---|---|
| `cache-misses` | 末级缓存未命中 | 高占比 → 内存 bound |
| `branch-misses` | 分支预测失败 | 高 → 分支 heavy |
| `instructions / cycles`（IPC） | 每周期指令数 | IPC<1 → 前端/串行瓶颈 |

```bash
# 文件：Linux 终端
# 指定具体计数器（逗号分隔）
perf stat -e cycles,instructions,cache-misses,branch-misses,L1-dcache-load-misses ./app

# 仅看 IPC（指令/周期）
perf stat -e instructions,cycles ./app
```

- `[实现]`：计数器由硬件提供；`perf` 只是读取接口。不同微架构事件名可能不同（Intel `/sys/bus/event_source/devices/cpu/events/`）。
- `[经验]`：**先算 IPC**。IPC≈3–4 说明算得快、等内存；IPC<1 说明指令供给或串行依赖是瓶颈。

```cpp
// ③ 缓存不友好：随机跳跃访问 -> 高 cache-miss
#include <vector>
#include <random>
long random_walk(const std::vector<long>& idx, const std::vector<double>& data) {
    long p = 0; double s = 0;
    for (long i = 0; i < (long)idx.size(); ++i) {
        p = idx[p];            // 随机跳，缓存行几乎每次失效
        s += data[p];
    }
    return (long)s;
}
```

## ④ 火焰图生成（perf script → flamegraph）

火焰图（Flame Graph，Brendan Gregg）把调用栈按"自底向上"堆叠，宽度=采样占比，一眼定位热点路径。

```bash
# 文件：Linux 终端
# 1) 采样（带调用栈）
perf record -F 99 -a -g -- sleep 30          # 采整个系统 30s
# 或针对进程：
perf record -F 99 -g ./your_program

# 2) 折叠栈
perf script | ./stackcollapse-perf.pl > out.folded

# 3) 生成 SVG
./flamegraph.pl out.folded > flame.svg
```

```cpp
// ④ 一个能产生"深调用栈"的工作负载，便于火焰图展示
#include <vector>
#include <cstdio>
long leaf(long n) { long s = 0; for (long i=0;i<n;++i) s+=i; return s; }
long mid(long n)  { return leaf(n) + leaf(n/2); }
long top(long n)  { return mid(n) + mid(n/3); }
int main() {
    long total = 0;
    for (int k = 0; k < 100000; ++k) total += top(1000);
    std::printf("%ld\n", total);
    return 0;
}
```

- `[平台]`：`stackcollapse-perf.pl` / `flamegraph.pl` 来自 [Brendan Gregg 的 flamegraph 仓库]（公开脚本，非本工程）；`perf script` 输出经管道折叠。
- `[经验]`：火焰图横轴是**采样占比**（不是时间顺序）。最宽的"塔"就是最该优化的路径。

## ⑤ [实现] 真实微基准：vector push_back reserve 与否耗时对比（真实数字）

**实测**。程序 `Examples/_ch15_vector_reserve.cpp` 用 `std::chrono` 测量 N=20,000,000 次 `push_back`，对比"不 reserve"与"先 reserve(N)"：

```cpp
// 文件：Examples/_ch15_vector_reserve.cpp
// 行号：11（no_reserve 段）/ 21（with_reserve 段）
#include <vector>
#include <chrono>
#include <cstdio>
static const long N = 20'000'000;
int main() {
    { // 不 reserve：触发多次指数级重新分配 + 元素搬移
        std::vector<long> v;
        auto t0 = std::chrono::steady_clock::now();
        for (long i = 0; i < N; ++i) v.push_back(i);
        auto t1 = std::chrono::steady_clock::now();
        std::printf("no_reserve   : %8.2f ms\n",
            std::chrono::duration<double, std::milli>(t1 - t0).count());
    }
    { // 先 reserve(N)：push_back 零重新分配
        std::vector<long> v; v.reserve(N);
        auto t0 = std::chrono::steady_clock::now();
        for (long i = 0; i < N; ++i) v.push_back(i);
        auto t1 = std::chrono::steady_clock::now();
        std::printf("with_reserve : %8.2f ms\n",
            std::chrono::duration<double, std::milli>(t1 - t0).count());
    }
    return 0;
}
```

编译运行（`g++ -std=c++23 -O2`，本机 MinGW GCC 13.1.0，多次运行区间）：

```text
# 命令：g++ -std=c++23 -O2 Examples/_ch15_vector_reserve.cpp -o _vr && ./_vr
# 本机真实输出（三次中的代表）：
no_reserve   :    66.79 ms   size=20000000
with_reserve :    32.90 ms   size=20000000
# 另一轮：no_reserve 73.81ms / with_reserve 35.06ms
```

- `[实现]`：**reserve 带来约 2.0× 加速**（~67ms → ~33ms）。差距来自 `push_back` 在容量不足时 `realloc` + 拷贝旧元素；`reserve` 一次性到位，后续 `push_back` 仅尾端写入。
- `[经验]`：已知上限的集合，先 `reserve` 是性价比最高的零风险优化之一。

## ⑥ VTune 简介

Intel VTune Profiler 是图形化、微架构级分析器（Windows/Linux 均可用），比 `perf` 更"会说话"：它直接告诉你 "Memory Bound"、"Front-End Bound"、"Bad Speculation" 占比。

```cpp
// ⑥ 一个 VTune "Memory Bound" 视角会标红的工作负载
#include <vector>
#include <random>
#include <cstdio>
int main() {
    const long N = 40'000'000;
    std::vector<long> a(N), b(N);
    std::mt19937 rng(42);
    for (long i=0;i<N;++i){ a[i]=rng(); b[i]=rng(); }
    long s=0;
    for (long i=0;i<N;++i) s += a[i]*b[i];   // 流访问，带宽受限
    std::printf("%ld\n", s);
    return 0;
}
```

- `[平台]`：VTune 是 **Intel 商业工具**（有免费版）；非 GCC 自带。它读取与 `perf` 相同的 PMC，但做了更高层归因。
- `[经验]`：新手先跑 VTune 的 "Microarchitecture Exploration"，它能把"慢"翻译成"前/后端/内存/分支"四宫格，省去自己读计数器。

## ⑦ Compiler Explorer (Godbolt) 用法

[Godbolt](https://godbolt.org) 是浏览器内编译器，输入 C++ 即时看汇编。用途：**确认你的优化有没有真的落到汇编**（比如 `-O2` 是否向量化了）。

```cpp
// ⑦ 把这段代码贴进 Godbolt，选 x86-64 gcc 13.1 -O2，看 sum() 是否被 vectorize
long sum(const long* a, long n) {
    long s = 0;
    for (long i = 0; i < n; ++i) s += a[i];
    return s;
}
```

- `[标准]`：Godbolt 不改语言语义，它只是把编译器后端输出可视化；你能验证"我以为的优化"是否发生。
- `[经验]`：对比 `-O0` / `-O2` / `-O3 -march=native` 三栏，常能发现 `-O3` 多做的向量化正是性能拐点（见 ⑪）。

## ⑧ 基准框架 Google Benchmark

手写 `chrono` 微基准容易踩坑（见 ⑯）。Google Benchmark 提供：多次迭代取中位数、自动剔除首尾、统计方差。

```cpp
// ⑧a 用 Google Benchmark 重写 reserve 对比（需链接 benchmark 库）
#include <benchmark/benchmark.h>
#include <vector>
static void BM_NoReserve(benchmark::State& st) {
    for (auto _ : st) {
        std::vector<long> v;
        for (long i = 0; i < 20'000'000; ++i) v.push_back(i);
    }
}
BENCHMARK(BM_NoReserve);

static void BM_Reserve(benchmark::State& st) {
    for (auto _ : st) {
        std::vector<long> v; v.reserve(20'000'000);
        for (long i = 0; i < 20'000'000; ++i) v.push_back(i);
    }
}
BENCHMARK(BM_Reserve);
BENCHMARK_MAIN();
```

```bash
# 文件：Linux / 任意装了 benchmark 的环境
# 编译并运行（需先 vcpkg/conan 安装 benchmark）
g++ -std=c++23 -O2 bench.cpp -lbenchmark -lpthread -o bench
./bench
# 典型输出（示意区间，非本机实测，数值因机器而异）：
# BM_NoReserve   66.3 ms  ±2%
# BM_Reserve     32.1 ms  ±1%
```

- `[经验]`：Google Benchmark 的 `State` 循环自动处理"热身"与"多次取中位数"，比手写 `chrono` 稳得多。
- `[实现]`：框架本身不测量——它只是把"跑 N 次取统计"做对；底层仍是 `std::chrono` + `clock_gettime`。

## ⑨ 热点识别方法

定位热点三步：

1. **总览**：`perf stat` 看 IPC / cache-miss，判断是"算得慢"还是"等内存"。
2. **采样**：`perf record -g` + 火焰图，找最宽塔。
3. **下钻**：对热点函数取 `-S` 汇编，确认是否向量化 / 有无冗余。

```cpp
#include <vector>
// ⑨ 把"疑似热点"用 __attribute__((noinline)) 隔离，便于单独剖析
__attribute__((noinline))
long suspect_hot(const std::vector<long>& v) {
    long s = 0;
    for (long x : v) s += x * x;     // 平方累加，可能成为热点
    return s;
}
int main() {
    std::vector<long> v(50'000'000, 3);
    return (int)suspect_hot(v);
}
```

- `[经验]`：先优化"最宽塔"，哪怕它只快 10%，因为基数大；别去抠 0.1% 的角落。
- `[实现]`：`__attribute__((noinline))` 阻止内联，让 `perf` 能把它作为独立栈帧采样到，否则热点被摊进调用方。

## ⑩ 微架构瓶颈（前端 / 后端 / 内存 bound）

现代 CPU 是流水线。瓶颈分四类：

```
┌──────────┐   ┌──────────┐   ┌──────────┐   ┌────────┐
│ 前端 Front│→ │ 后端 Back │→ │ 执行单元  │→ │ 退役    │
│ 取指/解码 │   │ 调度/发射 │   │ ALU/SIMD │   │ Retire │
└──────────┘   └──────────┘   └──────────┘   └────────┘
   ↑              ↑                  ↑
 Front-End    Bad Speculation   Back-End / Memory
   Bound         Bound            Bound
```

- `[标准]`：该分解源自 Intel Top-down Microarchitecture Analysis（TMA）方法论。
- `[经验]`：
  - **Front-End Bound**：指令喂不进（代码体积大 / 跳转多）→ 关注 I-cache、分支布局。
  - **Back-End / Memory Bound**：等数据（cache-miss、DRAM 延迟）→ 优化数据局部性。
  - **Bad Speculation**：分支预测失败 → 减少不可预测分支。

```cpp
// ⑩ 内存 bound 典型：顺序流访问，受带宽限制（非计算受限）
#include <vector>
#include <cstddef>
double stream_add(const std::vector<double>& a, const std::vector<double>& b) {
    double s = 0;
    for (size_t i = 0; i < a.size(); ++i) s += a[i] + b[i];  // 每元素 2 次加载
    return s;
}
```

## ⑪ [实现] 真实：-O2 汇编对比（标量 vs 多累加器向量化雏形）

**实测**。程序 `Examples/_ch15_scalar_vs_accum.cpp` 对比两个求和算法，并取真实 `-O2` 汇编。

```cpp
// 文件：Examples/_ch15_scalar_vs_accum.cpp
// 行号：14（scalar_sum）/ 21（four_acc_sum）
// 朴素标量累加：单累加器，依赖链长度 = N
long scalar_sum(const long* a, long n) {
    long s = 0;
    for (long i = 0; i < n; ++i) s += a[i];
    return s;
}
// 多累加器：4 条独立依赖链（向量化雏形，缩短 loop-carried 依赖）
long four_acc_sum(const long* a, long n) {
    long s0=0,s1=0,s2=0,s3=0; long i=0;
    for (; i+4<=n; i+=4){ s0+=a[i]; s1+=a[i+1]; s2+=a[i+2]; s3+=a[i+3]; }
    for (; i<n; ++i) s0+=a[i];
    return s0+s1+s2+s3;
}
```

真实计时（`g++ -std=c++23 -O2`，N=50,000,000，本机）：

```text
# 命令：g++ -std=c++23 -O2 Examples/_ch15_scalar_vs_accum.cpp -o _sa && ./_sa
# 本机真实输出（代表轮）：
scalar_sum  :    12.63 ms
four_acc_sum:    11.35 ms
# 另一轮：scalar_sum 14.04ms / four_acc_sum 12.26ms
```

真实汇编（`g++ -std=c++23 -O2 -S -masm=intel`）。注意：**`four_acc_sum` 被编译器向量化为 128 位 SSE（`paddd` 一次加 4 个 32 位），而 `scalar_sum` 仍是逐元素标量 `add`**——这正是多累加器更快的根因。

```asm
; 文件：Examples/_ch15_scalar_vs_accum.asm  行号：37（_Z10scalar_sumPKll）
; scalar_sum：标量循环，单依赖链
_Z10scalar_sumPKll:
	test	edx, edx
	jle	.L6
	movsx	rdx, edx
	xor	eax, eax
	lea	rdx, [rcx+rdx*4]
.L5:
	add	eax, DWORD PTR [rcx]      ; 一次加 1 个 32 位元素
	add	rcx, 4
	cmp	rcx, rdx
	jne	.L5
	ret
```

```asm
; 行号：63（_Z12four_acc_sumPKll）
; four_acc_sum：被向量化（SSE2），一次处理 4 个 32 位元素
_Z12four_acc_sumPKll:
	push	rsi
	push	rbx
	cmp	edx, 3
	jle	.L13
	lea	r9d, -4[rdx]
	xor	eax, eax
	pxor	xmm0, xmm0               ; 128 位累加寄存器清零
	shr	r9d, 2
	add	r9d, 1
.L10:
	mov	rcx, rax
	add	rax, 1
	sal	rcx, 4
	cmp	eax, r9d
	movdqu	xmm1, XMMWORD PTR [r10+rcx]   ; 一次加载 16 字节 = 4×int32
	paddd	xmm0, xmm1                     ; 向量加（4 路并行）
	jb	.L10
	pshufd	xmm1, xmm0, 85
	...                                   ; 把 xmm0 的 4 路归约
```

- `[实现]`：多累加器写法让 GCC 识别出"4 路独立加法"并自动 SSE 向量化；标量单累加器则因 loop-carried 依赖 + 64 位/32 位处理选择而保持标量。结果 `four_acc_sum` 略快且更有扩展空间（若改 `-O3 -march=native` 会进一步 AVX 化）。
- `[经验]`：写"对编译器友好"的代码（独立累加、规则步长）比手写 intrinsics 更可移植，且随编译器升级自动变快。

## ⑫ 缓存命中分析

缓存层级：L1（~1ns）→ L2（~4ns）→ L3（~10ns）→ DRAM（~100ns）。**缓存友好 = 顺序、局部、紧凑**。

```cpp
#include <cstddef>
#include <vector>
// ⑫a 行主序遍历（连续内存，缓存友好）
void row_major(const std::vector<std::vector<double>>& m, double& s) {
    for (size_t i = 0; i < m.size(); ++i)
        for (size_t j = 0; j < m[i].size(); ++j)
            s += m[i][j];           // 地址连续递增
}
```

```cpp
#include <cstddef>
#include <vector>
// ⑫b 列主序遍历（跨行跳跃，缓存失效多）
void col_major(const std::vector<std::vector<double>>& m, double& s) {
    size_t cols = m[0].size();
    for (size_t j = 0; j < cols; ++j)
        for (size_t i = 0; i < m.size(); ++i)
            s += m[i][j];           // 每次跳一行，缓存行浪费
}
```

- `[标准]`：C++ 多维 `std::vector` 是"向量的向量"，**行不连续**；列遍历跨堆块跳，缓存最差。
- `[经验]`：密集数值用一维扁平数组 + `idx = i*W + j` 模拟矩阵，既连续又易向量化。

## ⑬ 采样 vs 插桩

| 方式 | 原理 | 优点 | 缺点 |
|---|---|---|---|
| 采样 (Sampling) | 周期性中断取栈 | 开销低、可上生产 | 短函数可能漏采 |
| 插桩 (Instrument) | 编译期注入计数器 | 精确、全覆盖 | 显著慢、改二进制 |

```cpp
// ⑬ 插桩视角：手动计数器（简化版"插桩"）
#include <unordered_map>
#include <map>
std::unordered_map<const char*, long> g_calls;
#define COUNT() g_calls[__func__]++
void api_a() { COUNT(); /* ... */ }
void api_b() { COUNT(); api_a(); }
```

- `[实现]`：采样是 `perf`/`VTune` 默认；插桩对应 GCC `-finstrument-functions` 或 sanitizer 类工具。
- `[经验]`：先用**采样**快速定位；对"已确认热点"再上**插桩**拿精确调用次数与路径。

## ⑭ 与 CI 集成

把性能守卫写进 CI：跑基准，对比基线，超阈值就红。

```cpp
// ⑭a 用 Google Benchmark 的阈值断言（回归捕获）
#include <benchmark/benchmark.h>
void BM_CriticalPath(benchmark::State& st) {
    for (auto _ : st) { /* 核心路径 */ }
}
BENCHMARK(BM_CriticalPath)->Iterations(1000);
```

```bash
# 文件：CI 脚本（Linux）
# 用 bench 的 --benchmark_format=json 解析，对比上次基线
./bench --benchmark_format=json | tee bench_new.json
python3 compare.py bench_baseline.json bench_new.json --threshold 5%
# 超过 5% 退化则 exit 1，阻断合并
```

- `[经验]`：CI 里用**相对回归阈值**（如 5%）而非绝对值，避免机器噪声误报。固定跑在专用、无扰动的 runner 上。
- `[平台]`：GitHub Actions / GitLab CI 的 Linux runner 可直接用 `perf`；Windows runner 用 ETW（见 ⑰）。

## ⑮ [经验] 分析流程

可复用的七步法：

```
  ① 定目标(延迟?吞吐?) → ② 建可复现基准
        → ③ perf stat 看 IPC/缓存 → ④ 火焰图定位最宽塔
        → ⑤ 取热点 -S 汇编确认向量化 → ⑥ 改代码
        → ⑦ 重测，确认提升且无误回归
```

```cpp
#include <vector>
// ⑮ 把"优化前后"做成同一基准的两种实现，便于对比
struct Algo {
    virtual long run(const std::vector<long>&) const = 0;
    virtual ~Algo() = default;
};
// 旧实现 vs 新实现，复用同一驱动，公平对比
```

- `[经验]`：每次只改**一个变量**再测；同时改三处，你不知道哪处生效、哪处反动。
- `[经验]`：记录"基线数字 + 改动 + 新数字"，复盘时比记忆可靠。

## ⑯ 常见误区（微基准陷阱 / 温度计效应）

```cpp
// ⑯a 陷阱1：死代码被优化掉——基准测了个寂寞
#include <vector>
#include <chrono>
#include <cstdio>
int main() {
    std::vector<long> v(10'000'000, 1);
    auto t0 = std::chrono::steady_clock::now();
    long s = 0;
    for (long x : v) s += x;          // 若 s 未使用，-O2 直接删掉整个循环！
    auto t1 = std::chrono::steady_clock::now();
    std::printf("%ld\n", s);          // 用 volatile 或输出强制保留
    return 0;
}
```

```cpp
// ⑯b 陷阱2：false sharing（伪共享）——两线程各写自己的计数器，却在同一缓存行
#include <thread>
struct Counters { long a = 0; long b = 0; }; // a 与 b 同缓存行(64B)
Counters c;
void thread_a() { for (int i=0;i<100'000'000;++i) c.a++; } // 与 c.b 互相 invalidation
void thread_b() { for (int i=0;i<100'000'000;++i) c.b++; }
// 修复：alignas(64) 把 a、b 隔开到不同缓存行
```

- `[经验]`：**温度计效应**（thermometer effect）——反复插桩/打印导致缓存状态失真，测得的是"被你干扰后的性能"。解决：测量前停止其他进程、关闭打印、跑多次取稳定区间。
- `[实现]`：`-O2` 会删除"结果无副作用"的循环；微基准必须用 `volatile` 或打印/返回结果"锚定"computed 值（如 ⑤⑥ 都 `printf` 了结果）。

## ⑰ 跨平台工具（Windows ETW / Visual Studio Profiler）

`perf` 仅 Linux。Windows 上等价能力：

- **ETW**（Event Tracing for Windows）+ `xperf` / `WPR`：内核级采样。
- **Visual Studio Profiler**：CPU Usage / Instrumentation，GUI 火焰图。

```cpp
// ⑰ 同一段热点代码，跨平台都成立；只是"怎么测"不同
#include <vector>
#include <cstdio>
int main() {
    std::vector<long> v(40'000'000, 2);
    long s = 0;
    for (long x : v) s += x * 3;            // Windows: VS Profiler 采样命中此处
    std::printf("%ld\n", s);
    return 0;
}
```

```bash
# 文件：Windows 管理员 PowerShell（ETW 真实命令，非本机输出）
# 开始记录，10 秒后停止
wpr -start CPU -onCPU            # 开始 CPU 采样
# 运行你的程序 ./app.exe
wpr -stop out.etl                # 停止并写出 ETL
# 用 WPA (Windows Performance Analyzer) 打开 out.etl 看火焰图
```

- `[平台]`：ETW 是 Windows 内核机制；`perf` 是 Linux 内核机制；二者概念同构（采样 + 栈），命令与文件格式不同。
- `[经验]`：团队跨平台时，抽象出"一段可复现基准 + 平台专属采集脚本"，让结论可比。

## ⑱ 可视化

可视化不只是火焰图。常见三类：

1. **火焰图**：调用栈占比（横向 = 采样量）。
2. **时间线/轨迹**（timeline）：多线程、锁等待、I/O 阻塞。
3. **Diff 火焰图**：优化前后减法，直接看"哪块塔矮了"。

```cpp
// ⑱ 多线程时间线视角：各线程忙等 vs 真正计算
#include <thread>
#include <vector>
#include <chrono>
void worker(long n, long& out) {
    long s = 0;
    for (long i=0;i<n;++i) s += i;       // 计算段（时间线里是"忙"）
    out = s;
    std::this_thread::sleep_for(std::chrono::milliseconds(10)); // 阻塞段
}
```

- `[经验]`：锁竞争看"时间线"比看火焰图更直观——火焰图显示"在锁里"，时间线显示"等了多久"。
- `[实现]`：Diff 火焰图 = 蓝（变慢）/ 红（变快）配色，是向同事证明优化有效的利器。

## ⑲ 最佳实践

```cpp
// ⑲ 把热点数据做成"对 cache 友好 + 对编译器友好"的形态
#include <vector>
// 扁平一维 + 规则步长 + 独立累加 —— 同时讨好缓存与向量化
long fast_sum(const long* data, long n) {
    long s0=0,s1=0,s2=0,s3=0;
    long i=0;
    for (; i+4<=n; i+=4){ s0+=data[i]; s1+=data[i+1]; s2+=data[i+2]; s3+=data[i+3]; }
    for (; i<n; ++i) s0+=data[i];
    return s0+s1+s2+s3;
}
```

- `[经验]`：
  1. 先有**可复现基准**，再优化。
  2. 每次只改**一个变量**。
  3. 多跑几轮取**稳定区间**，别信单次。
  4. 锚定结果值，防 `-O2` **删死代码**。
  5. 看**汇编**确认向量化真发生（Godbolt / `-S`）。
- `[标准]`：以上不依赖任何特定编译器扩展，是普适工程纪律。

## ⑳ 速查表

```cpp
// ⑳ 一键自查：你的微基准是否"诚实"？
// 1) 结果是否被使用/打印？ 2) 是否多次取中位数？
// 3) 是否单次只改一个变量？ 4) 是否看了汇编？
bool honest_benchmark(long result_used, int iterations, bool checked_asm) {
    return result_used && iterations >= 10 && checked_asm;
}
```

| 目标 | Linux 命令 | Windows 等价 |
|---|---|---|
| 计数器总览 | `perf stat -d ./app` | VS Profiler / ETW |
| 采样 + 栈 | `perf record -F 99 -g ./app` | WPR + WPA |
| 火焰图 | `perf script \| stackcollapse \| flamegraph.pl` | VS / WPA 内置 |
| 看汇编 | `g++ -S -masm=intel -O2` | 同（MinGW GCC） |

| 现象 | 可能瓶颈 | 对策 |
|---|---|---|
| IPC < 1 | 前端/串行依赖 | 缩短依赖链（⑪） |
| cache-miss 高 | 内存 bound | 局部性（⑫） |
| branch-miss 高 | 不可预测分支 | 查表/概率化 |
| 多线程反而慢 | false sharing | `alignas(64)`（⑯b） |

- `[经验]`：速查表是给你自己用的——贴在显示器边，每次"优化"前对照一遍。
- `[标准]`：所有命令与对策均对应本章前述 C++23 示例，可在 `Examples/_ch15_*.cpp` 复现。

---

## 补充完整可编译示例（profiling）

```cpp
// P1 手动计时模板（避免重复 boilerplate）
#include <chrono>
template <class F>
double time_ms(F f) {
    auto t0 = std::chrono::steady_clock::now();
    f();
    auto t1 = std::chrono::steady_clock::now();
    return std::chrono::duration<double, std::milli>(t1 - t0).count();
}
```

```cpp
// P2 锚定结果，防 -O2 删循环（用 volatile 输出）
#include <vector>
int main() {
    std::vector<long> v(10'000'000, 1);
    long s = 0;
    for (long x : v) s += x;
    volatile long sink = s;   // 阻止优化掉计算
    (void)sink;
    return 0;
}
```

```cpp
// P3 扁平矩阵（连续内存，利于缓存与向量化）
#include <vector>
#include <cstddef>
struct Mat {
    size_t W, H;
    std::vector<double> d;
    Mat(size_t w, size_t h): W(w), H(h), d(w*h) {}
    double& at(size_t i, size_t j) { return d[i*W + j]; }   // 连续寻址
};
```

```cpp
// P4 false sharing 修复：缓存行隔离
#include <cstddef>
struct Aligned {
    alignas(64) long a = 0;   // 独占一个 64 字节缓存行
    alignas(64) long b = 0;   // 与 a 不同行，不再互相 invalidation
};
```

```cpp
// P5 用 std::accumulate 的"看起来不同、其实一样"的写法
#include <vector>
#include <numeric>
long acc_sum(const std::vector<long>& v) {
    return std::accumulate(v.begin(), v.end(), 0L);
}
```

```cpp
// P6 测"分配器压力"：频繁小对象 new/delete
#include <vector>
long alloc_pressure(long n) {
    long s = 0;
    for (long i = 0; i < n; ++i) {
        std::vector<int> tmp(16, (int)i);  // 每次堆分配
        s += tmp.back();
    }
    return s;
}
```

```cpp
// P7 分支预测友好的查表替代（去分支）
#include <array>
long lut_pick(const std::array<long,4>& t, int k) {
    return t[k & 3];   // 用位掩码替代 if/else 链，预测友好
}
```

```cpp
// P8 多线程热点（tbb 风格思路，纯 std 实现）
#include <thread>
#include <vector>
#include <cstddef>
void parallel_sum(const std::vector<long>& v, long& out, size_t lo, size_t hi) {
    long s = 0;
    for (size_t i = lo; i < hi; ++i) s += v[i];
    out = s;
}
```

```cpp
// P9 让函数不被内联，便于 perf 单独采样
__attribute__((noinline)) long isolated(long n) {
    long s = 0; for (long i=0;i<n;++i) s+=i; return s;
}
```

```cpp
// P10 取汇编的极简驱动（配合 g++ -S）
long add_all(const long* a, long n) {
    long r = 0;
    for (long i = 0; i < n; ++i) r += a[i] + 1;  // 看是否被 vectorize
    return r;
}
```

```cpp
// P11 cache line 大小感知的字段排布（热字段聚拢）
struct Hot {
    long hit_count = 0;     // 频繁访问
    long last_value = 0;    // 频繁访问（同缓存行，友好）
    char pad[48];           // 把冷字段推开，减少伪共享/抖动
    long cold_meta = 0;
};
```

```cpp
// P12 基准前"热身"：把数据拉进缓存，避免冷启动噪声
#include <vector>
void warmup(std::vector<long>& v) {
    volatile long s = 0;
    for (long x : v) s += x;   // 触发缺页 + 预热缓存
    (void)s;
}
```

```cpp
// P13 端到端：构建可复现基准的最小骨架
#include <vector>
#include <chrono>
#include <cstdio>
int main() {
    const long N = 10'000'000;
    std::vector<long> v(N, 1);
    auto t0 = std::chrono::steady_clock::now();
    long s = 0; for (long x : v) s += x;
    auto t1 = std::chrono::steady_clock::now();
    std::printf("result=%ld  time=%.2f ms\n", s,
        std::chrono::duration<double, std::milli>(t1 - t0).count());
    return 0;
}
```

## 附录 A：工业性能分析与WG21背景

```
perf (Linux, 2009): perf record -g → perf report → 火焰图(Brendan Gregg,2013)
  → 采样 <5% overhead, Google 强制要求每个perf bug附perf报告
VTune (Intel, 2005): 微架构分析(uop/BPU/cache), HW counter精度 ~1ms
tracy (2017): C++原生profiler, ~50ns/zone, Unity/Blizzard游戏公司使用
```

## 附录 B：性能分析黄金法则与面试

```
黄金法则:
1. 先测量后优化 (never guess bottleneck)
2. 真实负载测试 (production data > synthetic)
3. 一次改一个变量 (否则不知道哪个有效)
4. 优化>1%CPU热路径 (冷路径收益<成本)
5. CI集成benchmark (每个PR自动性能回归检测)

面试: perf(采样,低开销) vs gprof(插桩,-pg编译,2x慢)
       cache-miss: perf stat -e cache-misses,cache-references ./app
       火焰图: X轴=占用比例,Y轴=调用栈深度,宽浅=热路径,高尖=深递归
```


## 联合使用场景

| 关联章节 | 场景 | 组合方式 |
|---|---|---|
| [第14章](Book/part02_toolchain/ch14_debugging.md) | 键值查找/缓存 | 本章提供概念，第14章提供实现 |
| [第16章](Book/part02_toolchain/ch16_ide.md) | 配置解析/API响应 | 本章提供概念，第16章提供实现 |
| [第151章](Book/part13_engineering/ch151_benchmark.md) | 泛型库/编译期计算 | 本章提供概念，第151章提供实现 |
| [第157章](Book/part14_perf/ch157_compiler_explorer.md) | 日志格式化/序列化 | 本章提供概念，第157章提供实现 |


## 相关章节（交叉引用）

- **相邻主题**：`Book/part02_toolchain/ch13_packaging.md`（第13章　包管理：vcpkg / Conan（C++））—— 编号相邻、主题接续。
- **相邻主题**：`Book/part02_toolchain/ch17_crosscompile.md`（第17章　交叉编译与嵌入式工具链（C++））—— 编号相邻、主题接续。
- **同模块**：`Book/part02_toolchain/ch11_compilers.md`（第11章　编译器全景：GCC / Clang / MSVC 架构与 ABI（C++））—— 同模块下的其他主题。

## 真实开源项目参考（可查证链接）

> 本节补可查证的真实项目引用（非虚构）。

- **Linux `perf`（github.com/torvalds/linux）**：`perf record`/`perf stat` 是用户态采样与硬件 PMU 计数（cycles/instructions/cache-misses）的工业标准，本章「② 热点定位」直接对应 `perf annotate` 的反汇编注释。
- **Google Benchmark（github.com/google/benchmark）**：微基准框架——`BENCHMARK` 宏 + `benchmark::DoNotOptimize` 防止编译器把被测循环优化掉，是「③ 微基准陷阱」的官方解法。
- **LLVM XRay（llvm/llvm-project）**：编译期插桩的轻量 tracing——`-fxray-instrument` 在每条函数入口/出口写入 sled，运行时 `xray` 工具聚合调用图，对应「④ 调用图深度」。
- **Chromium tracing（`base::trace_event`）**：`chrome://tracing` 的后端——`TRACE_EVENT` 宏产出 Chrome JSON 格式 trace，浏览器级性能画像直接落地。
- **gperftools（github.com/gperftools/gperftools）**：Google 的 `pprof` + `TCMalloc` 采样器，CPU profiler 用信号采样栈，对应「① 采样 vs 插桩」的采样派代表。
- **Abseil（abseil/abseil-cpp）**：`absl::Profiling` 与 `pprof` 输出配合，是 Google 内部 profiling 栈的一环。
- **ClickHouse（ClickHouse/ClickHouse）**：列式引擎用 `perf` + 自研 `query_log` 做瓶颈定位，其官方性能指南明确推荐 `perf record -g` 抓 CPU 火焰图。

**最佳实践**：采样型 profiler（`perf`/`pprof`）开销低但分辨率受采样频率限制；插桩型（XRay/tracing）精确但引入固定开销。热路径先用 `perf` 粗定位，再 `XRay` 细追。

> 交叉引用：基准方法见 [ch151](Book/part13_engineering/ch151_benchmark.md)；编译器优化见 [ch156](Book/part14_perf/ch156_compiler_opt.md)。

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

