# 第71章　策略设计 Policy-Based Design

⟶ Book/part06_templates/ch65_type_traits.md
⟶ Book/part12_patterns/ch140_policy_pattern.md

> 本章所有汇编证据由 **MinGW GCC 13.1.0**（`-std=c++23 -O2 -S -masm=intel`）真实提取，源码剖析行号取自该工具链安装的 libstdc++ 13.1.0 头文件。
> 立场标签：`[标准]`=标准条文，`[实现]`=编译器实现行为，`[平台]`=平台/ABI 相关，`[经验]`=工程经验。

## ① 学习目标

⟶ Book/part06_templates/ch70_tag_dispatch.md
⟶ Book/part06_templates/ch72_expression_templates.md


- 掌握 **Policy-Based Design**：把"可变的算法/行为"抽象为**策略类（Policy）**，作为宿主模板的**模板参数**（普通类型参数或模板模板参数），在编译期组合出定制类型。
- 理解**静态多态**与虚函数动态多态的本质区别：策略在编译期绑定、被完全内联，运行期**无 vtable 查表、无间接调用**（见 ⑩ 汇编证据）。
- 会用**模板模板参数**（`template <typename> class Policy`）把"类模板策略"注入宿主（如 `NewCreator` 模板）。
- 通过真实汇编确认：`-O2` 下策略方法被静态内联消除、运行期零间接调用；`-O0` 下每个**策略组合**生成独立 mangled 实例化符号。
- 识别 STL 中的策略参数：`std::vector<T,Allocator>`、`std::basic_string<C,Traits,Allocator>`、`std::shared_ptr<T,D>`（删除器）都是 Policy-Based。

## ② 本模板模式速查（名称 / 适用场景 / 核心结构 / 定义）

| 项 | 内容 |
|---|---|
| **名称** | 策略设计（Policy-Based Design） |
| **适用场景** | 需要"编译期可配置行为"的组件：容器分配器、线程安全模型、智能指针删除器、序列化格式、存储布局（Eigen）。避免为每种组合写派生类。 |
| **核心结构** | 宿主模板 `Host<T, Policy1, Policy2, ...>`；每个 Policy 是提供特定行为的类/类模板；宿主通过 `Policy::method()` 调用策略。 |
| **定义** | 将"一类可替换的行为"封装为策略类，通过**模板参数**在编译期注入宿主并组合；不同策略组合生成不同的具体类型（每个组合一份实例化）。 |

## ③ 核心结构与完整代码实现

```cpp
// 策略 1：线程策略（类型策略，无状态）
struct SingleThreaded { static void lock() {} static void unlock() {} };
struct MultiThreaded  { static void lock() {} static void unlock() {} };

// 策略 2：创建策略（类模板，作为模板模板参数传入）
template <typename T> struct NewCreator    { static T* create() { return new T(); } };
template <typename T> struct MallocCreator { static T* create() { return static_cast<T*>(std::malloc(sizeof(T))); } };

// 宿主模板：组合两个策略
template <typename T, template <typename> class CP, typename TP>
struct Widget {
    static T* make() {
        TP::lock();
        T* p = CP<T>::create();
        TP::unlock();
        return p;
    }
};

// 具体配置（策略组合 = 新类型）
using W1 = Widget<int, NewCreator,    SingleThreaded>;
using W2 = Widget<int, MallocCreator, MultiThreaded>;
```

```cpp
// 策略作为"类型参数"（非模板）：日志策略
struct NoLog { static void log(const char*) {} };
struct StdLog { static void log(const char* m) { std::puts(m); } };

template <typename T, typename LogPolicy = NoLog>
class Counter {
    T v{};
public:
    void inc() { ++v; LogPolicy::log("inc"); }
    T get() const { return v; }
};
using SilentCounter = Counter<int>;
using LoudCounter   = Counter<int, StdLog>;
```

```cpp
// 多策略组合：线程 + 创建 + 校验
template <typename T, typename ThreadPolicy, typename CreatePolicy, typename CheckPolicy>
class Resource {
public:
    static T* acquire() {
        ThreadPolicy::lock();
        T* p = CreatePolicy::template create<T>();
        ThreadPolicy::unlock();
        CheckPolicy::verify(p);
        return p;
    }
};
```

