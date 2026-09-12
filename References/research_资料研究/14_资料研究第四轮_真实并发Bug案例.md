# 资料研究第四轮：真实并发 Bug 案例——从 PostgreSQL 到 ProxySQL 的反面教材

> 2026-09-11，底层工程资料研究员。主题：真实并发 bug 案例。
> 检索方式：web.fetch 一手来源（kernel.org / postgresql.org / GitHub）+ general_search。

---

## 一、核心资料（S/A+ 级）

### 1. PostgreSQL 18.1：`__atomic_thread_fence()` 不阻止编译器重排

- **类型**：真实 bug（release note）
- **来源**：PostgreSQL 官方 release notes
- **链接**：https://www.postgresql.org/docs/release/18.1/
- **修复者**：Thomas Munro
- **核心内容**：PostgreSQL 假设 `__atomic_thread_fence()` 是足够的屏障，可以阻止 C 编译器在其周围重排内存访问。**但 Clang 不这么认为**——在 RISC-V、MIPS、LoongArch 上，Clang 仍然重排了内存访问，生成错误代码。修复：加显式 compiler barrier。
- **解决的问题**：编译器重排 vs CPU 重排的混淆——`__atomic_thread_fence()` 是运行时内存屏障（阻止 CPU 重排），但不保证阻止编译器重排
- **为什么重要**：**这是"编译器重排"最经典的真实案例**。连 PostgreSQL 这样的顶级项目都会犯"以为运行时屏障能阻止编译器重排"的错误。而且只在非 x86 架构上触发——x86 TSO 再次掩盖了 bug。
- **技术亮点**：
  - `__atomic_thread_fence(memory_order_acq_rel)` 生成 CPU 屏障指令，但编译器仍可以在它周围重排
  - 正确做法：`asm volatile("" ::: "memory")`（编译器屏障）+ `__atomic_thread_fence()`（CPU 屏障），或用 `atomic_thread_fence` 的同时加 `barrier()`
  - 只在 RISC-V/MIPS/LoongArch 触发——x86 上即使编译器重排了，CPU TSO 也会把顺序拉回来
- **与 C++ 的关系**：C++ `std::atomic_thread_fence()` 同样只保证运行时顺序，编译器优化仍可能重排；需要 `std::atomic_signal_fence()` 或 `asm volatile("" ::: "memory")` 来阻止编译器重排
- **与 CPP-Bible 的关系**：CONC 域"编译器重排 vs CPU 重排"pitfall 原子的绝佳素材；可以做成"x86 上能跑、ARM 上崩"的实验
- **可以放入哪个章节**：part09_concurrency（内存序）、part08_compiler（编译器优化）
- **适合讲什么**：编译器重排、运行时屏障的局限、跨架构可移植性
- **可以设计什么实验**：用 `-O2` 在 x86 和 ARM（QEMU）上分别编译同一段无屏障代码，对比汇编输出
- **历史背景**：2025 年 11 月 PostgreSQL 18.1 修复；这个 bug 可能存在了很久，只是因为 x86 TSO 掩盖了
- **可信度**：S（PostgreSQL 官方 release note，一手来源）
- **教材价值**：S

### 2. ProxySQL #5353：`memory_order_relaxed` 导致的引用计数可见性 bug

- **类型**：真实 bug（GitHub PR）
- **来源**：ProxySQL（sysown/proxysql）
- **链接**：https://github.com/sysown/proxysql/pull/5353
- **核心内容**：ProxySQL 的 PostgreSQL prepared statement purge 线程用 `memory_order_relaxed` 检查 `ref_count_client`，看不到其他线程的最新值，读到 stale 数据后以为引用计数为 0，purge 了仍在使用的 statement → crash。修复：`memory_order_relaxed` → `memory_order_acquire`。
- **解决的问题**：`memory_order_relaxed` 只保证原子性（不撕裂），不保证可见性顺序
- **为什么重要**：**这是"relaxed 用错"最典型的工业案例**。很多人以为"原子操作就是线程安全的"，但 relaxed 原子操作只保证不撕裂，不保证你看到的是最新值。引用计数是最容易踩这个坑的场景。
- **技术亮点**：
  - `ref_count_client.load(memory_order_relaxed)` 可能返回旧值——其他线程已经递增了，但当前线程看不到
  - 修复不只是改 load：对应的 store 也要用 `memory_order_release`，形成 acquire-release 对
  - PR 附带了回归测试（并发创建/销毁 prepared statement，低缓存阈值触发频繁 purge）
