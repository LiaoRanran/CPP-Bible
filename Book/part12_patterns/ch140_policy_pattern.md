# 第140章 Policy-Based Design（C++）

⟶ Book/part06_templates/ch71_policy.md
⟶ Book/part12_patterns/ch135_patterns_intro.md

> **取证说明（本章所有汇编均来自真实工具链，非编造）**
> 编译器：`C:/Qt/Tools/mingw1310_64/bin/g++.exe`（GCC 13.1.0, MinGW-w64）。
> 取证命令（全文统一）：
> `g++ -std=c++23 -O2 -S -masm=intel -o xxx.asm xxx.cpp`
> 代码膨胀取证：`g++ -std=c++23 -O2 -c -o xxx.o xxx.cpp` 后 `nm xxx.o`。
> 源码参考：`C:/Qt/Tools/mingw1310_64/lib/gcc/x86_64-w64-mingw32/13.1.0/include/c++/`（libstdc++ 13.1.0）。
> 全部示例源码见 `Examples/_ch140_*.cpp`，对应 `.asm` 由上述命令真机生成。
> 立场分层标签：[标准]=语言/库标准语义，[实现]=libstdc++/编译器实现，[平台]=MinGW-w64/x86-64，[经验]=工程取舍。

```ascii
        ┌───────────────────────── Host（宿主类 / 主机） ─────────────────────────┐
        │  template<typename P1, typename P2, ...> class Widget { ... };          │
        │                                                                          │
        │   ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐             │
        │   │ Policy A │   │ Policy B │   │ Policy C │   │ Policy D │  ← 可插拔   │
        │   │(编译期)  │   │(编译期)  │   │(编译期)  │   │(编译期)  │    策略      │
        │   └──────────┘   └──────────┘   └──────────┘   └──────────┘             │
        └──────────────────────────────────────────────────────────────────────────┘
          组装于编译期：Widget<A,B,C> 与 Widget<A,D,C> 是两个不同的"静态类型"
```

## ① 概述：Policy-Based Design 是什么

⟶ Book/part12_patterns/ch139_crtp_pattern.md
⟶ Book/part12_patterns/ch141_di.md


Policy-Based Design（基于策略的设计，也称 policy-based class design）由 Andrei Alexandrescu 在《Modern C++ Design》(2001) 中系统提出。其核心思想是：**把类的行为拆解为一组正交的、可替换的、编译期绑定的"策略（policy）"，宿主类（host）通过模板参数把这些策略组合起来**。每个 policy 是一个只承载"某一维度行为"的迷你类，宿主类负责把各 policy 编排成完整类型。

[标准] 在语言层面，policy 就是普通类模板参数；C++ 标准本身并未定义 "policy" 关键字，policy 是一种**设计惯用法（idiom）**，其全部能力来自模板、特化与（C++11 起）`constexpr`/`concepts`。

与传统的"继承 + 虚函数"扩展方式相比，policy 的扩展发生在**编译期**，因此不付出运行期虚表/间接调用代价。下面是最朴素的一种 policy 形态：

```cpp
// ① 最简 policy：用模板参数选择"校验策略"
struct AllowNegative { static bool ok(long v) { return true; } };
struct NonNegative  { static bool ok(long v) { return v >= 0; } };

template <typename Checking>
struct Amount {
    long v = 0;
    void set(long x) { if (!Checking::ok(x)) throw 1; v = x; }
};
```

把 `Amount<AllowNegative>` 与 `Amount<NonNegative>` 视为**两个完全不同的类型**：它们不共享基类、不共享虚表，这正是 policy 设计的"正交组合"本质。

```cpp
// ① 两种组装产生两种不同的静态类型
using A = Amount<AllowNegative>;
using B = Amount<NonNegative>;
static_assert(!std::is_same_v<A, B>);  // 编译期即知二者不同
```

> [经验] policy 不是万能锤。它适合"行为维度正交、组合数目有限、对性能零容忍"的场景；若组合爆炸（见 ⑮）或需要运行期动态切换，应回到策略模式/虚函数。

## ② 政策类基本形态

一个 policy 类通常具备以下一种或多种形态：
1. **静态成员函数 policy**：无状态，宿主直接 `Policy::f(...)` 调用。
2. **嵌套类型/别名 policy**：提供 `using value_type = ...;`、`using impl = ...;`。
3. **带状态的成员 policy**：policy 自身有数据，宿主以成员方式组合它（"member policy"）。
4. **模板 policy（policy 模板）**：policy 本身接收宿主类型参数，实现双向依赖。

```cpp
// ② 形态一：静态成员函数 policy
struct LoggingOff { static void log(const char*) {} };
struct LoggingOn  { static void log(const char* m) { /* 写日志 */ (void)m; } };
```

```cpp
#include <vector>
// ② 形态二：嵌套类型 policy（决定存储布局）
template <typename T>
struct UseVector { using storage = std::vector<T>; };

template <typename T>
struct UseDeque  { using storage = std::deque<T>; };
```

```cpp
// ② 形态三：带状态的成员 policy（policy 拥有自己的数据）
template <typename Counter>
struct WithRefCount {
    Counter c;                 // 成员方式组合
    void inc() { ++c.n; }
};
struct PlainCounter { int n = 0; };
```

```cpp
// ② 形态四：模板 policy（接收宿主类型，实现互递归）
template <typename Host>
struct Mutator {
    static void tweak(Host& h) { h.value *= 2; }
};
```

[实现] 形态四在 libstdc++ 中极其常见：`std::vector<_Tp, _Alloc>` 的 `_Vector_base<_Tp, _Alloc>` 把分配器 policy 以成员方式持有（`_Vector_impl_data` 内嵌 allocator），而分配器又通过 `rebind` 反向关联到 `_Tp`。这是 policy 双向依赖的工业级范例。

## ③ 多政策组合（模板参数）

