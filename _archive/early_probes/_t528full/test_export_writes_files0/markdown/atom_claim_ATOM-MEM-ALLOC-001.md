# ATOM-MEM-ALLOC-001（atom_claim）

## 正面

【MEM】ATOM-MEM-ALLOC-001
以下论断是否成立？依据是什么？
allocator 是 STL 容器的内存**策略**抽象：容器只经 allocator_traits 要内存，不直接调 new/delete。 C++17 后 std::allocator 只剩 allocate/deallocate 纯分配层（construct/destroy 移除、统一走 traits）， 分配与对象构造是两个独立动作。策略可整体替换：自定义 arena 分配器接入 vector 后 16 次 push_back 零堆分配；std::pmr（C++17）把策略变成运行时多态——monotonic_buffer_resource 用栈缓冲伺候全部 分配、全程不触碰上游。

## 背面

论断：allocator 是 STL 容器的内存**策略**抽象：容器只经 allocator_traits 要内存，不直接调 new/delete。 C++17 后 std::allocator 只剩 allocate/deallocate 纯分配层（construct/destroy 移除、统一走 traits）， 分配与对象构造是两个独立动作。策略可整体替换：自定义 arena 分配器接入 vector 后 16 次 push_back 零堆分配；std::pmr（C++17）把策略变成运行时多态——monotonic_buffer_resource 用栈缓冲伺候全部 分配、全程不触碰上游。
边界：{'standard': ['C++11', 'C++14', 'C++17', 'C++20', 'C++23'], 'compilers': ['GCC 15.3.0'], 'opt': ['-O0', '-O2'], 'platform': ['x86-64 MinGW-w64']}
关键证据：
  - EV-MEM-026: confirm
  - EV-MEM-027: confirm
  - EV-MEM-028: confirm
