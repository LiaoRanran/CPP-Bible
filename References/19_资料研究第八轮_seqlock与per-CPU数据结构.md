# 资料研究第八轮：seqlock / per-CPU 数据结构——读多写少同步的另一条路

> 2026-09-11，底层工程资料研究员。主题：seqlock / per-CPU 数据结构。
> 检索方式：web.fetch 一手来源（docs.kernel.org / kernel.org）+ general_search。

---

## 一、核心资料（S/A+ 级）

### 1. Linux Kernel seqlock（Sequence Counter + Sequential Lock）

- **类型**：内核同步机制（官方文档 + 源码）
- **来源**：Linux Kernel（docs.kernel.org/locking/seqlock.html + include/linux/seqlock.h）
- **链接**：https://docs.kernel.org/locking/seqlock.html
- **核心内容**：seqlock 用一个单调递增的序号实现无锁读——写者进出临界区各加一次序号（进入时变奇、退出时变偶），读者读前读序号、读后再读，两次相等且为偶才说明读取没被打断。
- **解决的问题**：读多写少场景下，读者完全无锁、不阻塞写者
- **为什么重要**：**这是"乐观读"的经典实现**——和 RCU 一样读者无锁，但机制完全不同（序号验证 vs 宽限期延迟回收）。两者是互补的，不是替代的。
- **技术亮点**：
  - **奇偶序号机制**：序号为奇 = 写者正在写，读者必须重试；序号为偶且前后一致 = 快照有效
  - **写者优先**：写者获取 spinlock 后直接写，不等读者——读者可能饿死（高频写时无限重试）
  - **三种读者模式**：
    1. **无锁读**（`read_seqbegin`/`read_seqretry`）：不阻塞写者，但可能重试
    2. **锁读**（`read_seqlock_excl`）：排他锁，和写者互斥（避免饿死）
    3. **条件读**（`read_seqbegin_or_lock`）：先试无锁读，失败后退化为锁读（防饿死的自适应策略）
  - **seqcount_t vs seqlock_t**：seqcount_t 是原始计数器（需外部锁串行化写者），seqlock_t = seqcount_t + 内嵌 spinlock
- **与 C++ 的关系**：C++ 标准库没有 seqlock，但可以用 `std::atomic<unsigned>` 实现——folly 有 `SequencedWriteLock`，用户态也有多种实现
- **与 CPP-Bible 的关系**：CONC 域"乐观读"机制的另一种实现；与 RCU 形成对比教学
- **可以放入哪个章节**：part09_concurrency、part16_os
- **适合讲什么**：乐观读、序号验证、写者优先、seqlock vs RCU
- **可以设计什么实验**：用 `std::atomic<unsigned>` 实现用户态 seqlock，对比无锁读和 mutex 的性能
- **历史背景**：源于 x86_64 vsyscall gettimeofday（Keith Owens、Andrea Arcangeli），2.6 内核引入
- **可信度**：S（Linux 内核官方文档 + 源码）
- **教材价值**：S

### 2. seqlock vs RCU：什么时候用哪个

- **类型**：对比分析（多方来源）
- **来源**：Linux 内核文档 + 技术博客 + 内核源码注释
- **核心内容**：

| 维度 | seqlock | RCU |
|---|---|---|
| 读端开销 | 两次读序号 + 比较（极低） | rcu_read_lock/unlock（接近零，可能编译为空） |
| 写端开销 | spinlock + 序号×2 | spinlock + 等待 grace period |
| 读者饿死 | 可能（高频写时无限重试） | 不可能（grace period 保证） |
| 适用数据 | 小结构体、简单值 | 指针指向的可回收数据 |
| 内存回收 | 不处理（数据原地更新） | 延迟回收（grace period 后释放） |
| 指针安全 | 不保证（指针可能指向已释放内存） | 保证（grace period 内不释放） |
| 典型场景 | 时间戳、统计计数、配置参数 | 路由表、进程列表、文件系统路径 |

**关键区别**：seqlock 是"原地更新 + 序号验证快照一致性"，RCU 是"写时复制 + 延迟回收保证指针安全"。**涉及可回收内存的指针必须用 RCU，seqlock 不能保证指针指向的内存不被释放。** Linux 路径查找就是 RCU + seqlock 组合——RCU 保证 dentry 不释放，seqlock 保证字段读取一致。

- **为什么重要**：**这是"没有银弹"的最佳教学案例**——两种读多写少机制各有适用场景，选错会出 bug（用 seqlock 保护指针 = use-after-free）。
- **教学价值**：S

### 3. per-CPU 数据结构与 this_cpu_ops