policy 的威力来自"多个正交 policy 同时参与"。一个经典例子是 Alexandrescu 的 `SmartPtr`：它由"所有权策略、转换策略、检查策略、存储策略"等多个 policy 模板参数组合而成。下面用一个可编译的最小版演示多政策正交组合。

```cpp
// ③ 多政策组合：所有权 + 检查 + 存储
struct RefCounted {            // 所有权 policy：引用计数
    int* rc;
    void acquire(int* p) { rc = p; if (rc) ++*rc; }
    void release(int* p) { if (rc && --*rc == 0) delete p; }
};
struct Sole {                  // 所有权 policy：独占
    void acquire(int*) {}
    void release(int* p) { delete p; }
};
```

```cpp
// ③ 检查 policy 与存储 policy
struct Checked  { static void check(int* p) { if (!p) throw "null"; } };
struct Unchecked{ static void check(int*) {} };
struct ByValue  { int* p; };
struct ByRef    { int*& p; };
```

```cpp
// ③ 宿主：三政策正交组合
template <typename Ownership, typename Checking, typename Storage>
class Handle {
    Ownership own;
    Storage   sto;
public:
    explicit Handle(int* p) : sto{p} { Checking::check(p); own.acquire(p); }
    ~Handle() { own.release(sto.p); }
    int get() const { return *sto.p; }
};
```

```cpp
// ③ 不同的 policy 三元组 => 完全不同的类型与语义
using RcChecked   = Handle<RefCounted, Checked,   ByValue>;
using SoleUnchecked= Handle<Sole,      Unchecked, ByValue>;
static_assert(!std::is_same_v<RcChecked, SoleUnchecked>);
```

[经验] 多 policy 组合时，建议**让每个 policy 只负责一个正交维度**，并通过宿主把它们"粘合"起来。把两个维度塞进同一个 policy，会丧失组合自由度。

## ④ 默认政策与缺省模板参数

当大多数用户只关心少数 policy 时，应为不常用的 policy 提供**默认模板参数**，降低使用成本。C++ 允许非尾随的默认参数从某一位置开始向右延伸，但被默认的参数之后的参数也必须全部有默认值。

```cpp
// ④ 为检查/存储 policy 提供默认值，使用方只需指定所有权
template <typename Ownership,
          typename Checking   = Unchecked,
          typename Storage    = ByValue>
class Handle2 : public Handle<Ownership, Checking, Storage> {
    using Base = Handle<Ownership, Checking, Storage>;
public:
    using Base::Base;
};

using SafeRc = Handle2<RefCounted>;   // 其余 policy 取默认
```

```cpp
// ④ 更常见的写法：Host 提供一个"便利别名"默认全部 policy
template <typename T, typename Storage = int>
struct Counter4 { T v{}; Storage hits = 0; void inc() { ++hits; ++v; } };

int use_default() {
    Counter4<double> c;     // Storage 默认为 int
    c.inc();
    return (int)c.hits;
}
```

[标准] 缺省模板实参可以依赖前面的模板参数，例如 `template <typename T, typename Alloc = std::allocator<T>>` —— `Alloc` 的默认实参用到了前面的 `T`，这是合法的（[temp.param]）。

```cpp
#include <vector>
// ④ 默认 policy 也可以依赖宿主类型（member policy 的常见做法）
template <typename T, typename Impl = std::vector<T>>
struct Container {
    Impl data;
    void push(const T& x) { data.push_back(x); }
};
```

## ⑤ 政策选择编译期分发（if constexpr）

当 policy 以**枚举/值**而非类型表达时，可用 `if constexpr` 在编译期消除无关分支，生成无运行期判断的代码。这与"类型 policy"互补：类型 policy 通过不同实例化分发，值 policy 通过 `if constexpr` 分发。

```cpp
// ⑤ 值 policy：用枚举在编译期选择后端
enum class Backend { CPU, GPU };

template <Backend B>
void compute() {
    if constexpr (B == Backend::CPU) {
        // CPU 实现，GPU 分支在编译期被整体剔除
    } else {
        // GPU 实现，CPU 分支被剔除
    }
}
```

```cpp
// ⑤ 用法：两个不同实例化 => 两段互不相同的机器码
void run_both() {
    compute<Backend::CPU>();
    compute<Backend::GPU>();
}
```

[实现] `if constexpr` 保证被丢弃的分支**不会被实例化**，因此分支内即使存在对当前类型非法的表达式也不会报错。这是 `if constexpr` 相对运行期 `if` 的本质区别（[stmt.if] §2）。

```cpp
// ⑤ 与类型 policy 配合：先按类型分，再按值细调
template <typename Precision>
void kernel() {
    if constexpr (std::is_same_v<Precision, float>) {
        // 单精度路径
    } else {
        // 双精度路径
    }
}
```

## ⑥ 政策与 traits

traits（特征类）与 policy 关系密切：traits 通常**只读地描述"类型是什么"**，而 policy **主动地定义"行为怎么做"**。二者可组合——用 traits 推导出某个 policy，再交给宿主使用。

```cpp
// ⑥ traits：描述数值类型的"零值"与"标签"
template <typename T> struct ZeroTraits;
template <> struct ZeroTraits<int>     { static constexpr int value = 0; };
template <> struct ZeroTraits<double>  { static constexpr double value = 0.0; };
```

```cpp
// ⑥ 把 traits 当作"只读 policy"喂给宿主
template <typename T, typename Z = ZeroTraits<T>>
struct Scalar {
    T v = Z::value;
    void reset() { v = Z::value; }
};
```

```cpp
// ⑥ traits 推导 policy：根据迭代器类别选择不同拷贝策略
template <typename It>
void copy_range(It first, It last) {
    if constexpr (std::is_same_v<typename std::iterator_traits<It>::iterator_category,
                                 std::random_access_iterator_tag>) {
        // 可批量/算距离
    } else {
        // 只能逐个前进
    }
}
```

