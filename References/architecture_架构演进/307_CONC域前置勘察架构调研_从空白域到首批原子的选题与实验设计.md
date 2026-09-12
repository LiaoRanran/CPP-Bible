# 307_CONC域前置勘察架构调研_从空白域到首批原子的选题与实验设计

> 2026-09-12 · CONC 域当前零原子/零证据卡，但有 8 份调研资料。本文勘察首批 CONC 原子的选题、实验设计、工具链需求和风险。
> 关联：References/research_资料研究/11/13/14/17/19/21/53/55 · gate_engine DOMAINS（CONC 已合法）

---

## 一、CONC 域现状

### 1.1 空白程度

| 项 | 数量 | 说明 |
|---|---|---|
| atoms/conc/ | 0 | 目录不存在 |
| evidence/conc/ | 0 | 目录不存在 |
| misconceptions/conc/ | 0 | 目录不存在 |
| 并发相关 References | 8 份 | 内存模型/无锁/seqlock/GC/Bug 案例 |

**结论**：CONC 是完全空白的域，但调研资料充足。这是"高开采价值"的域——从零开始，可以建立最优的结构，不受历史包袱影响。

### 1.2 已有调研资料盘点

| 编号 | 主题 | 可转化为原子的素材 |
|---|---|---|
| 11 | C++ 内存模型与并发 | memory_order 六档、happens-before、synchronizes-with |
| 13 | 无锁数据结构 | CAS、ABA、Michael-Scott 队列、无锁栈 |
| 14 | 真实并发 Bug 案例 | 死锁、数据竞争、活锁、优先级反转 |
| 17 | C++26 并发特性 | jthread、stop_token、latches、barriers、安全内存回收 |
| 19 | seqlock 与 per-CPU | seqlock 读写模式、per-CPU 数据结构 |
| 21 | 无锁正确性验证 | Relacy、cdschecker、模型检验 |
| 53 | 无锁内存回收 | Hazard Pointer、EBR、RCU、ABA 问题 |
| 55 | 垃圾回收深度 | 分代/三色标记/写屏障/ZGC，与 RAII 对照 |

---

## 二、首批 CONC 原子选题

### 2.1 选题原则

1. **从基础到高级**：首批应该是 CONC 域的"地基"——内存序、原子操作、锁的代价
2. **可实验验证**：每个选题必须能写夹具、跑实测、生成工件（与 MEM 域同标准）
3. **教学价值高**：能展示 C++ 并发的核心概念，不是边角特性
4. **与 MEM 域衔接**：CONC 与 MEM 密切相关（内存序、缓存行、false sharing），首批可以利用已有 PERF-004（false sharing）的基础

### 2.2 首批 3 颗原子建议

#### CONC-001：内存序六档的可观测差异

**type**: mechanism
**claim**：C++ memory_order 六档（relaxed/consume/acquire/release/acq_rel/seq_cst）在 x86-64 上的编译产物差异是可观测的——relaxed 无屏障、acquire/release 单向屏障、seq_cst 全屏障（mfence 或 lock xchg）；但在 ARM 上差异更大（dmb ish 等），"x86 上跑通"不等于"可移植"。

**实验设计**：
- 夹具：同一组原子操作（store/load/fetch_add），用六档 memory_order 分别编译
- 工件：.asm 对比六档的编译产物（x86-64 + ARM 交叉编译或 WSL）
- 断言：contains_any 检查各档的屏障指令（mfence/lock/dmb）
- 活性对照：seq_cst 的指令数 > relaxed 的指令数

**难点**：
- ARM 交叉编译需要工具链（WSL 安装 g++-arm-linux-gnueabihf）
- memory_order_consume 在大多数编译器中被降级为 acquire（需要如实标注）
- 运行时差异比编译期差异更难观测（需要多线程压测）

**DAL**：B（教学结论方向——如果内存序的理解错了，读者会写出并发缺陷）

#### CONC-002：锁的代价与无锁的代价