```cpp
// 策略可含状态（非纯静态）：引用计数策略
struct RefCount {
    int n = 0;
    void add() { ++n; }
    bool release() { return --n == 0; }
};
template <typename T, typename Ownership = RefCount>
class Handle {
    T* p; Ownership own;
public:
    Handle(T* q) : p(q) { own.add(); }
    ~Handle() { if (own.release()) delete p; }
};
```

## ④ 实例化机制（实例化点 / 两阶段查找）

- **策略组合进 mangled 名**：每个 `<T,Policy...>` 组合生成独立类型与实例化。实测 `-O0` 符号：`_ZN6WidgetIi10NewCreator14SingleThreadedE4makeEv`（`W1::make`，策略 `NewCreator`+`SingleThreaded`）与 `_ZN6WidgetIi13MallocCreator13MultiThreadedE4makeEv`（`W2::make`）——**策略类型被编码进 mangled 名**。
- **静态绑定、无 vtable**：策略方法（如 `CP<T>::create()`）在实例化时直接绑定到具体策略实现，编译器内联；运行期不存在虚表查表（对比 ⑩ 虚函数对照）。
- **两阶段查找**：`CP<T>::create` 是依赖型名字，按 ch60 ④ 两阶段规则解析；`CreatePolicy::template create<T>()` 需 `template` 关键字消除"<"歧义（③ 第三段）。
- **组合爆炸**：N 个策略各有 M 种选择 → 最多 M^N 种组合，每种一份实例化（代码体积代价，见 ⑲）。

```cpp
// 实例化示例：W1 与 W2 是不同类型（即便 T 相同）
static_assert(!std::is_same_v<W1, W2>);          // 不同策略组合 = 不同类型
static_assert(std::is_same_v<W1::make, T*(void)>); // make 是静态成员
```

## ⑤ 适用场景与选型

- **容器/数据结构**：`std::vector<T,Allocator>` 用分配器策略解耦内存来源（堆/池/共享内存）。
- **线程模型**：单线程 vs 多线程对象（如 `boost::shared_ptr` 的 `mutex` 策略）在编译期选定，单线程零锁开销。
- **智能指针删除器**：`std::unique_ptr<T,D>`、`std::shared_ptr<T,D>` 用删除器策略定制释放逻辑（文件句柄、数组、自定义释放）。
- **算法变体**：比较策略、哈希策略、校验策略（③ 第三段）。
- **vs 虚函数**：需要运行期动态切换行为用虚函数；行为在编译期已知且追求零开销用 Policy-Based。

```cpp
// 选型对比：静态策略 vs 虚函数
struct FastPolicy { static int run() { return 1; } };
struct SlowPolicy { static int run() { return 2; } };
template <typename P> int static_run() { return P::run(); }   // 编译期内联

struct VPoly { virtual int run() = 0; };
struct VFast : VPoly { int run() override { return 1; } };     // 运行期 vtable 查表
```

```cpp
// 选型：删除器策略（unique_ptr）
#include <memory>
auto fdel = [](FILE* f) { if (f) std::fclose(f); };
using FilePtr = std::unique_ptr<FILE, decltype(fdel)>;
FilePtr fp(std::fopen("x.txt", "r"), fdel);   // 自定义删除策略
```

## ⑥ 完整可运行示例（最小）

```cpp
// 编译：g++ -std=c++23 -O2 policy_demo.cpp -o policy_demo
#include <cstdlib>
#include <iostream>

struct ST { static void lock() {} static void unlock() {} };
struct MT { static void lock() {} static void unlock() {} };

template <typename T> struct NewC    { static T* create() { return new T(); } };
template <typename T> struct MallocC { static T* create() { return static_cast<T*>(std::malloc(sizeof(T))); } };

template <typename T, template <typename> class CP, typename TP>
struct Widget {
    static T* make() { TP::lock(); T* p = CP<T>::create(); TP::unlock(); return p; }
};

int main() {
    using A = Widget<int, NewC,    ST>;
    using B = Widget<int, MallocC, MT>;
    int* a = A::make();
    int* b = B::make();
    std::cout << (a != nullptr) + (b != nullptr) << '\n';   // 2
    delete a; std::free(b);
}
```