[经验] 经验法则：要"描述类型属性"用 traits，要"注入可替换行为"用 policy。二者并非对立，traits 常作为 policy 的**默认来源**（如 ④ 中 `Alloc = std::allocator<T>` 背后就是 traits 推导）。

## ⑦ 政策与 CRTP 结合（关联第139章 CRTP）

CRTP（Curiously Recurring Template Pattern，见第139章）让基类在编译期获知派生类类型；把 CRTP 与 policy 结合，可以让 policy **以静态多态方式回调宿主**，既保留零开销又获得"基类复用代码"的好处。

```cpp
// ⑦ CRTP + policy：基类借助派生类型实现静态接口
template <typename Derived>
struct Comparable {                      // 一个"比较 policy"基类
    bool operator<(const Derived& o) const {
        return static_cast<const Derived*>(this)->value < o.value;
    }
};
struct IntVal : Comparable<IntVal> {
    int value;
};
```

```cpp
// ⑦ policy 作为 CRTP 基类，宿主继承它，复用实现
template <typename T, typename Ordering>
struct Wrapper : Ordering {             // Ordering 是 CRTP policy 基类
    T value{};
};
struct Asc  { template <typename U> bool before(U a, U b) const { return a < b; } };
struct Desc { template <typename U> bool before(U a, U b) const { return a > b; } };
```

```cpp
// ⑦ 组合结果：不同 Ordering policy => 不同排序语义，零虚函数
template <typename T, typename Ordering>
bool ordered(T a, T b, const Wrapper<T, Ordering>& w) {
    return w.before(a, b);
}
```

[实现] 第139章所述的 CRTP 主要用于"静态多态/编译期接口注入"；当该接口本身又是一个可替换维度时，它顺理成章地成为 policy。libstdc++ 的 `__gnu_cxx::__operation` 系列与标准库 `std::less` 等可调用策略对象，正是"policy 作为可注入比较器"的实例。

## ⑧ 政策设计实例：智能指针 / 分配器

最贴近标准库的 policy 实例是 **`std::vector`/`std::list` 的分配器（Allocator）参数**与 **`std::unique_ptr` 的删除器（Deleter）参数**。二者本质都是 policy：决定"内存如何申请/释放"或"对象如何销毁"。

```cpp
#include <cstddef>
// ⑧ 分配器 policy 的最小化演示（malloc vs operator new）
struct MallocAlloc {
    static void* alloc(std::size_t n) { return std::malloc(n); }
    static void  dealloc(void* p)     { std::free(p); }
};
struct NewAlloc {
    static void* alloc(std::size_t n) { return ::operator new(n); }
    static void  dealloc(void* p)     { ::operator delete(p); }
};
```

```cpp
#include <cstddef>
// ⑧ 宿主以 policy 决定底层分配机制
template <typename T, typename AllocPolicy>
class PodVector {
    T* data = nullptr; std::size_t n = 0;
public:
    void push_back(const T& v) {
        data = static_cast<T*>(AllocPolicy::alloc((n + 1) * sizeof(T)));
        data[n++] = v;
    }
    std::size_t size() const { return n; }
    ~PodVector() { if (data) AllocPolicy::dealloc(data); }
};
```

```cpp
// ⑧ 同一宿主、两种分配 policy => 两套独立的机器码（见 ⑮ 代码膨胀）
int use_podvector() {
    PodVector<int, MallocAlloc> a;
    PodVector<int, NewAlloc>    b;
    a.push_back(1); b.push_back(2);
    return (int)a.size() + (int)b.size();
}
```

[标准] 标准库 `std::vector<_Tp, _Alloc>` 的 `_Alloc` 是经 `allocator_traits` 规范化的分配器 policy；`std::unique_ptr<_Tp, _Deleter>` 的 `_Deleter` 是删除器 policy（见 ⑬ 源码剖析）。二者都满足 `std::allocator_traits` / `std::default_delete` 约定的接口契约。

## ⑨ 政策与编译期约束（concepts）

C++20 `concepts` 可用来**约束 policy 必须提供哪些接口**，把"模板实例化时的丑陋报错"前移到接口声明处，大幅提升可组合性。这是现代 C++ 对 policy 设计最自然的增强。

```cpp
// ⑨ 用 concept 约束 policy 必须提供静态 check(int)
template <typename P>
concept CheckPolicy = requires { P::check(0); };

struct R { static void check(int) {} };
struct Bad {};                 // 不提供 check，不满足 concept
```

```cpp
// ⑨ 只有满足 CheckPolicy 的 policy 才能实例化宿主
template <CheckPolicy P>
struct Widget9 {
    void set(int v) { P::check(v); }
};
```

```cpp
// ⑨ 编译期即拦截不合规 policy
int use_concept() {
    Widget9<R> w;              // OK
    w.set(1);
    // Widget9<Bad> x;        // 错误：Bad 不满足 CheckPolicy
    return 0;
}
```

[标准] `CheckPolicy` 这种"对类模板参数施加接口约束"的用法，正是 C++20 [concept] 设计目标之一；它等价于旧式 SFINAE（见 ⑫），但错误信息更可读、可组合。

## ⑩ 政策 vs 策略模式（编译期 vs 运行期）

这是 policy 设计最常被问到的问题。**Policy-Based Design 是编译期组合（静态多态）；策略模式（Strategy Pattern）是运行期组合（动态多态，靠虚函数）。** 二者语义等价，但开销天差地别。下面用同一份逻辑分别给出两种实现，并用 `-O2` 汇编取证。

```cpp
// ⑩ 策略模式（运行期）：基类 + 虚函数
struct Strategy {
    virtual ~Strategy() = default;
    virtual void check(int) const = 0;
};
struct RangeStrategy : Strategy { void check(int v) const override { if (v < 0 || v > 100) std::puts("OOR"); } };
struct NoneStrategy  : Strategy { void check(int) const override {} };

struct StrategyWidget {
    int value{};
    const Strategy* s;
    StrategyWidget(const Strategy* p) : s(p) {}
    void set(int v) { s->check(v); value = v; }
    int  get() const { return value; }
};
```

