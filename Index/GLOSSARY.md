# 术语库 · GLOSSARY

> 全书术语索引。每条含：定义 + 出现章节 + 关联术语。持续扩充。

## A
- **ABI（Application Binary Interface，应用二进制接口）**：决定编译产物如何互操作的底层约定（调用约定、名称修饰、结构体布局、异常展开）。C++ 无跨编译器稳定 ABI；Itanium C++ ABI 被 GCC/Clang 采用，MSVC 自有。⟶ ch11、ch51、ch54
- **ADL（Argument-Dependent Lookup，实参依赖查找）**：名字查找时连同实参所属命名空间一并搜索。支撑 `std::swap` 定制。⟶ ch24、ch115
- **API（Application Programming Interface）**：源码级接口约定。
- **AST（Abstract Syntax Tree，抽象语法树）**：编译器前端产出。⟶ ch127

## B
- **benchmark（基准测试）**：可重复的性能度量。⟶ ch151、ch156
- **BSS 段**：存放未初始化/零初始化全局变量的段。⟶ ch35

## C
- **Cache Line（缓存行）**：CPU 缓存与内存交换的最小单位，通常 64 字节。⟶ ch44
- **constexpr（常量表达式）**：编译期可求值的变量/函数说明符（C++11 起，C++14/17/20 放宽）。⟶ ch21、ch69
- **consteval（立即函数）**：强制编译期求值的函数（C++20）。⟶ ch21、ch69
- **constinit（常量初始化）**：保证静态初始化期完成（C++20）。⟶ ch21
- **Concepts（概念）**：对模板实参的谓词约束（C++20）。⟶ ch67
- **Coroutine（协程）**：可暂停/恢复的函数（C++20）。⟶ ch113、ch120
- **CRTP（Curiously Recurring Template Pattern，奇异递归模板模式）**：基类以派生类为模板实参，实现静态多态。⟶ ch57、ch73、ch139
- **copy elision（拷贝消除）**：编译器省略拷贝/移动构造。⟶ ch117

## D
- **data race（数据竞争）**：未同步的并发读写同一内存。⟶ ch102、ch108
- **deadlock（死锁）**：多线程互相等锁。⟶ ch104

## E
- **EBO（Empty Base Optimization，空基类优化）**：空基类不占空间的布局优化。⟶ ch58
- **exception safety（异常安全）**：不泄漏资源、不破坏不变式的保证等级。⟶ ch49

## F
- **False Sharing（伪共享）**：多核修改同一缓存行的不同变量，互相失效。⟶ ch44
- **fold expression（折叠表达式）**：对参数包二元运算展开（C++17）。⟶ ch64
- **free store（自由存储区）**：`new`/`delete` 管理的堆区域。⟶ ch37、ch38

## I
- **inline namespace（内联命名空间）**：成员对外可见如在外层命名空间，用于版本化 ABI。⟶ ch24
- **Itanium C++ ABI**：GCC/Clang 采用的 C++ ABI 规范。⟶ ch11、ch54

## L
- **lock-free（无锁）**：某线程崩溃系统仍前进。⟶ ch110
- **LTO（Link Time Optimization，链接时优化）**：跨 TU 优化。⟶ ch156

## M
- **memory order（内存序）**：原子操作对可见性的约束。⟶ ch108
- **move semantics（移动语义）**：资源所有权转移而非拷贝（C++11）。⟶ ch115
- **MRU / Mermaid**：图示工具，见 CONVENTIONS §4

## N
- **NRVO（Named Return Value Optimization）**：具名返回值优化。⟶ ch117
- **NUMA（Non-Uniform Memory Access，非一致内存访问）**：多插槽内存延迟不等。⟶ ch45

## O
- **ODR（One Definition Rule，单定义规则）**：每个实体全程序至多一个定义。违反致 UB/链接错误。⟶ ch19、ch60
- **object slicing（对象切片）**：派生对象赋给基类值对象丢失派生部分。⟶ ch51
- **ODR-use**：变量/函数被「以需要定义的方式使用」。⟶ ch19、ch21

## P
- **PMR（Polymorphic Memory Resource，多态内存资源）**：C++17 分配器模型（`std::pmr`）。⟶ ch122
- **PGO（Profile-Guided Optimization，基于剖面的优化）**：用训练运行指导优化。⟶ ch156
- **perfect forwarding（完美转发）**：保持值类别的转发。⟶ ch116
- **placement new**：在给定地址构造对象。⟶ ch39
- **POD / trivial type**：平凡类型概念。⟶ ch19、ch51

## R
- **RAII（Resource Acquisition Is Initialization，资源获取即初始化）**：构造获资源、析构释资源。⟶ ch47
- **Rule of Three / Five / Zero**：拷贝控制三/五法则与零法则。⟶ ch48
- **RVO（Return Value Optimization，返回值优化）**：返回临时对象省略拷贝。⟶ ch117

## S
- **SFINAE（Substitution Failure Is Not An Error，替换失败非错误）**：重载决议中模板替换失败不报错。⟶ ch66
- **seq_cst（sequential consistency，顺序一致性）**：最强内存序。⟶ ch108
- **SSO（Small String Optimization，短字符串优化）**：短字符串存栈内联缓冲。⟶ ch81
- **stack unwinding（栈展开）**：异常抛出后逐层析构。⟶ ch49

## T
- **TLB（Translation Lookaside Buffer，转址旁路缓冲）**：页表缓存。⟶ ch45
- **TMP（Template Metaprogramming，模板元编程）**：编译期计算。⟶ ch68
- **type traits（类型特性）**：编译期查询/变换类型的工具。⟶ ch65
- **TLS（Thread-Local Storage，线程局部存储）**：每线程独立变量。⟶ ch19、ch35

## U
- **UB（Undefined Behavior，未定义行为）**：标准未规定后果，后果不可预测。⟶ ch34
- **universal reference（万能引用）**：`T&&` 在类型推导上下文兼作左/右值引用。⟶ ch116

## V
- **vtable（虚函数表）**：存放虚函数指针的只读表。⟶ ch54
- **vptr（虚表指针）**：对象中指向 vtable 的隐藏指针。⟶ ch54

## W
- **WG21**：ISO C++ 标准委员会。⟶ ch02
- **wait-free（无等待）**：每线程有限步内完成。⟶ ch110

## 关联网络（节选）
- RAII → unique_ptr → shared_ptr → allocator → move → thread → mutex → future
- ODR → 模板实例化 → 链接 → 内联 → 头文件
- False Sharing → Cache Line → NUMA → 无锁
- Concept → requires → 约束 → 重载决议 → 错误可读性
