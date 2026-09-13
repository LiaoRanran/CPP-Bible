# MIS-MEM-021（misconception）

## 正面

【误解】MIS-MEM-021 allocator 就是 new/delete 的包装（低估它作为内存策略抽象的地位）
触发说法：allocator 没什么用，就是帮你调 new/delete 的东西

## 背面

为什么错：实测 EV-MEM-027/028：把自定义 arena 策略（或 pmr 的 monotonic_buffer_resource）注入容器，16 次 push_back 零堆分配（heap_new=0 / upstream_allocs=0）——new/delete 包装做不到这一点，策略（从哪块内存、怎么回收）是 allocator 的本体，不是包装细节
反例 1：接口事实：C++17 起 std::allocator 只保留 allocate/deallocate 纯分配层（construct/destroy 移除为标准条文；EV-MEM-026 实测的是 allocate 零构造、构造/析构经 allocator_traits 显式走）——容器由此解耦'内存策略'与'对象生命周期'，内存池/共享内存/对齐内存/pmr 运行时多态（EV-MEM-028）都建立在这之上（见 ATOM-MEM-ALLOC-001）
关联原子：ATOM-MEM-ALLOC-001 ATOM-MEM-NEW-001
