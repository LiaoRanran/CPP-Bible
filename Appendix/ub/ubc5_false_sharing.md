# UB-C5 false sharing（伪共享）

**分类**：并发/性能 UB（缓存一致性副作用）｜ **检测工具**：基准测量 / TSan 不报
**源码**：[ub_false_sharing.cpp](./ub_false_sharing.cpp)

---

## ① 真实代码

```cpp
#include <atomic>
#include <chrono>
#include <cstdio>
#include <thread>

static const long N = 200'000'000L;

struct Packed { std::atomic<long> x{0}, y{0}; } g_packed;        // 同缓存行 → 伪共享
struct Aligned { alignas(64) std::atomic<long> x{0};              // 各占一行 → 无共享
               alignas(64) std::atomic<long> y{0}; } g_aligned;

// bench_packed / bench_aligned：各起 2 线程分别 fetch_add 自己的计数器，测总耗时
```

## ② 为什么是 UB / 性能陷阱

两个线程各自修改**独立变量**，逻辑上无竞争（变量不同），但两变量位于**同一
64 字节缓存行**。x86 缓存一致性协议（MESI）要求：任一核写该行，其它核的该行
副本即失效，须重新从拥有者拉取。两线程高频写 → 缓存行在核间**反复弹跳（bounce）**，
每次写都触发跨核一致性流量。这不是 UB 的"未定义"，而是**定义良好但极慢**——
教科书称其为「伪共享」，是并发性能的头号隐性杀手。

## ③ 基准结果（本机实测，GCC 15.3.0 `-O2 -pthread`，32 逻辑核）

| 版本 | 耗时 | 说明 |
|------|------|------|
| Packed（同缓存行） | **4237.8 ms** | 两核争同一缓存行，MESI 弹跳 |
| Aligned（各占一行） | **698.1 ms** | 无弹跳 |
| **加速比** | **≈ 6.1×** | 仅因加 `alignas(64)` |

3 次复测稳定（4237/4130/4057 ms vs 698/701/701 ms，slowdown 5.8–6.1×）。

> 这是**真实可复现**的性能证据（无需 sanitizer）。在多核/多路服务器上，放大更剧烈，
> 文献与生产案例常见 **10–50×** 退化。

## ④ 根因

`struct Packed { long x, y; }` 中 `x` 与 `y` 地址相邻，落入同一 64B 缓存行。
两线程各写一个字段，触发缓存一致性协议的缓存行无效/传输风暴。

## ⑤ 修复

```cpp
// 1) 按缓存行对齐隔离热写字段
struct Aligned { alignas(std::hardware_destructive_interference_size) std::atomic<long> x{0};
                 alignas(std::hardware_destructive_interference_size) std::atomic<long> y{0}; };

// 2) 或把频繁写的字段凑到不同结构（避免与只读字段同行的"伪共享"）
// 3) 或合并为单计数器 + 分片（sharding）：N 个线程各写本地分片，最后汇总
```

`std::hardware_destructive_interference_size`（C++17）是标准给出的缓存行大小
（多数平台 64），比硬编码 `alignas(64)` 更具可移植性。

## ⑥ 检测建议

- 性能剖析：perf `cache-misses` / `mem_load_uops_retired.l2_miss` 异常高 → 怀疑伪共享。
- TSan **不**报伪共享（它不是 race）；靠基准对比（同/不同行）定位。
- 高频计数器、每线程状态、无锁结构的热字段是重灾区。
