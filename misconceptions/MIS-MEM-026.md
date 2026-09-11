---
id: MIS-MEM-026
name: "shared_ptr 是线程安全的（所以怎么用都安全）"
level: deep
domain: MEM
trigger_patterns:
  - "shared_ptr 引用计数是原子的，所以 shared_ptr 线程安全"
  - "多线程里传 shared_ptr 不用加锁"
refutations:
  - "边界一（可实测）：控制块引用计数原子 ⇒ **各持副本**并发拷贝/销毁安全——实测 EV-MEM-034：4 线程 × 2000 次拷贝后 use_count 收敛回 1，且引用计数路径在工件里带 lock 前缀原子 RMW；但**同一个 shared_ptr 实例**的并发读写不原子（一线程读、另一线程写/重置同一实例即数据竞争），需外部同步或改用 C++20 的 std::atomic<std::shared_ptr<T>>"
  - "边界二：**被指对象本身**不原子——shared_ptr 只保护控制块计数，对象内部状态仍需自己的同步；把 shared_ptr 传进多个线程并不等于对象访问被串行化"
  - "边界三：`use_count()` 在并发下只是近似值（libstdc++ 实现为一次无锁 32 位读），不能当同步原语——不能在并发路径上用 `use_count()==1` 判'是否唯一持有'"
  - "对照：unique_ptr 连拷贝都不允许（copyable=0，实测 EV-MEM-035），工件零 lock 指令——'要不要付原子代价'在 unique_ptr 侧是**编译期**决定，在 shared_ptr 侧是运行期事实，两者都不能推出'对象访问安全'"
source: G5 第三批指令（SHARED-002）；ATOM-MEM-SHARED-002 / EV-MEM-034 / EV-MEM-035
related_atoms: [ATOM-MEM-SHARED-002, ATOM-MEM-SHARED-001, ATOM-MEM-WEAK-001]
---

# MIS-MEM-026 · "shared_ptr 是线程安全的"

**层级**：deep —— 结构性误解：把"引用计数原子"外推成"整个对象线程安全"。它不是记错一个细节，而是会让人在多线程代码里**省掉本该有的锁**（并发读写同一 shared_ptr 实例、或并发修改被指对象），后果是数据竞争与难以复现的 UB。

## 触发模式（学习者常这么说 / 这么写）
- "shared_ptr 引用计数是原子的，所以 shared_ptr 线程安全"
- "多线程里传 shared_ptr 不用加锁"

## 为什么它不成立
1. **边界一（可实测）**：控制块引用计数原子 ⇒ **各持副本**并发拷贝/销毁安全——实测 EV-MEM-034：4 线程 × 2000 次拷贝后 use_count 收敛回 1，且引用计数路径在工件里带 `lock` 前缀原子 RMW；但**同一个 shared_ptr 实例**的并发读写不原子（一线程读、另一线程写/重置同一实例即数据竞争），需外部同步或改用 C++20 的 `std::atomic<std::shared_ptr<T>>`
2. **边界二**：**被指对象本身**不原子——shared_ptr 只保护控制块计数，对象内部状态仍需自己的同步；把 shared_ptr 传进多个线程并不等于对象访问被串行化
3. **边界三**：`use_count()` 在并发下只是近似值（libstdc++ 实现为一次无锁 32 位读），不能当同步原语——不能在并发路径上用 `use_count()==1` 判"是否唯一持有"
4. **对照**：unique_ptr 连拷贝都不允许（`copyable=0`，实测 EV-MEM-035），工件零 lock 指令——"要不要付原子代价"在 unique_ptr 侧是**编译期**决定，在 shared_ptr 侧是运行期事实，两者都不能推出"对象访问安全"

## 正确理解
- 一句话判据：**"计数安全 ≠ 对象安全"**。shared_ptr 保证"引用计数不会因并发拷贝/销毁而错乱"，**不**保证"多线程同时访问它管的东西是安全的"。
- 三项自检：① 我并发读写的是**同一个 shared_ptr 实例**吗（是 ⇒ 要同步）？② 我并发访问的是**同一个被指对象**吗（是 ⇒ 对象自己要有同步）？③ 我用 `use_count()` 做并发判断吗（是 ⇒ 错，它只是近似值）？
- 机制层理解：控制块计数用 LOCK 前缀 RMW（`lock add` / `lock sub` / `lock xadd`；`weak_ptr::lock` 的提升路径还用 CAS 重试 `lock cmpxchg`）；而 `shared_ptr` 实例本身只是"对象指针 + 控制块指针"两个普通字段——字段读写没有原子性修饰。

## 出处与关联
- 出处：G5 第三批指令（SHARED-002）；ATOM-MEM-SHARED-002 / EV-MEM-034 / EV-MEM-035
- 关联原子：ATOM-MEM-SHARED-002、ATOM-MEM-SHARED-001、ATOM-MEM-WEAK-001