**type**: contrast
**claim**：互斥锁（std::mutex）的代价是"上下文切换 + 缓存失效 + 公平性开销"，无锁 CAS 的代价是"重试循环 + ABA 风险 + 内存回收"；在低竞争下 mutex 可能比 CAS 更快（futex 快速路径），在高竞争下 CAS 的重试开销可能超过锁的等待开销——"无锁一定更快"是误解。

**实验设计**：
- 夹具：同一计数器（单值递增），三种实现：std::mutex、atomic.fetch_add、CAS 重试循环
- 性能：1/2/4/8 线程各跑 1e7 次递增，测吞吐量和延迟分布
- 工件：.asm 对比 lock add（fetch_add）vs CAS 循环（lock cmpxchg）vs mutex 调用（__gthread_mutex_lock）
- 活性对照：单线程下三者性能接近（证明差异来自竞争，不是实现本身）

**难点**：
- 性能数据波动大（需要多轮中位数，同 PERF-003/004 的方法论）
- std::mutex 的实现差异大（glibc futex vs MSVC CRITICAL_SECTION）
- 需要控制线程亲和性（避免线程迁移影响缓存）

**DAL**：C（性能定量结论，不改变方向）

#### CONC-003：数据竞争的 UB 与工具检测

**type**: pitfall
**claim**：数据竞争是 C++ 的未定义行为——编译器可以假设"非原子变量不会被并发修改"，从而做出激进优化（如把变量缓存在寄存器、重排读写）；这种优化在单线程下正确，在多线程下产生错误结果。ThreadSanitizer 可以检测数据竞争，但有 5-15× 性能开销和 5-10× 内存开销。

**实验设计**：
- 夹具：两个线程并发读写一个非原子 int（无同步），编译 -O0 vs -O2，观察结果差异
- 工件：.asm 对比 -O0 和 -O2 的编译产物（-O2 可能把变量缓存在寄存器）
- TSan：用 -fsanitize=thread 编译运行，观察 TSan 报告
- 活性对照：用 std::atomic 后数据竞争消失（TSan 不报）

**难点**：
- 数据竞争是 UB，结果不确定——需要多跑几次才能复现
- TSan 在 MinGW 上不支持（需要 WSL/Linux）
- -O2 的优化可能完全消除变量（需要 volatile 或 side effect 防止优化）

**DAL**：A（读者写出数据竞争 = 并发缺陷，崩溃/数据错误）

### 2.3 第二批候选（CONC-004..006）

| 编号 | 主题 | type | 前置 |
|---|---|---|---|
| CONC-004 | false sharing 与缓存行（可与 PERF-004 合并或扩展） | pitfall | CONC-001 |
| CONC-005 | ABA 问题与 Hazard Pointer | mechanism | CONC-002 |
| CONC-006 | 死锁的四个必要条件与 std::lock | pitfall | CONC-002 |
| CONC-007 | seqlock 的读写模式 | mechanism | CONC-001 |
| CONC-008 | RCU 与 EBR 的内存回收 | mechanism | CONC-005 |

---

## 三、工具链需求

### 3.1 编译器

| 工具 | 用途 | 当前状态 |
|---|---|---|
| MinGW g++ 15.3 | Windows 侧编译/工件 | ✅ 已有 |
| WSL g++-14 | Linux 侧编译/TSan | ✅ 已有 |
| WSL g++-14 -fsanitize=thread | TSan 数据竞争检测 | ✅ 可用（需验证） |
| ARM 交叉编译 | ARM 内存序工件对比 | ❌ 需安装 g++-arm-linux-gnueabihf |
| Clang | 多编译器对照 | ❌ 仓内无 Clang 记录（可 WSL 安装或 CI） |

### 3.2 运行时控制