```cpp
// 日志策略最小示例
#include <iostream>
struct NoLog  { static void log(const char*) {} };
struct PrintLog { static void log(const char* m) { std::cout << m << '\n'; } };
template <typename T, typename L = NoLog>
struct Box { T v; void set(T x) { v = x; L::log("set"); } };

int main() {
    Box<int> silent; silent.set(1);            // 无输出
    Box<int, PrintLog> loud; loud.set(2);      // 输出 "set"
}
```

```cpp
// 删除器策略最小示例
#include <memory>
#include <cstdio>
int main() {
    auto del = [](int* p) { delete p; };
    std::unique_ptr<int, decltype(del)> up(new int(7), del);
    // 释放逻辑由删除器策略决定
}
```

## ⑦ 标准规定 [标准]

- `[temp.param]`：模板可声明**模板模板参数** `template <parameter-list> class|typename Name`，作为实参的必须是类模板（如 `NewCreator`）。
- `[temp.names]`：宿主模板 `Host<T, Policy>` 实例化时，每个 `Policy` 实参必须是**完整类型或类模板**（视形参种类）；策略方法调用遵守常规两阶段查找。
- `[class.template]`：策略若本身为类模板（如 `NewCreator<T>`），在宿主内通过 `Policy<T>::method()` 调用，依赖名需 `typename`/`template` 消歧（③、④）。
- **分配器/删除器要求**：`Allocator` 须满足 `Cpp17Allocator`（`allocate`/`deallocate`/`value_type`），`Deleter` 须可调用 `d(ptr)`——这些是策略类的"概念契约"（衔接 ch67）。

```cpp
// 标准：模板模板参数语法（C++17 起可用 typename 替代 class）
template <typename T, template <typename> typename CP>   // C++17 typename 等价 class
struct Host { using R = decltype(CP<T>::create()); };
```

```cpp
// 标准：依赖名消歧（template 关键字）
template <typename T, typename CP>
void f() { auto p = CP::template create<T>(); (void)p; }
```

## ⑧ GCC / Clang / MSVC 行为差异 [实现][平台]

- **策略内联行为**：三编译器都内联策略静态方法；差异在 devirtualization 启发式——GCC/Clang 对"单派生类可见"的虚函数会去虚拟化（⑩ 的 `use_virtual` 被优化成直接 `call`），但**Policy-Based 根本不生成 vtable**，任何情况都是直接静态调用。
- **代码体积**：策略组合多时，MSVC 的 COMDAT 折叠（/OPT:ICF）与 GCC/Clang 的 `--gc-sections` 都能剔除未用实例化；但组合爆炸仍会膨胀 `.text`。
- **模板模板参数匹配**：C++17 起模板模板参数可用 `typename`；旧 MSVC 对"默认模板实参一致性"检查更严，跨编译器策略类建议显式默认实参一致。

```cpp
// 各编译器对策略组合的实例化符号一致（Itanium ABI）
// GCC/Clang: _ZN6WidgetIi10NewCreator14SingleThreadedE4makeEv
// MSVC:      ?make@?$Widget@H$1?NewCreator@@... 装饰名不同，但同样每组合一份
```

## ⑨ 内存 / 对象模型

- **无 vtable**：Policy-Based 宿主（除非显式加 `virtual`）不含虚表指针，对象布局紧凑（对比含虚函数的等价类少 8 字节 vptr）。
- **策略静态内联**：策略方法是 `static` 或内联成员，实例化时被内联进宿主，运行期不携带策略对象（无状态策略零占用）。
- **代码段体积**：每个策略组合一份实例化（④ mangled 符号），`.text` 随组合数增长；但有状态策略（③ 第四段 `RefCount`）会使宿主对象包含策略成员（增加对象大小）。
- **EBO 影响**：若策略作基类（ch52），空策略受 EBO 优化占 0 字节；若作成员则至少 1 字节。