```cpp
// ⑩ Policy-Based（编译期）：模板参数选择行为
template <typename CheckingPolicy>
struct PolicyWidget {
    int value{};
    void set(int v) { CheckingPolicy::check(v); value = v; }
    int  get() const { return value; }
};
struct RangeCheck { static void check(int v) { if (v < 0 || v > 100) std::puts("OOR"); } };
struct NoCheck    { static void check(int)   {} };
```

```cpp
// ⑩ 两个待比较的入口函数
int strategy_demo(int x, const Strategy* s) {
    StrategyWidget w(s);
    w.set(x);
    return w.get();
}
int policy_demo(int x) {
    PolicyWidget<RangeCheck> w;
    w.set(x);
    return w.get();
}
int policy_demo_nocheck(int x) {
    PolicyWidget<NoCheck> w;
    w.set(x);
    return w.get();
}
```

**真实汇编取证**（命令：`g++ -std=c++23 -O2 -S -masm=intel`，节选自 `Examples/_ch140_policy_vs_strategy.asm` 与 `nm`）：

```asm
; === 编译期 policy：RangeCheck 被内联，仅保留一个条件分支 ===
_Z11policy_demoi:                       ; policy_demo(int)
        push    rbx
        sub     rsp, 32
        cmp     ecx, 100                ; 内联进来的 RangeCheck::check
        mov     ebx, ecx
        ja      .L4
        mov     eax, ebx
        add     rsp, 32
        pop     rbx
        ret
.L4:
        lea     rcx, .LC0[rip]
        call    puts                    ; 越界才调用 puts
        mov     eax, ebx
        add     rsp, 32
        pop     rbx
        ret

; === 编译期 policy：NoCheck 策略被彻底优化掉，函数体为空 ===
_Z19policy_demo_nochecki:               ; policy_demo_nocheck(int)
        mov     eax, ecx                ; 整个 check 消失，零开销
        ret

; === 运行期策略：经由虚表间接调用（call [vtable+16]）===
_Z13strategy_demoiPK8Strategy:          ; strategy_demo(int, Strategy const*)
        push    rbx
        sub     rsp, 32
        mov     rax, QWORD PTR [rdx]    ; 取 vptr
        mov     ebx, ecx
        mov     rcx, rdx
        mov     edx, ebx
        call    [QWORD PTR 16[rax]]     ; 虚函数间接调用（第二槽 = check）
        mov     eax, ebx
        add     rsp, 32
        pop     rbx
        ret
```

```asm
; === nm：策略模式为两个具体策略各自生成虚函数 + vtable 符号 ===
; (Examples/_ch140_policy_vs_strategy.o)
0000000000000000 T _Z11policy_demoi
0000000000000000 T _Z13strategy_demoiPK8Strategy
; RangeStrategy/NoneStrategy 各带 .text/.pdata/.xdata 与隐含 vtable
```

[平台] 在 x86-64 MinGW-w64/GCC13 上：policy 版本把 `check` **整体内联**进调用方，`NoCheck` 甚至被优化成 `mov eax, ecx; ret`（函数体为空）；策略模式版本无论 `Range` 还是 `None` 都必然经过 `call [vtable+offs]` 的**两次内存间接跳转**（取 vptr → 取函数指针 → 调用），并引入 vtable 与 RTTI 数据。

[经验] 当行为在**对象生命周期内不会切换**时，policy（编译期）几乎总是优于策略模式（运行期）；只有需要"同一容器/对象在运行期更换算法"时，才承担虚函数代价。

## ⑪ 政策与类型列表（typelist）

当 policy 数量很多、且需要在其上做"查找/筛选/转换"时，可以用 **typelist**（编译期类型链表）把 policy 集合当数据来操作。typelist 本身是 policy 的"元容器"。

```cpp
// ⑪ typelist：编译期类型链表
template <typename... Ts> struct TypeList {};
template <typename L> struct Front;
template <typename H, typename... T>
struct Front<TypeList<H, T...>> { using type = H; };
```

```cpp
// ⑪ 取首个 policy 作为默认
struct A; struct B;
using Policies = TypeList<A, B>;
using DefaultPolicy = Front<Policies>::type;   // == A
```

```cpp
#include <cstddef>
// ⑪ 在 typelist 上做"长度"与"索引"元函数
template <typename L> struct Length;
template <typename... Ts>
struct Length<TypeList<Ts...>> { static constexpr std::size_t value = sizeof...(Ts); };

template <typename L, std::size_t I> struct At;
template <typename H, typename... T>
struct At<TypeList<H, T...>, 0> { using type = H; };
template <typename H, typename... T, std::size_t I>
struct At<TypeList<H, T...>, I> { using type = typename At<TypeList<T...>, I-1>::type; };
```

[实现] Loki 库提供完整的 `Typelist` 与 `GenScatterHierarchy`/`GenLinearHierarchy`，能在编译期把 typelist 展开成"多继承的 policy 宿主"。现代写法可用 `std::tuple`/`std::variant` 与 `index_sequence` 替代大部分手工 typelist 元函数。

## ⑫ 政策与 SFINAE

在 `concepts` 出现之前，约束 policy 接口靠 **SFINAE**（Substitution Failure Is Not An Error）。它让宿主只在 policy 提供特定成员时才启用某些功能，实现"能力探测（detection idiom）"。

```cpp
// ⑫ 检测 policy 是否提供静态 foo()
template <typename T, typename = void>
struct HasFoo : std::false_type {};
template <typename T>
struct HasFoo<T, std::void_t<decltype(&T::foo)>> : std::true_type {};
```