| 需求 | 方案 |
|---|---|
| 线程亲和性 | SetThreadAffinityMask（Windows）/ sched_setaffinity（Linux） |
| 性能计时 | std::chrono::high_resolution_clock（同 PERF-003/004） |
| 多轮中位数 | 同 PERF-003 的 7 轮中位数方法论 |
| 缓存刷新 | _mm_clflush（x86）或 std::atomic_thread_fence |

### 3.3 CI 适配

- TSan 在 CI（ubuntu-latest）上可用
- ARM 交叉编译在 CI 上可安装（apt install g++-arm-linux-gnueabihf）
- 并发测试的运行时间可能较长（多线程压测），需要控制 CI 超时

---

## 四、与 MEM 域的衔接

### 4.1 已有原子的复用

| MEM 原子 | CONC 复用方式 |
|---|---|
| PERF-004（false sharing） | CONC-004 可以直接引用，或扩展为"缓存行与并发" |
| SHARED-002（线程安全边界） | CONC-002 可以引用"shared_ptr 控制块的原子 RMW" |
| VALUE-001/002（值类别） | CONC-001 可以引用"右值引用与移动在并发中的意义" |

### 4.2 关系设计

- CONC-001 prerequisites [PERF-004]（缓存行是内存序的硬件基础）
- CONC-002 contrasts [SHARED-002]（锁 vs 原子 RMW）
- CONC-003 contrasts [UB-GRAY-001]（数据竞争是 UB 的一种）
- CONC-001 builds_on [VALUE-001]（原子操作的值类别）

---

## 五、风险与缓解

| 风险 | 缓解 |
|---|---|
| 并发测试结果不确定（UB/时序敏感） | 多轮运行 + 中位数 + 明确标注"本结果在 X 核/Y 内存/Z OS 上获得" |
| TSan 在 MinGW 不可用 | 只用 WSL/Linux 跑 TSan，Windows 侧只做编译期工件对比 |
| ARM 交叉编译工具链缺失 | 首批只做 x86-64，ARM 作为"外部留痕"（同 PERF-003 的 libc++ 处理） |
| 性能数据波动大 | 同 PERF-003/004 的方法论：锚方向不锚倍数，多轮中位数 |
| 并发夹具的复杂度高 | 首批从简单的计数器开始，不做复杂的无锁数据结构 |
| DAL A 原子需要人审 | CONC-003 是 DAL A，需要人审签署；可以先做 CONC-001/002（DAL B/C） |

---

## 六、实施建议

### 6.1 第六批是否转 CONC？

**建议：是。** 理由：
1. MEM 域 18 颗，边际递减（再做 MEM 是"补充"而非"开拓"）
2. CONC 域零开采，首批 3 颗可以建立域的地基
3. 调研资料充足（8 份），不需要额外调研
4. CONC 与 MEM 衔接好（PERF-004 已铺垫）
5. 用户的 CPP-Bible 目标是"贯通"，CONC 是关键一环

### 6.2 首批顺序

1. **CONC-001（内存序）**：地基，其他 CONC 原子都依赖它
2. **CONC-002（锁 vs 无锁）**：性能对比，复用 PERF-003/004 的方法论
3. **CONC-003（数据竞争 UB）**：pitfall，与 UB-GRAY-001 形成对照

### 6.3 前置准备

1. 新建 atoms/conc/、evidence/conc/、misconceptions/conc/ 目录
2. 验证 WSL TSan 可用（写一个探针夹具）
3. 验证 WSL g++-14 的并发编译（pthread 链接）
4. 确认 gate_engine 对 CONC 域的支持（已确认 DOMAINS 含 CONC）
5. 编号规则：EV-CONC-001..、MIS-CONC-001..

---

*核心结论：CONC 域是"高开采价值"的空白域——零原子但有 8 份调研资料，与 MEM 域衔接好，教学价值高。首批 3 颗（内存序/锁代价/数据竞争 UB）覆盖了 CONC 的地基，实验设计可复用 PERF-003/004 的方法论。主要风险是并发测试的不确定性和 TSan 的平台限制，但都有成熟的缓解方案。*