- **类型**：内核性能优化机制（官方文档）
- **来源**：Linux Kernel（docs.kernel.org/core-api/this_cpu_ops.html + mm/percpu.c）
- **链接**：https://docs.kernel.org/core-api/this_cpu_ops.html
- **核心内容**：为每个 CPU 维护独立数据副本，本地访问无锁、无 cache line bouncing。
- **解决的问题**：多 CPU 并发更新同一计数器导致的 cache line bouncing（MESI 无效化风暴）
- **为什么重要**：**这是"用空间换时间、用副本换锁"的极致**——计数器是最常见的共享数据，per-CPU 让计数器更新从"原子指令 + lock 前缀"变成"单指令无锁"。
- **技术亮点**：
  - **this_cpu_ops 黑科技**：x86 用 `gs:` 段寄存器前缀，`this_cpu_inc(x)` 编译为 `inc gs:[x]`——单指令、无 lock 前缀、无需关抢占
  - **段寄存器重定位**：per-CPU 变量是偏移量不是地址，`gs:` 前缀自动加上当前 CPU 的 per-CPU 基址
  - **读-改-写无原子性问题**：因为只有当前 CPU 访问自己的副本，不需要同步
  - **代价**：需要全局值时必须遍历所有 CPU 求和（`percpu_counter_sum()`）
  - **远程写禁忌**：其他 CPU 写本地 per-CPU 数据会干扰 this_cpu RMW，强烈建议用 IPI 而非远程写
- **与 C++ 的关系**：用户态可以用 `thread_local` 实现类似机制，但 thread_local 是 per-thread 不是 per-CPU（线程可能迁移）；folly 有 `ThreadCached` 等类似模式
- **与 CPP-Bible 的关系**：CONC/PERF 交叉域"消除 false sharing"的核心技术；与第七轮 ARM 内存模型形成"软件优化 vs 硬件模型"的对照
- **可以放入哪个章节**：part09_concurrency、part18_perf、part16_os
- **适合讲什么**：false sharing、cache line bouncing、per-CPU 优化、this_cpu_ops
- **可以设计什么实验**：全局原子计数器 vs per-CPU 计数器的性能对比（多线程递增，测量吞吐量）
- **可信度**：S（Linux 内核官方文档）
- **教材价值**：A+

---

## 二、其他高价值资料（A 级）

### 4. False Sharing（伪共享）

- **类型**：性能问题（内核文档 + 真实修复案例）
- **来源**：Linux Kernel（kernel-hacking/false-sharing.html）+ Red Hat 演讲
- **链接**：https://cdn.kernel.org/doc/html/latest/kernel-hacking/false-sharing.html
- **核心内容**：两个独立变量在同一 cache line，一个 CPU 写导致另一个 CPU 的 cache line 失效（MESI Invalidation）——即使它们逻辑上无关。
- **真实修复案例**：
  - `net: cache align tcp_memory_allocated, tcp_sockets_allocated`——两个计数器共享 cache line，分开到不同 cache line
  - `mm: page_counter: re-layout structure to reduce false sharing`——重排结构体字段
- **教学价值**：**这是"为什么需要 per-CPU 和 cacheline 对齐"的根因**。CPU 按 cache line（通常 64 字节）维护一致性，不是按变量。

### 5. seqlock 条件读（防饿死自适应策略）

- **类型**：内核 API 设计
- **来源**：Linux 内核 seqlock.h
- **核心内容**：`read_seqbegin_or_lock`——先试无锁读（序号偶），失败后序号变奇，下一次退化为排他锁读。这是"乐观尝试 + 悲观兜底"的自适应策略，避免写突发时读者无限重试。
- **教学价值**：**这是"自适应并发控制"的典范**——不是固定用无锁或有锁，而是根据竞争情况动态切换。

### 6. folly SequencedWriteLock（用户态 seqlock）

- **类型**：用户态库实现
- **来源**：Facebook Folly
- **核心内容**：folly 实现了用户态 seqlock，用于读多写少的场景。和内核 seqlock 原理相同，但用 C++11 原子操作实现。
- **教学价值**：从内核机制到用户态实现的对照——C++ 标准库没有 seqlock，但可以用 `std::atomic` 实现。

---

## 三、核心概念：乐观读的两种实现

```
seqlock（序号验证）：
  写者：序号++（变奇）→ 改数据 → 序号++（变偶）
  读者：读序号 → 读数据 → 读序号 → 两次相等且偶？有效 : 重试
  特点：原地更新，读者可能饿死，不保护指针

RCU（延迟回收）：
  写者：复制 → 修改副本 → 发布新指针 → 等 grace period → 释放旧版
  读者：rcu_read_lock → 读指针 → 用数据 → rcu_read_unlock
  特点：写时复制，读者不饿死，保护指针不释放
```

**共同本质**：读者无锁——但实现无锁读的方式完全不同。

---

## 四、Linux 读多写少同步机制全景

| 机制 | 读端开销 | 写端开销 | 读者饿死 | 指针安全 | 适用场景 |
|---|---|---|---|---|---|
| rwlock | 原子操作 | 原子操作 | 可能（写者饿死） | 是 | 通用读写 |
| seqlock | 两次读+比较 | spinlock+序号×2 | 可能 | 否 | 小数据、写少且快 |
| RCU | 接近零 | spinlock+grace period | 不可能 | 是 | 指针数据、读极频繁 |
| per-CPU | 单指令无锁 | 需聚合 | 不可能 | 不适用 | 计数器、统计 |
| hazard pointer | 写 hazard slot | 扫描+回收 | 不可能 | 是 | 无锁数据结构 |