```cpp
// 内存对比：策略宿主无 vptr
struct VPoly { virtual ~VPoly() = default; };
static_assert(sizeof(VPoly) == 8);          // [平台] x64 含 vptr
static_assert(sizeof(W1) == 1);             // 空宿主（策略皆空/静态）占 1 字节
```

```cpp
// 有状态策略增加对象大小
static_assert(sizeof(Handle<int>) > sizeof(int*));   // 含 RefCount 成员
```

## ⑩ 汇编 / 符号证据（真实 MinGW GCC 13.1.0，-O2 -masm=intel）

测试文件 `Examples/_asm_policy.cpp`，编译：`g++ -std=c++23 -O2 -S -masm=intel _asm_policy.cpp -o _asm_policy.asm`。

**`use_policy()` 主体（关键片段）**：

```asm
_Z10use_policyv:
    sub     rsp, 32
    mov     ecx, 4
    call    malloc                  ; W2::make 的 MallocCreator 策略内联 → 直接 call
    mov     rbx, rax
    mov     rcx, rax
    call    free                    ; 直接 call free（无间接）
    cmp     rbx, 1
    mov     eax, 1
    sbb     eax, -1                 ; 返回 2（两个 create 均非空）
    add     rsp, 32
    ret
```

**`use_virtual()` 主体（虚函数对照，即使被 devirtualize 仍留 vtable 取指）**：

```asm
_Z11use_virtualR5VBase:
    lea     rdx, _ZN4VNew4makeEv[rip]
    mov     rax, QWORD PTR [rcx]    ; ← 取 vtable 指针（对象首 8 字节）
    mov     rax, QWORD PTR [rax]    ; ← 取 vtable[0] = make 偏移
    cmp     rax, rdx
    jne     .L5
    mov     ecx, 4
    call    _Znwy                   ; operator new（编译器证明类型后才内联）
    ...
```

**结论（[实现]）**：
1. `use_policy` 中 `W1::make`/`W2::make` 的策略（`lock`/`unlock` 空函数、`create`=new/malloc）被**完全静态内联**，运行期只有 `call malloc`/`call free` 直接调用，**无任何 vtable 取指或间接跳转**。
2. `use_virtual` 即便 GCC 做了去虚拟化（devirtualization），仍保留 `mov rax,[rcx]; mov rax,[rax]` 的 **vtable 查表结构**；跨 TU/多派生类时退化为 `call [rax]` 间接调用。Policy-Based 在**任何情形**下都不依赖 vtable。
3. 组合爆炸代价见 `-O0` 符号：每个策略组合独立实例化。

**`-O0` 策略组合 mangled 符号（验证每组合独立实例化）**：

```asm
.globl  _ZN6WidgetIi10NewCreator14SingleThreadedE4makeEv     ; W1 = NewCreator + SingleThreaded
.globl  _ZN6WidgetIi13MallocCreator13MultiThreadedE4makeEv   ; W2 = MallocCreator + MultiThreaded
```

## ⑪ STL 中的该模式

- **`std::vector<T,Allocator>`**：`Allocator` 是内存分配策略（默认 `std::allocator`），可替换为池分配器、栈分配器等（ch38）。
- **`std::basic_string<C,Traits,Allocator>`**：`Traits`（字符特性策略：比较/长度/赋值）与 `Allocator`（内存策略）双策略组合（见 ⑮）。
- **`std::shared_ptr<T,D>` / `std::unique_ptr<T,D>`**：`D` 是删除器策略，定制释放逻辑（文件、数组、自定义资源）。
- **`std::regex`**：`Traits` 策略参数定制字符类别识别。

```cpp
// 复用 STL 策略：自定义分配器的 vector
#include <vector>
#include <memory>
std::vector<int, std::allocator<int>> v1;     // 默认堆分配策略
// std::vector<int, MyPoolAllocator> v2;       // 自定义池策略（Policy-Based 典型）
```