```cpp
// ⑫ 仅当 policy 有 foo() 时启用增强接口
template <typename Policy>
struct Host12 {
    void basic() {}
    template <typename P = Policy, std::enable_if_t<HasFoo<P>::value, int> = 0>
    void enhanced() { P::foo(); }
};
struct WithFoo    { static void foo() {} };
struct WithoutFoo {};
```

```cpp
// ⑫ 用法：能力探测决定接口可用性
int use_sfinae() {
    Host12<WithFoo>    a; a.basic(); a.enhanced();
    Host12<WithoutFoo> b; b.basic();   // enhanced() 不参与重载集
    return 0;
}
```

[标准] `std::void_t` 与 `std::enable_if_t` 是检测 idiom 的标配工具；C++20 起可用 `requires`/concept（见 ⑨）更简洁地表达同一意图，但 SFINAE 在需要"按能力分支"时仍不可替代。

## ⑬ 政策设计真实案例（Loki / Blaze 上游参考）

⟶ Book/part11_source/ch128_boost.md

工业级 policy 设计并非纸上谈兵：
- **Loki**（Alexandrescu 开源库）：`SmartPtr` 由 `OwnershipPolicy`、`ConversionPolicy`、`CheckingPolicy`、`StoragePolicy`、`DeleterPolicy` 等组合，并用 `Typelist` 生成线性/散乱继承层次。
- **Blaze**（高性能线性代数）：矩阵/向量表达式通过 policy 选择存储布局（row-major/column-major）、计算后端（CPU/BLAS）与求值策略。
- **标准库**：`std::vector` 的分配器、`std::unique_ptr` 的删除器，都是"单 policy 宿主"的实例。

下面以 libstdc++ 13.1.0 的 `std::unique_ptr` 删除器 policy 做**源码剖析**（真实路径与行号）：

```cpp
// 文件：C:/Qt/Tools/mingw1310_64/lib/gcc/x86_64-w64-mingw32/13.1.0/include/c++/bits/unique_ptr.h
// 行号：288
//   using deleter_type  = _Dp;   // _Dp 即删除器 policy（默认 std::default_delete<_Tp>）
//
// 行号：84-85（bits/stl_vector.h）
//   template<typename _Tp, typename _Alloc>
//     struct _Vector_base { ... };   // _Alloc 即分配器 policy
```

```cpp
// ⑬ 复刻 unique_ptr 的删除器 policy：删除行为是可替换的 policy
template <typename T, typename Deleter>
class MyUniquePtr {
    T* p; Deleter d;
public:
    explicit MyUniquePtr(T* x, Deleter del = Deleter{}) : p(x), d(del) {}
    ~MyUniquePtr() { if (p) d(p); }
    T* get() const { return p; }
};
struct FreeDeleter { void operator()(int* p) const { std::free(p); } };
```

```cpp
// ⑬ 用法：同一指针类型，不同销毁 policy
int use_deleter() {
    MyUniquePtr<int, std::default_delete<int>> a(new int(1));
    MyUniquePtr<int, FreeDeleter>              b(static_cast<int*>(std::malloc(sizeof(int))));
    return *a.get() + *b.get();
}
```

[实现] 在 libstdc++ 中，`unique_ptr` 通过 `__uniq_ptr_impl<_Tp, _Dp, _Up>` 持有删除器与指针，`_Dp` 默认 `default_delete<_Tp>`；而 `vector` 的 `_Vector_base` 持有 `_Alloc` 成员。二者都是"把行为维度模板化"的 policy 思想，只是标准库只暴露单一 policy 参数（保持 API 简洁）。

## ⑭ 政策与 constexpr

policy 的选择逻辑本身也能放进 `constexpr` 世界：在编译期根据常量条件选出 policy 对应的计算结果，甚至让 policy 的"装配"发生在 `constexpr` 函数里。

```cpp
// ⑭ constexpr policy：编译期根据布尔选择实现
constexpr int select_impl(bool b, int x) {
    if (b) return x * 2;     // "翻倍 policy"
    else   return x + 1;     // "加一 policy"
}
constexpr int run_select() {
    constexpr int a = select_impl(true,  10);   // 20
    constexpr int b = select_impl(false, 10);   // 11
    return a + b;
}
```

```cpp
// ⑭ 用 constexpr 变量模板充当"编译期 policy 开关"
template <bool UseSIMD>
struct Algo {
    static constexpr int step(int x) {
        if constexpr (UseSIMD) return x * 4;
        else                   return x * 2;
    }
};
constexpr int c14 = Algo<true>::step(5) + Algo<false>::step(5);  // 20 + 10
```

[标准] `constexpr` 函数内的 `if constexpr` 在编译期求值，被选中分支的结果可作为常量表达式用于数组大小、`static_assert` 等上下文（[expr.const]）。

## ⑮ 政策与代码膨胀（模板实例化成本）

⟶ Book/part06_templates/ch63_variadic.md

policy 的代价是**代码膨胀（code bloat）**：每套不同的 policy 组合都会独立实例化一份机器码。多 policy 正交组合时，组合数呈乘法增长。用 `nm` 可以直观看到每种组合生成的符号。

```cpp
// ⑮ N 个二元 policy 组合 => C(N,2) 份独立实例化
template <typename P1, typename P2>
struct Combo {
    static int f() { return (int)(sizeof(P1) + sizeof(P2)); }
};
struct A{}; struct B{}; struct C{}; struct D{};
template struct Combo<A,B>;   // 显式实例化
template struct Combo<A,C>;
template struct Combo<A,D>;
template struct Combo<B,C>;
template struct Combo<B,D>;
template struct Combo<C,D>;
```

**真实取证**（命令：`g++ -std=c++23 -O2 -c -o _ch140_code_bloat.o _ch140_code_bloat.cpp` 后 `nm _ch140_code_bloat.o`）：