- **与 C++ 的关系**：直接对应 `std::atomic::load(memory_order_relaxed)` vs `memory_order_acquire`
- **与 CPP-Bible 的关系**：CONC 域"memory_order_relaxed 的可见性陷阱"pitfall 原子；与上一轮 preshing 的内存序文章形成"理论→真实 bug"闭环
- **可以放入哪个章节**：part09_concurrency
- **适合讲什么**：relaxed vs acquire 的区别、引用计数的可见性要求、acquire-release 配对
- **可以设计什么实验**：两个线程，一个递增 relaxed 原子、一个读 relaxed 原子，在 ARM 上用压力测试复现 stale read（x86 上很难复现）
- **历史背景**：2026 年 2 月修复；bug 编号 #5352
- **可信度**：A+（GitHub PR，含修复 diff 和回归测试）
- **教材价值**：S

### 3. Linux Kernel memory-barriers.txt（130KB）

- **类型**：官方技术文档（真实案例集合）
- **来源**：Linux Kernel（kernel.org）
- **链接**：https://www.kernel.org/doc/Documentation/memory-barriers.txt
- **作者**：David Howells、Paul E. McKenney、Will Deacon、Peter Zijlstra
- **核心内容**：Linux 内核内存屏障的完整指南——抽象内存访问模型、屏障种类、什么不能假设、地址依赖、控制依赖、SMP 屏障配对、I/O 屏障、中断交互。包含大量**真实的反例**和"不要这样做"的案例。
- **解决的问题**：如何在内核中正确使用内存屏障
- **为什么重要**：**这是内存屏障最权威的实践文档**，130KB，四位内核维护者合著。里面的"什么不能假设"一节全是真实踩坑总结。
- **技术亮点**：
  - **控制依赖（control dependency）**：`if (READ_ONCE(x)) { WRITE_ONCE(y); }` 中，y 的写不能被移到 if 之前——但编译器可能不这么认为，需要 `barrier()`
  - **地址依赖**：Alpha 是唯一需要地址依赖屏障的架构（其他架构自然保持）；`rcu_dereference()` 在 Alpha 上生成屏障，在其他架构上编译为空
  - **SMP 屏障配对**：写端的 release 必须和读端的 acquire 配对，单边屏障无效
  - **I/O 屏障**：MMIO 寄存器访问的顺序问题，地址寄存器+数据寄存器的经典 race
- **与 C++ 的关系**：Linux 的 `smp_store_release`/`smp_load_acquire` 与 C++ `memory_order_release`/`memory_order_acquire` 语义完全对应
- **与 CPP-Bible 的关系**：CONC 域"内存屏障"章节的核心参考；控制依赖和地址依赖是高级主题
- **可以放入哪个章节**：part09_concurrency、part16_os
- **适合讲什么**：内存屏障的种类、控制依赖、地址依赖、屏障配对
- **可以设计什么实验**：控制依赖被编译器重排的实验（`if (atomic_load(x)) { non_atomic_store(y); }` 在 -O2 下的汇编）
- **历史背景**：持续维护 15+ 年，从 2.6 内核到 6.x
- **可信度**：S
- **教材价值**：A+

---

## 二、其他高价值真实 bug（A 级）

### 4. 线程池析构函数 race（ThreadSanitizer 抓到）

- **类型**：真实 bug（案例分析）
- **来源**：DEV Community 案例研究
- **链接**：https://dev.to/datacpp_8185/case-study-the-thread-pool-passed-6464-tasks-threadsanitizer-found-the-race-in-the-destructor-3cal
- **核心内容**：线程池 64/64 任务全部通过，但 ThreadSanitizer 在析构函数里发现了 race——析构函数写 `stop_` 标志没有被 mutex 保护，worker 线程在下一轮循环时读 `stop_` 没有 happens-before 边。窗口只有几微秒，所以测试全过但实际有 race。
- **教学价值**：**"测试通过≠没有 race"**。race 窗口极小时，常规功能测试永远抓不到，必须用 TSan。这是"为什么需要 sanitizer"的最佳案例。