```cpp
// 复用 STL 策略：unique_ptr 删除器
#include <memory>
auto arr_del = [](int* p) { delete[] p; };
std::unique_ptr<int[], decltype(arr_del)> buf(new int[10], arr_del);  // 数组删除策略
```

## ⑫ 变体（variant patterns）

- **Policy-Based vs CRTP**（ch51/57）：CRTP 用派生类作为模板参数做"静态接口回调"；Policy-Based 用"独立策略类"做行为注入。二者常结合：宿主以 CRTP 调派生，派生再以 Policy 注入行为。
- **Policy-Based vs 虚函数**：前者编译期静态多态（零开销、代码膨胀），后者运行期动态多态（vtable 间接、可运行时切换）。
- **Policy-Based + Concepts**（ch67）：用 `requires` 约束策略满足契约（`Allocator`/`Deleter` 概念），错误更早更清晰。
- **策略链（Chain of Policies）**：多个策略按固定顺序组合，前一策略的输出作后一输入（如 `Threading → Creation → Checking`）。

```cpp
// 变体：Policy-Based + CRTP 组合
template <typename Derived, typename LogP>
struct BaseCRTP {
    void run() { static_cast<Derived*>(this)->impl(); LogP::log("run"); }
};
struct MyImpl : BaseCRTP<MyImpl, NoLog> { void impl() { /* ... */ } };
```

```cpp
// 变体：用 concept 约束策略契约（C++20）
template <typename P>
concept CreatorPolicy = requires { P::template create<int>(); };
template <typename T, CreatorPolicy CP>
struct Widget2 { static T* make() { return CP::template create<T>(); } };
```

```cpp
// 变体：策略链
template <typename A, typename B>
struct Chain { static void go() { A::step(); B::step(); } };
```

## ⑬ 反模式（anti-patterns）

- **过度策略化（组合爆炸）**：把每个微小差异都做成策略，导致 M^N 组合、`void` 膨胀、编译变慢。应只对**真正可变且独立**的轴做策略。
- **有状态策略引发耦合**：策略含可变性状态却以 `static` 方法暴露，导致线程不安全或语义错误；应明确策略是无状态（静态）还是有状态（成员）。
- **策略间隐式依赖**：策略 A 假定策略 B 已初始化某资源却不文档化，组合时崩溃。策略契约应在注释/concept 中明确。
- **忘记 `template` 关键字**：在宿主内调 `Policy<T>::create()` 漏 `template`，模板内编译错误。

```cpp
// 反模式：组合爆炸（4 策略各 3 选 = 81 种类型）
// template <typename T, typename P1, typename P2, typename P3, typename P4> class X;
// 实际多数组合无用 → 编译慢、体积大
```

```cpp
// 反模式：漏 template 关键字
// template <typename T, typename CP>
// void bad() { auto p = CP::create<T>(); }   // [标准] 错误：需 CP::template create<T>()
template <typename T, typename CP>
void good() { auto p = CP::template create<T>(); (void)p; }
```

```cpp
// 反模式：有状态策略误用 static
struct BadState { static int counter; static void tick() { ++counter; } };  // 全局共享，非每对象
```

## ⑭ 工业案例

- **智能指针删除器**：`std::unique_ptr<FILE, fclose_deleter>` 用删除器策略管理非内存资源（文件、句柄、连接）。
- **游戏引擎内存池**：对象分配器策略切换（堆/帧分配器/池），热路径用无锁策略，冷路径用通用策略（性能 ch19/43）。
- **Eigen 存储顺序**：`Matrix<float,3,3,RowMajor>` 用存储策略（行主序/列主序）影响循环展开与 SIMD（ch72 表达式模板结合）。
- **序列化框架**：编码策略（二进制/JSON/XML）作为模板参数，公共 `serialize(T)` 入口按策略分派。

```cpp
// 工业案例：文件句柄的删除器策略
#include <memory>
#include <cstdio>
struct FClose { void operator()(FILE* f) const { if (f) std::fclose(f); } };
using FilePtr = std::unique_ptr<FILE, FClose>;
FilePtr open_log(const char* p) { return FilePtr(std::fopen(p, "w")); }
```