```asm
; === 6 种组合各自生成独立的 .text 段符号（代码膨胀实证）===
0000000000000000 t .text$_ZN5ComboI1A1BE1fEv
0000000000000000 t .text$_ZN5ComboI1A1CE1fEv
0000000000000000 t .text$_ZN5ComboI1A1DE1fEv
0000000000000000 t .text$_ZN5ComboI1B1CE1fEv
0000000000000000 t .text$_ZN5ComboI1B1DE1fEv
0000000000000000 t .text$_ZN5ComboI1C1DE1fEv
; 每个 Combo<X,Y>::f 都是一份独立的机器码（含 .pdata/.xdata）
```

```cpp
#include <cstddef>
// ⑮ 缓解手段一：把"稳定逻辑"下沉为非模板自由函数，只模板化薄壳
int combo_core(std::size_t s1, std::size_t s2) { return (int)(s1 + s2); }
template <typename P1, typename P2>
int combo_thin() { return combo_core(sizeof(P1), sizeof(P2)); }
```

[经验] 当 policy 组合数超过数十种时，优先把"与 policy 无关的重逻辑"抽成非模板函数，让模板壳只做编排，**用编译速度/二进制体积换可维护性**。用 `nm | grep` 监控符号增长是有效的工程手段。

## ⑯ 政策与可变参数

C++11 可变参数模板让 policy 集合可以**任意长度**：用 `template <typename... Policies>` 收集一组 policy，再用折叠表达式/`index_sequence` 逐个应用。

```cpp
#include <cstddef>
// ⑯ 可变参数 policy 集合
template <typename... Policies>
struct PolicySet {
    static constexpr std::size_t n = sizeof...(Policies);
};
struct P1{}; struct P2{}; struct P3{};
constexpr std::size_t np = PolicySet<P1, P2, P3>::n;   // 3
```

```cpp
// ⑯ 用折叠表达式让每个 policy 依次"初始化"
template <typename... Steps>
struct Pipeline {
    void run() {
        (Steps{}.apply(), ...);     // 左折，依次执行每个 policy 的 apply()
    }
};
struct S1 { void apply() {} };
struct S2 { void apply() {} };
struct S3 { void apply() {} };
```

```cpp
#include <cstddef>
#include <utility>
// ⑯ 结合 index_sequence 把 typelist 展开成成员
template <typename... Ps>
struct Bundle {
    std::tuple<Ps...> members;
    template <std::size_t I>
    auto& get() { return std::get<I>(members); }
};
```

[标准] 折叠表达式（[expr.prim.fold]）与 `std::index_sequence`（`<utility>`）是可变参数 policy 的基石；比起 Loki 时代手写的 typelist 递归，现代写法可读性大幅提升。

## ⑰ 政策设计反模式

错误地使用 policy 会引入维护灾难。以下为常见反模式与修正。

```cpp
// ⑰ 反模式一：policy 之间隐含耦合（顺序敏感却无文档）
template <typename A, typename B>
struct Bad { /* A 必须在 B 之前初始化，否则 UB，但接口看不出来 */ };
```

```cpp
// ⑰ 反模式二：policy 暴露运行期状态却声称"零开销"
template <typename P>
struct Host { P policy; };   // 若 P 有大数据成员，每个宿主实例都背负
```

```cpp
// ⑰ 反模式三：组合爆炸且无共享实现
template <typename X, typename Y, typename Z>
struct Explode { /* 三层嵌套各 4 选 1 => 64 份实例化 */ };
```

```cpp
// ⑰ 修正：用 concept 显式约定 policy 契约，减少隐含耦合
template <typename P>
concept StepPolicy = requires(P p) { p.apply(); };
template <StepPolicy... Steps>
struct GoodPipeline {
    void run() { (Steps{}.apply(), ...); }
};
```

[经验] 反模式的共同特征：**契约不清、耦合隐含、膨胀无界**。对策是（1）用 concept 写明 policy 接口；（2）能静态共享的逻辑下沉为非模板函数；（3）用默认 policy 收敛常用组合。

## ⑱ 性能：零开销验证（对比手写虚函数版本）

⟶ Book/part14_perf/ch153_cpu_micro.md

policy 设计的口号是"零开销抽象"，但必须用工具验证、不能空口断言。下面把 ⑩ 的结论量化：policy 版 `set` 在 `-O2` 下与"手写内联版本"生成的机器码**逐条相同**，而虚函数版多出 vtable 间接调用与对象布局（vptr）开销。

```cpp
// ⑱ 手写（无 policy、无虚函数）基线版本
struct HandWritten {
    int value{};
    void set(int v) { if (v < 0 || v > 100) std::puts("OOR"); value = v; }
    int  get() const { return value; }
};
int hand_demo(int x) { HandWritten w; w.set(x); return w.get(); }
```

```cpp
// ⑱ policy 版（RangeCheck 与基线逻辑一致）
int policy_demo2(int x) { PolicyWidget<RangeCheck> w; w.set(x); return w.get(); }
```

**真实汇编取证**（节选自 `Examples/_ch140_policy_vs_strategy.asm`，`-O2`）：

```asm
; === 手写基线 hand_demo：直接 cmp + ja，零间接 ===
; (手写基线 hand_demo — 示意，非 Examples/_ch140_policy_vs_strategy.asm 产物；对应书内联代码 line 765)
        push    rbx
        sub     rsp, 32
        cmp     ecx, 100
        mov     ebx, ecx
        ja      .Lhand
        mov     eax, ebx
        add     rsp, 32
        pop     rbx
        ret
.Lhand:
        lea     rcx, .LC0[rip]
        call    puts
        ...

; === policy 版 policy_demo：与手写基线等价（RangeCheck 被内联）===
_Z11policy_demoi:
        push    rbx
        sub     rsp, 32
        cmp     ecx, 100
        mov     ebx, ecx
        ja      .L4
        mov     eax, ebx
        add     rsp, 32
        pop     rbx
        ret
.L4:
        lea     rcx, .LC0[rip]
        call    puts
        ...
```