### 5. `std::vector<bool>` 线程安全误解

- **类型**：真实 bug（GitHub issue）
- **来源**：cybrid-systems/aura #1083
- **链接**：https://github.com/cybrid-systems/aura/issues/1083
- **核心内容**：GC 的 mark 阶段用 `std::vector<bool>` 做标记位图，文档声称"atomic byte writes"所以线程安全。但 `std::vector<bool>::operator[]` 返回代理类型（`std::vector<bool>::reference`），写代理需要读-改-写整个字节（因为 bit-packed），不是原子的。多线程写不同 bit 会 race。
- **教学价值**：`std::vector<bool>` 是特殊化，不是容器——`operator[]` 不返回 `bool&` 而是代理。这是 C++ 最著名的"不是容器的容器"。

### 6. Hazard Pointer 内存序 bug（ARM64 use-after-free）

- **类型**：真实 bug（GitHub issue）
- **来源**：kcenon/thread_system #600
- **链接**：https://github.com/kcenon/thread_system/issues/600
- **核心内容**：Hazard Pointer 实现的内存序有问题，在弱模型架构（ARM64）上 CPU 重排导致 use-after-free。代码里甚至有注释："This implementation has memory ordering issues (TICKET-002)"。
- **教学价值**：与上一轮 folly Hazptr 形成对比——"正确的 HP 实现"和"有内存序 bug 的 HP 实现"的差别。HP 的保护逻辑必须用 acquire-release 配对，否则弱模型上会崩。

### 7. "x86 能跑、ARM 失败"模式

- **类型**：普遍现象（多个来源）
- **来源**：多篇工程博客 + PostgreSQL bug
- **核心内容**：x86 TSO 让每个 load 自带 acquire、每个 store 自带 release，所以很多内存序错误在 x86 上不会触发。迁到 ARM（AWS Graviton、Azure Cobalt、苹果硅）后才失败。这是云原生时代越来越常见的问题。
- **教学价值**：这是"为什么不能只在 x86 上测试并发代码"的核心理由。CPP-Bible 的 CI 已经有 Clang 矩阵，可以扩展到 ARM QEMU。

---

## 三、Bug 分类体系（教学用）

本轮调研的真实 bug 可以归纳为 **5 类并发 bug 模式**，每类都可以做成 pitfall 原子：

| 类别 | 典型 bug | 根因 | 检测手段 |
|---|---|---|---|
| ① 编译器重排 | PostgreSQL `__atomic_thread_fence` | 运行时屏障不阻止编译器重排 | 跨架构编译、看汇编 |
| ② 内存序用错 | ProxySQL relaxed 引用计数 | relaxed 不保证可见性顺序 | TSan、弱模型压力测试 |
| ③ 缺 happens-before | 线程池析构 race | 无同步的共享变量访问 | TSan |
| ④ 伪线程安全 | vector<bool> 代理写 | 以为 bit 写是原子的 | 代码审查、TSan |
| ⑤ x86 TSO 掩盖 | HP 内存序 bug（ARM64） | x86 免费 acquire/release 掩盖错误 | ARM QEMU、跨架构 CI |

---

## 四、知识网络

```
真实并发 bug
├── 编译器重排（PostgreSQL）
│   └── 运行时屏障 ≠ 编译器屏障
│       ├── __atomic_thread_fence → CPU 屏障
│       ├── asm volatile("":::"memory") → 编译器屏障
│       └── 两者都需要
│
├── 内存序用错（ProxySQL）
│   └── relaxed 只保证原子性，不保证可见性
│       ├── 引用计数必须 acquire-release
│       └── 对应 C++ memory_order 枚举
│
├── 缺 happens-before（线程池析构）
│   └── 测试通过 ≠ 没有 race
│       ├── race 窗口几微秒
│       └── TSan 是唯一可靠手段
│
├── 伪线程安全（vector<bool>）
│   └── 代理类型的读-改-写
│       ├── vector<bool> 不是容器
│       └── bit-packed 存储的固有问题
│
└── x86 TSO 掩盖（HP bug、PostgreSQL）
    └── x86 上能跑 ≠ 正确
        ├── x86 load=acquire / store=release（免费）
        ├── ARM/PowerPC/RISC-V 弱模型
        └── 跨架构 CI 是唯一解法
```