```cpp
// 工业案例：线程模型策略（单线程零锁）
template <typename T, typename ThreadP>
class SafeQueue {
    void push(T v) { ThreadP::lock(); /* ... */ ThreadP::unlock(); }
};
// SafeQueue<int, SingleThreaded> 单线程版无锁开销；SafeQueue<int, Mutexed> 多线程版加锁
```

```cpp
// 工业案例：Eigen 式存储策略
template <typename T, int Rows, int Cols, int Options>
class Mat {
    static constexpr bool row_major = Options & 0x1;   // 存储顺序策略（位标志）
    T data[Rows * Cols];
};
using RM = Mat<float, 3, 3, 0x1>;   // 行主序策略
using CM = Mat<float, 3, 3, 0x0>;   // 列主序策略
```

## ⑮ 源码剖析（libstdc++ 相关）

**剖析 1：`std::basic_string` 的双策略参数（Traits + Allocator）**（`bits/basic_string.h`）

```cpp
// 文件：C:/Qt/Tools/mingw1310_64/lib/gcc/x86_64-w64-mingw32/13.1.0/include/c++/bits/basic_string.h
// 行号：85（class basic_string 模板参数）
template <typename _CharT,
          typename _Traits = char_traits<_CharT>,        // ← 字符特性策略
          typename _Alloc  = allocator<_CharT>>           // ← 内存分配策略
class basic_string { /* ... */ };
// char_traits 定义见 bits/char_traits.h 行 111（主模板）/ 347（char 特化）
```

**剖析 2：`std::allocator` 作为默认策略**（`bits/allocator.h`）

```cpp
// 文件：C:/Qt/Tools/mingw1310_64/lib/gcc/x86_64-w64-mingw32/13.1.0/include/c++/bits/allocator.h
// 行号：130（class allocator : public __allocator_base<_Tp>）
template <typename _Tp>
class allocator : public __allocator_base<_Tp> {
    using value_type = _Tp;
    _Tp* allocate(size_type __n);      // ← 分配策略方法
    void  deallocate(_Tp* __p, size_type __n);
};
// allocator_traits 主模板（统一策略接口）见 bits/alloc_traits.h 行 105
```

**剖析 3：`allocator_traits` 把任意策略归一化**（`bits/alloc_traits.h`）

```cpp
// 文件：C:/Qt/Tools/mingw1310_64/lib/gcc/x86_64-w64-mingw32/13.1.0/include/c++/bits/alloc_traits.h
// 行号：105（struct allocator_traits）
template <typename _Alloc>
struct allocator_traits {
    using allocator_type = _Alloc;
    static typename _Alloc::pointer allocate(_Alloc& __a, size_type __n);
};   // 任何满足 allocate/deallocate 的类都可作为策略传入容器
```

**小结**：STL 是 Policy-Based 的最大实践场——`basic_string` 用 `Traits`+`Allocator` 两个策略参数解耦"字符语义"与"内存来源"；`allocator_traits`（行 105）把任意分配策略归一化为统一接口，正是 ③ 中"策略契约"的标准库实现。

## ⑯ 易错点

- **模板模板参数必须传类模板**：`Widget<int, NewCreator, ...>` 中 `NewCreator` 必须是 `template <typename> class`，普通类（即使有成员模板）不符（见本取证最初编译错误）。
- **`template` 消歧**：宿主内调用 `Policy<T>::create()` 须写 `Policy::template create<T>()`，否则 `<` 被解析为小于号。
- **策略对象生命周期**：无状态策略用 `static` 方法、零占用；有状态策略须作为成员持有，否则状态丢失（⑬）。
- **二进制兼容**：不同策略组合的宿主是不同类型，不能在同一 ABI 边界混用（如 `W1*` 不能指向 `W2` 对象）。

```cpp
// 易错点：模板模板参数误传普通类
// using Bad = Widget<int, NewCreatorInst, ST>;  // 若 NewCreatorInst 非类模板 → 编译错误
// 应为类模板 NewCreator（template <typename> struct）
```

```cpp
// 易错点：template 关键字
template <typename T, typename P>
void use() {
    // P::create<T>();          // [标准] 错误
    P::template create<T>();    // OK
}
```