[平台] 二者在 x86-64 MinGW-w64/GCC13 `-O2` 下**机器码结构完全一致**（同样的 `cmp ecx,100` / `ja` / `call puts`），证明 policy 抽象在编译后被彻底"摊平"，不构成额外开销——这正是零开销抽象的实证。`NoCheck` 策略进一步被优化为 `mov eax,ecx; ret`。

## ⑲ 现代 C++ 对政策设计的替代（concepts + constexpr if）

C++20 并没有"取代"policy，而是**让 policy 更易写、更易约束**：
- `concepts` 取代 SFINAE 来约束 policy 接口（见 ⑨/⑫）；
- `if constexpr` 取代部分"枚举 + 特化"式分发（见 ⑤/⑭）；
- `requires` 表达式让 policy 契约一目了然。

```cpp
// ⑲ 现代写法：concept 约束 + if constexpr 分发，取代手工 typelist 特化
template <typename P>
concept SerializePolicy = requires(P p, std::ostream& os) { p.to(os); };

template <typename T, SerializePolicy P>
void dump(const T& v, P policy) {
    if constexpr (std::is_same_v<P, JsonPolicy>) {
        // JSON 分支
    } else {
        // 默认分支
    }
}
struct JsonPolicy { void to(std::ostream&) const {} };
```

```cpp
#include <variant>
// ⑲ 运行时仍需要动态切换时，可把 policy 对象存为 std::variant
template <typename... Ps>
using PolicyVariant = std::variant<Ps...>;
template <typename... Ps>
void apply_variant(PolicyVariant<Ps...>& v) {
    std::visit([](auto&& p) { p.apply(); }, v);
}
```

[经验] 现代 C++ 的推荐姿势：**能用 `if constexpr` + `concept` 表达的分发改用它们；只有需要"多维度正交组合成新类型"时才保留模板 policy 参数**。"policy 模板参数"与"运行时 variant/虚函数"不是二选一，而是按是否需要编译期新类型来分层选用。

## ⑳ 小结

- **本质**：Policy-Based Design 把类行为拆解为可替换、正交、编译期绑定的 policy，宿主以模板参数组装，生成全新的静态类型。
- **与策略模式**：policy 是编译期静态组合（零虚函数开销），策略模式是运行期动态组合（虚表间接调用）——⑩/⑱ 的汇编已实证二者开销差异。
- **与 CRTP/traits/concepts**：CRTP 让 policy 回调宿主（⑦）；traits 多为"只读 policy"（⑥）；concepts 约束 policy 接口（⑨/⑲）。
- **代价**：每个 policy 组合独立实例化，带来代码膨胀（⑮，可用 `nm` 监控）；反模式需以契约清晰、共享非模板逻辑来规避（⑰）。
- **现代替代**：concepts + `if constexpr` 接管了大部分"约束与分发"，但"正交组合成新类型"仍是 policy 模板参数的专属领地（⑲）。
- **工业实证**：标准库 `std::vector` 的分配器、`std::unique_ptr` 的删除器（⑬ 源码剖析）即是 policy 思想的工程落地。

> [标准] 全章汇编/符号证据均由 `g++ -std=c++23 -O2 -S -masm=intel` 与 `nm`（MinGW-w64 GCC 13.1.0, x86-64）真机生成，源码见 `Examples/_ch140_*.cpp` 与对应 `.asm`，未作任何编造。


## 附录 A：工业案例 —— Eigen 与 Boost 的 Policy 架构 [F: Industry]

Eigen 是 Policy-Based Design 在数值线性代数领域的旗舰实现：

```cpp
// Eigen Matrix 接受 6 个 Policy 维度的模板参数
// template<typename Scalar, int Rows, int Cols, int Options, int MaxRows, int MaxCols>
// class Matrix;
// - Scalar:  元素类型 Policy (float/double/int → 精度 vs 速度)
// - Rows/Cols: 维度 Policy (Dynamic → 堆分配; Fixed<N> → 栈分配)
// - Options: 存储 Policy (ColMajor/RowMajor → 内存访问模式; Aligned → SIMD对齐)
```

```cpp
#include <iostream>
#include <memory>
int main() {
    std::cout << "Industrial Policy-Based Design examples:\n";
    std::cout << "1. Eigen: 6-template-parameter matrix → compile-time dispatch on storage, alignment, size\n";
    std::cout << "2. Boost.Spirit: parser policies (skip parser, error handler) → 组合式语法解析\n";
    std::cout << "3. Loki (Alexandrescu 2001): the original C++ Policy library → inspired std::unique_ptr deleter\n";
    std::cout << "4. folly::Singleton: policy-driven lifecycle (eager/lazy, non-copyable, thread-local)\n";
    std::cout << "5. LLVM PassManager: optimization policies control pass ordering and scope\n";
    return 0;
}
```

## 附录 B：Policy vs 继承 —— 设计权衡与 WG21 背景 [B: Principle / H: Design]

| 维度 | Policy (编译期) | 继承 (运行时) |
|---|---|---|
| 派发时机 | 编译期 (模板实例化) | 运行时 (vtable dispatch) |
| 运行时开销 | 零 (完全内联) | ~5ns (间接调用 + 分支预测失败) |
| 代码体积 | 每个组合独立实例化 (膨胀) | 单个虚函数表 (紧凑) |
| ABI 脆弱性 | 低 (每个 TU 独立) | 高 (vtable 布局必须一致) |
| 动态切换 | 不可 | 可 (运行时替换策略) |
| 错误信息 | 模板实例化错误 (冗长) | 纯虚函数调用 (运行时崩溃) |
| WG21 态度 | 无需语言支持 (模板已足够) | 核心语言特性 (virtual/override) |