---

## 五、知识网络

```
读多写少同步
├── seqlock（序号验证）
│   ├── 奇偶序号机制
│   ├── 三种读者模式（无锁/锁读/条件读）
│   ├── 写者优先、读者可能饿死
│   └── 不保护指针（需 RCU 组合）
│
├── RCU（延迟回收）
│   ├── 写时复制 + grace period
│   ├── 读端零开销
│   ├── 保护指针不释放
│   └── 多种 flavor（memb/qsbr/mb/bp）
│
├── per-CPU（副本换锁）
│   ├── 每 CPU 独立副本
│   ├── this_cpu_ops（gs: 段寄存器）
│   ├── 消除 false sharing
│   └── 全局值需聚合
│
├── hazard pointer（对象级保护）
│   ├── 写 hazard slot
│   ├── 扫描回收
│   └── C++26 标准化
│
└── false sharing（根因）
    ├── cache line 64 字节
    ├── MESI 无效化风暴
    └── 解决方案：per-CPU / cacheline 对齐
```

---

## 六、本轮最重要的 10 个资料

| # | 资料 | 级别 | 核心价值 |
|---|---|---|---|
| 1 | Linux seqlock 官方文档 | S | 三种读者模式、奇偶序号 |
| 2 | seqlock vs RCU 对比 | S | 适用场景决策框架 |
| 3 | per-CPU this_cpu_ops | S | 段寄存器单指令无锁 |
| 4 | False Sharing 内核文档 | A+ | cache line bouncing 根因 |
| 5 | seqlock 条件读自适应 | A | 乐观+悲观兜底策略 |
| 6 | folly SequencedWriteLock | A | 用户态 seqlock 实现 |
| 7 | Linux 路径查找 RCU+seqlock | A | 两种机制组合使用 |
| 8 | percpu_counter 实现 | A | 计数器聚合的工程实现 |
| 9 | Red Hat false sharing 演讲 | A | 真实性能修复案例 |
| 10 | folly Hazptr（第三轮） | A+ | 对象级保护的另一条路 |

## 七、强烈建议深入研究的 5 个资料

1. **Linux seqlock.h 源码**——读三种读者模式的实现细节
2. **this_cpu_ops 官方文档**——理解段寄存器重定位的黑科技
3. **False Sharing 内核文档**——看真实修复 commit
4. **Linux 路径查找文档**——RCU + seqlock 组合使用的案例
5. **folly Hazptr + SequencedWriteLock**——用户态对照实现

## 八、适合直接进入 CPP-Bible 的资料

| 资料 | 进入方式 | 目标原子/章节 |
|---|---|---|
| seqlock | "乐观读的两种实现"对比 | CONC 域原子 |
| seqlock vs RCU 决策表 | 直接作为章级决策表 | CONC 域 |
| per-CPU + false sharing | "消除 false sharing"实验 | PERF 域原子 |
| this_cpu_ops 段寄存器 | "软件优化 vs 硬件模型"交叉 | CONC/PERF 交叉 |

## 九、对 CPP-Bible 的工程升级建议

1. **CONC 域新增"读多写少同步全景"章节**——rwlock/seqlock/RCU/per-CPU/HP 五种机制的对比和选择指南
2. **"乐观读的两种实现"对比实验**——seqlock（序号验证）vs RCU（延迟回收），用同一个读多写少场景对比
3. **PERF 域新增"false sharing"实验**——全局原子计数器 vs per-CPU 计数器的性能对比，可复现
4. **"没有银弹"教学**——seqlock 保护指针 = use-after-free 的反面案例

## 十、发现的知识空白

1. **seqlock 完全未覆盖**——全书只讲了 mutex/condition_variable，没讲乐观读
2. **per-CPU / false sharing 无内容**——PERF 域的核心优化技术缺失
3. **读多写少同步全景无对比**——没有五种机制的决策框架
4. **用户态 seqlock 实现无案例**——C++ 标准库没有，但可以用 atomic 实现
5. **"乐观+悲观自适应"策略无内容**——seqlock 条件读是很好的工程设计案例

## 十一、下一轮推荐搜索方向

1. **无锁数据结构正确性验证工具**——CDSChecker、Relacy、GenMC（并发域收尾）
2. **KCSAN（Kernel Concurrency Sanitizer）**——Linux 内核动态数据竞争检测，与 TSan 对比
3. **STL 域源码调研**——std::sort / std::vector / std::unordered_map 实现细节（换域）
4. **C++26 reflection / contracts**——C++26 其他重要特性（换域）
5. **Power 内存模型**——比 ARM 更弱（非 MCA），极端案例
6. **数据库并发控制**——MVCC、2PL、乐观并发控制（换域到数据库）

---

*本轮新增知识节点：seqlock、奇偶序号、乐观读、seqlock vs RCU、per-CPU、this_cpu_ops、false sharing、cache line bouncing、自适应并发控制。补齐了 CONC 域"读多写少同步全景"和 PERF 域"false sharing 优化"两个空白。八轮调研覆盖并发域从同步原语到性能优化的完整工程实践。*
