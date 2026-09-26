# 644 D3 · 反例覆盖扫描报告

- 卡片总数：**27**  命中反例候选：**2**  覆盖率：**7%**

| 卡片 | 标题 | 候选数 |
|---|---|---|
| ATOM-CONC-FENCE-001 | 内存屏障（fence）只约束顺序，不提供原子性；屏障在循环体内才阻止消除，但屏障≠原子类型 | 0 |
| ATOM-CONC-LOCK-001 | 锁的代价与无锁的代价：高竞争下 CAS 的原子 RMW 代价可能超过 mutex，但依赖核数与竞争度 | 0 |
| ATOM-CONC-RACE-001 | 数据竞争是未定义行为；TSan 可检测，但『没被报 ≠ 没有』 | 0 |
| ATOM-HIST-AUTOPTR-001 | 别看 auto_ptr 的名字像智能指针：它的"拷贝"是转移，而 C++98 只能这么表达 | 1 |
| ATOM-LANG-INLINE-001 | inline 函数的定义必须跨 TU 一致：违反 ODR 是「无须诊断」的 UB，且形态由链接顺序与优化档决定 | 0 |
| ATOM-MEM-ALIGN-001 | 结构体有对齐与填充：成员按对齐排列插 padding，sizeof 含 padding；alignas 可控、memcpy 安全 | 0 |
| ATOM-MEM-ALLOC-001 | allocator：STL 容器的内存策略抽象 | 0 |
| ATOM-MEM-ALLOC-002 | 分配器策略的时空权衡：arena / pool / bitmap（元数据换灵活性） | 0 |
| ATOM-MEM-LEAK-001 | 内存泄漏的检测信号分层：为什么"ASan 没报"不等于"没泄漏" | 0 |
| ATOM-MEM-LEAK-002 | 泄漏检测的工具边界：报告与否不能等价于泄漏有无 | 0 |
| ATOM-MEM-MOVE-002 | 用 std::move 申报所有权转移，真正的搬运发生在移动构造里 | 0 |
| ATOM-MEM-NEW-001 | new/delete 是两层：new=分配+构造、delete=析构+释放；new[]/delete[] 必须配对，nothrow 失败返 null | 2 |
| ATOM-MEM-PERF-001 | 移动比拷贝快多少？收益只来自"掏空源对象"，无动态资源的类型移动=拷贝 | 0 |
| ATOM-MEM-PERF-002 | SSO：std::string 为什么短字符串不分配堆内存 | 0 |
| ATOM-MEM-PERF-003 | 小对象分配的真实开销：SSO 阈值不可移植 + 分配策略必须基准测量 | 0 |
| ATOM-MEM-PERF-004 | 伪共享：多线程"独立变量"为何慢 18 倍，以及对齐 padding 的代价 | 0 |
| ATOM-MEM-RAII-001 | 资源要绑在对象生命周期上：构造获取、析构释放，异常也安全 | 0 |
| ATOM-MEM-RAII-002 | Rule of 0/3/5：什么时候该写析构函数，什么时候不该 | 0 |
| ATOM-MEM-RVREF-001 | 别以为形参写成 T&& 就会自动移动：进了函数体，它是左值 | 0 |
| ATOM-MEM-SHARED-001 | std::shared_ptr 用引用计数共享所有权；但循环引用会泄漏，须用 weak_ptr 打破 | 0 |
| ATOM-MEM-SHARED-002 | shared_ptr 的线程安全边界与原子代价：控制块原子、对象不原子 | 0 |
| ATOM-MEM-UNIQUE-001 | std::unique_ptr 是唯一所有权智能指针：移动转移、拷贝删除、sizeof 等于裸指针 | 0 |
| ATOM-MEM-UNIQUE-002 | unique_ptr 自定义删除器与数组：删除器进不进类型系统 | 0 |
| ATOM-MEM-VALUE-001 | C++ 的值不是"左/右"二分：glvalue×rvalue 正交出 lvalue / xvalue / prvalue 三类 | 0 |
| ATOM-MEM-VALUE-002 | 引用折叠与完美转发：为什么 std::forward 不能省 | 0 |
| ATOM-MEM-WEAK-001 | std::weak_ptr 是非拥有观察者；用 weak_ptr 打破 shared_ptr 的循环引用 | 0 |
| ATOM-UB-GRAY-001 | 先分清副作用是 unsequenced 还是 indeterminately sequenced：前者是 UB，后者只是未指定 | 0 |