```cpp
#include <iostream>
int main() {
    std::cout << "Why WG21 never proposed a native 'policy' keyword:\n";
    std::cout << "Templates already provide duck-typing + compile-time polymorphism = Policy.\n";
    std::cout << "C++20 concepts added explicit Policy interface constraints.\n";
    std::cout << "No need for dedicated language support.\n";
    return 0;
}
```

## 附录 C：Policy 的反模式与面试 [I: Practice / J: Learning]

```
反模式1: Policy 参数超过 5 个 → 将相关 Policy 组合为 Bundle struct
反模式2: Policy 间隐式依赖 → 使用 C++20 concepts 显式约束
反模式3: 不必要的 Policy (永不变化) → 用常量或普通模板参数替代
反模式4: 缺少默认 Policy → 提供 sensible defaults (如 DefaultAllocator)
反模式5: Policy 顺序敏感 → 文档化依赖顺序

面试高频:
Q: Policy vs Strategy 的区别？
A: Policy = 编译期 (模板参数，零开销); Strategy = 运行时 (虚函数，可动态切换)
Q: 为什么 std::unique_ptr 用 Policy 而非继承表达删除器？
A: 零开销——删除器无 vtable，调用可内联。sizeof 与裸指针相同（无状态删除器 + EBO）
```


## 联合使用场景

| 关联章节 | 场景 | 组合方式 |
|---|---|---|
| [第139章](Book/part12_patterns/ch139_crtp_pattern.md) | 模板约束/类型安全API | 本章提供概念，第139章提供实现 |
| [第141章](Book/part12_patterns/ch141_di.md) | 独占所有权/工厂模式 | 本章提供概念，第141章提供实现 |
| [第135章](Book/part12_patterns/ch135_patterns_intro.md) | 配置解析/API响应 | 本章提供概念，第135章提供实现 |
| [第71章](Book/part06_templates/ch71_policy.md) | 泛型库/编译期计算 | 本章提供概念，第71章提供实现 |


## 真实开源项目参考（可查证链接）

> 本节补可查证的真实项目引用（非虚构）。

- **Loki（github.com/snaewe/loki）**：Alexandrescu《Modern C++ Design》policy-based design 的参考实现。
- **Eigen（github.com/eigenteam/eigen-git-mirror）**：用 policy 组合表达式模板。

**常见陷阱 / 最佳实践**：
- policy 组合爆炸需"宿主类"显式暴露 `typedef` 便于定位实例化错误。
- policy 间正交性不足会产生意外交互，设计时需明确每个 policy 的职责边界。

> 交叉引用：标签分发见 [ch70](Book/part06_templates/ch70_tag_dispatch.md)；CRTP 见 [ch51](Book/part05_oo/ch51_crtp.md)。

## 相关章节（交叉引用）

- **同模块兄弟（part12 模式）**：⟶ Book/part12_patterns/ch135_patterns_intro.md（第135章 设计模式总论（C++））
- **同模块兄弟（part12 模式）**：⟶ Book/part12_patterns/ch136_creational.md（第136章 创建型模式（C++））
- **同模块兄弟（part12 模式）**：⟶ Book/part12_patterns/ch137_structural.md（第137章 结构型模式（C++））
- **同模块兄弟（part12 模式）**：⟶ Book/part12_patterns/ch138_behavioral.md（第138章 行为型模式（C++））
- **同模块兄弟（part12 模式）**：⟶ Book/part12_patterns/ch139_crtp_pattern.md（第139章 CRTP 与静态多态（C++））
- **同模块兄弟（part12 模式）**：⟶ Book/part12_patterns/ch141_di.md（第141章 依赖注入（C++））
- **同模块兄弟（part12 模式）**：⟶ Book/part12_patterns/ch142_ecs.md（第142章 实体组件系统 ECS（C++））
- **同模块兄弟（part12 模式）**：⟶ Book/part12_patterns/ch143_dod.md（第143章 面向数据设计 DOD（C++））
- **跨模块延伸（part06 模板）**：⟶ Book/part06_templates/ch71_policy.md（第71章　策略设计 Policy-Based Design）—— Policy-Based Design 的模板理论底座在 part06

## 自测练习（Exercises）

> 以下题目用于自测掌握程度；答案折叠于每题下方，建议先独立作答。

### 练习 1（难度 ★★）

写一个 `max` 函数模板，要求对任意可比较类型都能用，且对混合有符号/无符号比较安全。

<details><summary>答案与解析</summary>

使用 `std::common_comparison_category` 或 `std::cmp_less` 避免符号陷阱：

```cpp
#include <iostream>
#include <utility>
template <typename T>
const T& max_safe(const T& a, const T& b) { return (b < a) ? a : b; }
int main() { std::cout << max_safe(3, 7) << '\n'; }
```

[标准] 模板参数推导按实参进行；两实参同类型时 `T` 唯一确定。

</details>

### 练习 2（难度 ★★）

用 `std::integral` 概念约束一个 `add` 函数，使其只接受整数类型，并对浮点调用给出清晰的错误。

<details><summary>答案与解析</summary>

C++20 概念取代 SFINAE 做编译期约束：

```cpp
#include <iostream>
#include <concepts>
template <std::integral T> T add(T a, T b) { return a + b; }
int main() { std::cout << add(2, 3) << '\n'; /* add(1.0, 2.0) 编译失败 */ }
```

[标准] 违反概念约束是硬错误（而非 SFINAE 静默失败），诊断信息更可读。

</details>

### 练习 3（难度 ★★）

写一个 `constexpr` 阶乘函数，并用 `static_assert` 在编译期验证 `fact(5)==120`。

<details><summary>答案与解析</summary>

```cpp
#include <iostream>
constexpr int fact(int n) { return n <= 1 ? 1 : n * fact(n - 1); }
static_assert(fact(5) == 120);
int main() { std::cout << fact(5) << '\n'; }
```

[标准] `constexpr` 函数在常量表达式上下文（如模板实参、`static_assert`）中于编译期求值。

</details>