---

## 五、本轮最重要的 10 个资料

| # | 资料 | 级别 | 核心价值 |
|---|---|---|---|
| 1 | PostgreSQL 18.1 编译器屏障 bug | S | 编译器重排真实案例，顶级项目也踩坑 |
| 2 | ProxySQL #5353 relaxed bug | A+ | relaxed 可见性陷阱，含修复和回归测试 |
| 3 | Linux memory-barriers.txt | S | 130KB 权威文档，控制依赖/地址依赖 |
| 4 | 线程池析构 TSan 案例 | A | "测试通过≠没有 race" |
| 5 | vector<bool> 伪线程安全 | A | 代理类型的读-改-写 race |
| 6 | HP 内存序 bug（ARM64） | A | 弱模型 use-after-free |
| 7 | "x86 能跑 ARM 失败"模式 | A+ | 跨架构可移植性的普遍问题 |
| 8 | preshing 内存序（上一轮） | A+ | 理论基础 |
| 9 | Boehm PLDI 2005（第一轮） | S | 内存模型奠基 |
| 10 | folly Hazptr（上一轮） | A+ | 正确的 HP 实现（对比 bug 版） |

## 六、强烈建议深入研究的 5 个资料

1. **PostgreSQL 18.1 release note**——精读编译器屏障 bug 的修复 commit，看加了什么 barrier
2. **Linux memory-barriers.txt**——重点读"什么不能假设"和"控制依赖"两节
3. **ProxySQL #5353 diff**——看 relaxed→acquire 的具体改动和回归测试
4. **ThreadSanitizer 官方文档**——理解 TSan 能抓什么、不能抓什么
5. **PostgreSQL 18.2 异步 I/O race**——另一个真实并发 bug

## 七、适合直接进入 CPP-Bible 的资料

| 资料 | 进入方式 | 目标原子/章节 |
|---|---|---|
| PostgreSQL 编译器屏障 bug | "编译器重排 vs CPU 重排"pitfall | CONC 域原子 |
| ProxySQL relaxed bug | "relaxed 可见性陷阱"pitfall | CONC 域原子 |
| 线程池析构 race | "为什么需要 TSan"案例 | CONC/TOOL 交叉 |
| vector<bool> 伪线程安全 | "vector<bool> 不是容器"pitfall | STL 域原子 |
| 5 类 bug 分类表 | 直接作为 CONC 域章级概述 | part09_concurrency |

## 八、发现的知识空白

1. **编译器重排完全未覆盖**——全书只讲 CPU 重排，不讲编译器重排
2. **"测试通过≠没有 race"无案例**——TSan 的价值没有真实案例支撑
3. **跨架构可移植性无实验**——没有"x86 能跑 ARM 失败"的可复现实验
4. **vector<bool> 线程安全问题未覆盖**——STL 域的经典 pitfall
5. **真实工业 bug 案例库缺失**——全书都是正面教材，缺反面案例

## 九、下一轮推荐搜索方向

1. **内存模型形式化验证**——Linux tools/memory-model/（herd7 工具）、Cambridge 内存模型、可以机器验证内存序
2. **C++ 标准提案追踪**——P2530R3 Hazard Pointer 最新进展、atomic_ref、jthread
3. **ARM 弱内存模型**——ARM Architecture Reference Manual、ARM 上的重排实验（需 QEMU）
4. **seqlock / per-CPU 数据结构**——Linux 其他读多写少同步机制，与 RCU 对比
5. **无锁数据结构正确性验证**——CDSChecker、Relacy 等无锁算法验证工具
6. **C++26 并发特性**——hazard pointer 标准化、execution policy、stop_token

---

*本轮新增知识节点：编译器重排、relaxed 可见性陷阱、happens-before 缺失、伪线程安全、x86 TSO 掩盖、5 类并发 bug 分类。补齐了 CONC 域"反面案例"和"编译器重排"两个空白。四轮调研形成完整并发教学链：内存模型（理论）→ RCU/HP（回收）→ 无锁数据结构（算法）→ 真实 bug（反面教材）。*