## ⑰ FAQ

- **Q：Policy-Based 和 CRTP 什么区别？** A：CRTP 是"宿主以派生类为模板参数、静态回调派生方法"；Policy-Based 是"宿主以独立策略类为参数、注入行为"。CRTP 解决接口/静态多态，Policy-Based 解决行为组合。可叠加（⑫）。
- **Q：策略必须是无状态的吗？** A：不必。无状态策略用 `static` 方法（零占用、可大量组合）；有状态策略作成员（增加对象大小，但可携带运行时配置）。
- **Q：Policy-Based 会增加编译时间吗？** A：会。每个策略组合独立实例化（④），组合多时编译变慢、体积膨胀（⑬/⑲）。应控制策略轴数量。
- **Q：何时不用 Policy-Based？** A：行为需运行期动态切换、或组合维度很少且变化频繁时，虚函数/函数指针更合适；或策略组合爆炸得不偿失时。

```cpp
// FAQ 演示：策略组合是不同类型，不能混用
W1 x;
// W2* p = &x;   // 错误：W1 与 W2 是不同的、不相关的类型
```

## ⑱ 最佳实践

- 只对"真正独立且多变"的行为轴抽成策略；避免组合爆炸（⑬）。
- 策略契约用 concept（ch67）或文档明确（需要哪些方法/类型别名）。
- 优先无状态策略（静态方法），减少对象开销与耦合。
- 宿主只做"组合与转发"，具体算法放策略，保持单一职责。
- 复杂策略链用 CRTP/概念约束，确保组合合法（⑫）。

```cpp
// 最佳实践：策略契约用 concept 约束（C++20）
template <typename P>
concept ThreadPolicy = requires { P::lock(); P::unlock(); };
template <typename T, ThreadPolicy TP>
class Guarded {
    void op() { TP::lock(); /* ... */ TP::unlock(); }
};
```

```cpp
// 最佳实践：无状态策略 + 静态方法
struct NoopPolicy { static void apply() {} };   // 零占用、可任意组合
```

## ⑲ 性能（编译期 / 运行期）

- **运行期**：Policy-Based 在 `-O2` 下**完全内联、零 vtable 查表**（⑩），与手写专用代码性能等价；虚函数即便被 devirtualize 仍残留 vtable 取指结构。
- **编译期**：策略组合在实例化时确定，零运行期路由计算。
- **代价**：每个 `<T,Policy...>` 组合一份实例化（`.text` 体积）与一次模板实例化（编译时间）；组合爆炸时显著（⑬）。
- **对象大小**：无状态策略零占用（对比含 vptr 的虚基类少 8 字节，⑨）。

```cpp
// 性能对比：Policy-Based 内联消除 vs 虚函数间接调用
// use_policy（⑩）：call malloc / call free 直接调用，无 [vtable]
// use_virtual（⑩）：mov rax,[rcx]; mov rax,[rax]  vtable 查表后才 call
```

```cpp
// 体积代价：3 策略各 2 选 → 8 种实例化
// 应只暴露实际使用的组合，未用组合用 extern template 抑制（C++11）
```

## ⑳ 练习题 + 思考题 + 源码阅读路线（内化，无独立推荐阅读节）

**练习题**
1. 用 Policy-Based 实现一个 `SmartArray<T, IndexPolicy, CheckPolicy>`，`IndexPolicy` 决定下标计算（线性/环形），`CheckPolicy` 决定是否越界检查。
2. 把"比较策略"做成模板模板参数，实现可配置排序的 `Sorter<T, ComparePolicy>`。
3. 用 `std::unique_ptr<T,D>` 的删除器策略管理 `std::FILE*`，写 `open_file` 返回带 `fclose` 删除器的智能指针。
4. 对比同一功能用 Policy-Based 与虚函数实现，各编译 `-O2` 提取汇编，统计间接调用数差异。

