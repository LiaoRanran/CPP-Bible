# MIS-MEM-026（misconception）

## 正面

【误解】MIS-MEM-026 shared_ptr 是线程安全的（所以怎么用都安全）
触发说法：shared_ptr 引用计数是原子的，所以 shared_ptr 线程安全

## 背面

为什么错：边界一（可实测）：控制块引用计数原子 ⇒ **各持副本**并发拷贝/销毁安全——实测 EV-MEM-034：4 线程 × 2000 次拷贝后 use_count 收敛回 1，且引用计数路径在工件里带 lock 前缀原子 RMW；但**同一个 shared_ptr 实例**的并发读写不原子（一线程读、另一线程写/重置同一实例即数据竞争），需外部同步或改用 C++20 的 std::atomic<std::shared_ptr<T>>
反例 1：边界二：**被指对象本身**不原子——shared_ptr 只保护控制块计数，对象内部状态仍需自己的同步；把 shared_ptr 传进多个线程并不等于对象访问被串行化
反例 2：边界三：`use_count()` 在并发下只是近似值（libstdc++ 实现为一次无锁 32 位读），不能当同步原语——不能在并发路径上用 `use_count()==1` 判'是否唯一持有'
关联原子：ATOM-MEM-SHARED-002 ATOM-MEM-SHARED-001 ATOM-MEM-WEAK-001
