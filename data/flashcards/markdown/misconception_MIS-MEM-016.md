# MIS-MEM-016（misconception）

## 正面

【误解】MIS-MEM-016 智能指针都自动安全：以为 shared_ptr 管了就绝不泄漏（忽略循环引用）
触发说法：用了 shared_ptr 就再也不会内存泄漏

## 背面

为什么错：shared_ptr 只在**非循环**的所有权图里自动释放；成环时引用计数永不为 0 → 泄漏（实测 EV-MEM-014 循环引用 destroyed count=0）
反例 1：打破循环须用 weak_ptr 旁观（不增计数）；把'自动管理'等同于'绝不泄漏'是误解 [smartptr.weakptr]（见 ATOM-MEM-SHARED-001 / ATOM-MEM-WEAK-001）
关联原子：ATOM-MEM-SHARED-001 ATOM-MEM-WEAK-001
