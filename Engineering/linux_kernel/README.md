# linux_kernel — Linux 内核 C 实战

平行核心章：Part0 C 篇 / `Book/part10_memory` `part11_concurrency` `part13_perf`。

- 蓝本：`docs/references/external/Linux内核极致详细手册.md`（已入库）
- 主参考：`std-c11`、`cert`、`book:krc`、`cppref:c/...`
- 计划内容：
  - 内核模块框架、kbuild、与用户态 C 的差异（无 libc、无浮点）
  - 内核链表 `struct list_head`（offsetof 宏技巧，呼应 Part0 A5）
  - 锁与并发：自旋锁 / 信号量 / RCU / 原子操作（对比 C++ `std::atomic` `[cppref:cpp/atomic]`）
  - 内存分配：`kmalloc`/`vmalloc`/`slab` 与 `malloc` 对比
  - 不知所措时：用 UBSan/ASan/Cocci 校验（`[ubsan]` `[asan]`）
- 引用键示例：`[std-c11]` `[cert:CONած]` `[cppref:c/memory]`