**思考题**
- Policy-Based 的组合爆炸如何用"策略分组"（把相关策略合并为一个大策略）缓解？
- 为什么 `std::allocator_traits` 要存在？它如何降低容器对具体分配器策略的耦合（参考 ⑮）？
- CRTP + Policy-Based 组合时，派生类与策略类的职责边界应如何划分（避免两者都试图定义 `impl`）？

**源码阅读路线**
1. `<bits/basic_string.h>` 85 行：`basic_string` 的 `Traits`+`Allocator` 双策略参数设计。
2. `<bits/allocator.h>` 130 行 + `<bits/alloc_traits.h>` 105 行：`allocator` 默认策略与 `allocator_traits` 归一化接口。
3. `<bits/char_traits.h>` 111/347 行：`char_traits` 作为字符语义策略（比较/长度/赋值）。
4. `<bits/unique_ptr.h>`：删除器 `Deleter` 策略如何作为模板参数注入并默认 `default_delete`。


## 联合使用场景

| 关联章节 | 场景 | 组合方式 |
|---|---|---|
| [第70章](Book/part06_templates/ch70_tag_dispatch.md) | 模板约束/类型安全API | 本章提供概念，第70章提供实现 |
| [第72章](Book/part06_templates/ch72_expression_templates.md) | 独占所有权/工厂模式 | 本章提供概念，第72章提供实现 |
| [第65章](Book/part06_templates/ch65_type_traits.md) | 多态插件/框架扩展 | 本章提供概念，第65章提供实现 |
| [第140章](Book/part12_patterns/ch140_policy_pattern.md) | 配置解析/API响应 | 本章提供概念，第140章提供实现 |


## 真实开源项目参考（可查证链接）

> policy-based design 的工业实现——下列链接指向真实源码（L2 文件级）。

- **Loki（policy-based design 鼻祖）**：[snaewe/loki · include/loki](https://github.com/snaewe/loki/blob/master/include/loki) —— Alexandrescu《Modern C++ Design》的参考实现；`SmartPtr` 用 policy 组合 `Storage`/`Ownership`/`Conversion` 等，是「① 什么是 policy」的工业原点。
- **Boost.MPL（编译期策略组合）**：[boostorg/mpl · include/boost/mpl](https://github.com/boostorg/mpl/blob/develop/include/boost/mpl) —— 用 `inherit_linearly` + `lambda` 元函数把 policy 列表组合进宿主类，对应「② policy 组合」的元编程骨架。
- **Boost.Policy（指针策略）**：[boostorg · boost/pointer_cast.hpp](https://github.com/boostorg/boost/blob/develop/boost/pointer_cast.hpp) —— `dynamic_pointer_cast` 等的策略化指针转换，对应「③ 应用场景」中"用 policy 统一指针语义"。
- **Chromium `base::RefCounted` / 线程策略**：[chromium/chromium · base/memory](https://github.com/chromium/chromium/tree/main/base/memory) —— 用 policy 式模板参数（`RefCountedThreadSafeBase`）区分单线程/多线程引用计数策略，对应「④ 常见陷阱」中"policy 正交性"的工业反面教材（线程策略错误导致数据竞争）。

**常见陷阱 / 最佳实践**：
- policy 组合爆炸需"宿主类"显式暴露 `typedef`，否则难以调试实例化错误。
- policy 间正交性不足会产生意外交互，设计时需明确每个 policy 的职责边界；Chromium 的线程策略分离即为此类设计的工业级示范。

> 交叉引用：与 CRTP 见 [ch51](Book/part05_oo/ch51_crtp.md)；与 traits 见 [ch65](Book/part06_templates/ch65_type_traits.md)。

## 相关章节（交叉引用）

- **后续依赖**：`Book/part07_stl/ch76_stl_arch.md`（第76章　STL 架构与迭代器概念）—— 本章为其前置，建议后续延伸阅读。
- **相邻主题**：`Book/part06_templates/ch69_constexpr.md`（第69章　编译期计算：constexpr / consteval / constinit）—— 编号相邻、主题接续。
- **同模块**：`Book/part06_templates/ch60_template_basics.md`（第60章　模板基础与实例化（Template Basics & Instantiation））—— 同模块下的其他主题。

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

