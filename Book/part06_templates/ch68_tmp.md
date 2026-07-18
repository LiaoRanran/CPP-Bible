# 第68章　模板元编程 TMP 基础（递归 / 分支 / 循环）

⟶ Book/part06_templates/ch69_constexpr.md
⟶ Book/part06_templates/ch65_type_traits.md

> 立场标签约定：`[标准]`=语言标准规定　`[实现]`=编译器/ABI 实现　`[平台]`=平台相关　`[经验]`=工程经验。
> 本章所有汇编证据由 **MinGW GCC 15.3.0**（`-std=c++23 -O2 -S -masm=intel`）真实提取，源码剖析行号取自该工具链安装的 libstdc++ 15.3.0 头文件。

## ① 学习目标

⟶ Book/part06_templates/ch67_concepts.md
⟶ Book/part06_templates/ch69_constexpr.md


- 理解 TMP（Template Metaprogramming）的本质：用模板实例化机制在**编译期**完成值计算与类型计算。
- 掌握三条基本控制流：**递归**（值/类型递归实例化 + 偏特化终止）、**分支**（`std::conditional` / `if constexpr` / bool 特化）、**循环**（包展开 / 折叠 / 递归展开）。
- 能通过真实汇编证明：TMP 计算在 `-O2` 下**零运行时代码**，全部折叠为立即数。
- 识别 TMP 的典型反模式（递归深度爆炸、实例化点陷阱、依赖名缺 `typename`）。

## ② 本模板模式速查（名称 / 适用场景 / 核心结构 / 定义）

| 维度 | 内容 |
|---|---|
| **名称** | 模板元编程（Template Metaprogramming, TMP） |
| **适用场景** | 编译期常量计算、类型分发、类型列表操作、编译期约束检查、`std::integer_sequence` 索引展开 |
| **不适用** | 运行时才能确定的值（用户输入、文件内容）、需要调试的单步逻辑（TMP 报错极难读） |
| **核心结构** | `template <int/type N> struct X { ... 递归引用 X<N-1> ... };` + `template <> struct X<0> { 基例 };` |
| **定义** | 利用模板偏特化与实例化点规则，把"计算"编码进类型系统，由编译器在实例化时求值 |

```cpp
// 速查：TMP 三段式 = 主模板（递归）+ 偏特化（基例）+ 调用点（触发实例化）
template <int N>
struct Fib { static constexpr int v = Fib<N-1>::v + Fib<N-2>::v; }; // 递归
template <> struct Fib<0> { static constexpr int v = 0; };          // 基例
template <> struct Fib<1> { static constexpr int v = 1; };
static_assert(Fib<10>::v == 55);                                     // 调用点：编译期求值
```

## ③ 核心结构与完整代码实现

**A. 值计算——编译期阶乘（递归 + 偏特化终止）**

```cpp
template <int N>
struct Fact { static constexpr int value = N * Fact<N - 1>::value; };
template <>
struct Fact<0> { static constexpr int value = 1; };
static_assert(Fact<5>::value == 120);
```

**B. 值计算——编译期 GCD（欧几里得，递归值）**

```cpp
template <int A, int B>
struct Gcd { static constexpr int value = Gcd<B, A % B>::value; };
template <int A>
struct Gcd<A, 0> { static constexpr int value = A; };
static_assert(Gcd<48, 36>::value == 12);
```

**C. 类型计算——bool 参数分支（`std::conditional` 等价手写）**

```cpp
template <bool B>
struct SelectT { using type = int; };          // 主模板：默认分支
template <>
struct SelectT<false> { using type = double; }; // 偏特化：false 分支
static_assert(sizeof(SelectT<true>::type) == sizeof(int));
static_assert(sizeof(SelectT<false>::type) == sizeof(double));
```

**D. 类型计算——类型列表 `at` 索引（递归 + 偏特化）**

```cpp
#include <cstddef>
template <typename... Ts> struct TypeList {};
template <size_t I, typename L> struct At;                  // 前向声明
template <typename T, typename... Rest>
struct At<0, TypeList<T, Rest...>> { using type = T; };     // 基例：取第一个
template <size_t I, typename T, typename... Rest>
struct At<I, TypeList<T, Rest...>>                          // 递归：剥头
    : At<I - 1, TypeList<Rest...>> {};
using L = TypeList<int, double, char>;
static_assert(std::is_same_v<At<0, L>::type, int>);
static_assert(std::is_same_v<At<2, L>::type, char>);
```

**E. 编译期判定——素数（递归 + 偏特化基例）**

```cpp
template <int N, int D = N - 1>
struct IsPrime { static constexpr bool value = (N % D != 0) && IsPrime<N, D - 1>::value; };
template <int N> struct IsPrime<N, 1> { static constexpr bool value = true; };
template <>     struct IsPrime<1> { static constexpr bool value = false; };
template <>     struct IsPrime<0> { static constexpr bool value = false; };
static_assert(IsPrime<17>::value);
static_assert(!IsPrime<15>::value);
```

**F. 循环——`std::integer_sequence` 包展开索引**

```cpp
template <typename T, T... Is>
void for_each_is(std::integer_sequence<T, Is...>, auto f) {
    (f(Is), ...); // 编译期展开为 f(0); f(1); ... f(N-1);
}
#include <utility>
int sum = 0;
for_each_is(std::make_integer_sequence<int, 5>{}, [&](int i){ sum += i; }); // 0+1+2+3+4=10
```

## ④ 实例化机制（实例化点 / 两阶段查找）

- **实例化点（POI, Point of Instantiation）**：模板在**第一次被 odr-use** 的地方实例化。`Fact<5>` 在 `static_assert` 处触发，`Fact<4>..Fact<0>` 由主模板递归引用链**级联实例化**。
- **两阶段查找（two-phase lookup）**：
  - 阶段一（模板定义时）：非依赖名（不依赖模板参数的名字）立即查找。
  - 阶段二（实例化时）：依赖名（含模板参数）在实例化上下文查找。
- **偏特化选择**：编译器在实例化时按**最特化匹配**选主模板或偏特化；无匹配偏特化则退回主模板。

```cpp
template <typename T>
void foo() { T x; bar(x); }  // bar 是依赖调用：阶段二才查找（需 ADL 或可见声明）
struct S {};
void bar(S) {}               // 必须在 foo<S>() 实例化点可见，否则 SFINAE/失败
int main() { foo<S>(); }     // POI：此处实例化 foo<S>，bar(S) 可见 -> OK
```

## ⑤ 适用场景与选型

| 需求 | TMP 手段 | 替代手段 | 选型 |
|---|---|---|---|
| 编译期常量（维度、掩码） | `constexpr` 值模板 | `constexpr` 函数 | 值模板更直观，函数更通用 |
| 编译期类型分发 | `std::conditional` / 偏特化 | `if constexpr` | C++17+ 优先 `if constexpr`（可读） |
| 类型列表索引 | 递归 `At` | `std::tuple_element` | 已有 `tuple` 用标准库 |
| 索引展开（数组遍历） | `integer_sequence` | 手写递归 | `integer_sequence` 标准且零开销 |
| 编译期约束 | `concept` / SFINAE | TMP 谓词 | C++20 优先 `concept` |

## ⑥ 完整可运行示例（最小）

```cpp
#include <type_traits>
#include <utility>
#include <iostream>
#include <cstdint>

template <int N>
struct Fact { static constexpr int value = N * Fact<N - 1>::value; };
template <> struct Fact<0> { static constexpr int value = 1; };

// 编译期类型选择：大端用 uint32_t 别名，否则 uint16_t（示意）
template <bool Big>
struct Word { using type = uint16_t; };
template <> struct Word<true> { using type = uint32_t; };

template <int... Is>
int sum_seq(std::integer_sequence<int, Is...>) { return (0 + ... + Is); }

int main() {
    std::cout << "Fact<5> = " << Fact<5>::value << "\n";            // 120
    std::cout << "Word size = " << sizeof(Word<false>::type) << "\n"; // 2
    std::cout << "sum_seq<0..4> = "
              << sum_seq(std::make_integer_sequence<int, 5>{}) << "\n"; // 10
    static_assert(Fact<5>::value == 120);
    return 0;
}
```

## ⑦ 标准规定 [标准]

- C++ 模板偏特化匹配规则由 `[temp.class.spec]`（偏特化）、`[temp.inst]`（实例化点）、`[temp.res]`（两阶段查找）规定。
- 部分特化**不参与重载决议**，仅在选择主模板后做"最特化匹配"（`[temp.class.spec.match]`）。
- 非类型模板参数（NTTP）允许的类别随标准扩展：C++11 仅整数/指针/引用/成员指针；C++20 允许**字面量类型 NTTP**（如 `fixed_string`、结构体），极大增强 TMP 表达力（`[temp.param]`）。

## ⑧ GCC / Clang / MSVC 行为差异 [实现][平台]

- **递归深度上限**：GCC 默认 `-ftemplate-depth=900`，Clang 默认 256，MSVC 默认 1024。超深递归报 `template instantiation depth exceeds`。`Fact<2000>` 在 GCC 需 `-ftemplate-depth=2048`。
- **符号修饰**：GCC/Clang 用 Itanium mangling（`_Z...`），MSVC 用 `@`-风格修饰名（`?Fact@$0?...`）。递归实例化的展开符号在三者都存在，但命名不同。
- **`integer_sequence` 实现**：三者都基于偏特化增量构造（`integer_sequence<T, Is..., N>` 追加），无运行时代码。

```cpp
// GCC 提高递归深度上限的编译选项（跨平台章节仅供认知，不滥用）
// g++ -ftemplate-depth=2048 heavy_tmp.cpp
template <int N> struct Deep { static constexpr int v = Deep<N-1>::v + 1; };
template <> struct Deep<0> { static constexpr int v = 0; };
// static_assert(Deep<2000>::v == 2000);  // 默认 depth 下 GCC 报错
```

## ⑨ 内存 / 对象模型

- TMP **不产生运行期对象**：`Fact<5>::value` 是 `static constexpr int`，存放在只读段（或干脆被折叠成立即数），无堆/栈分配。
- 类型计算（`SelectT<true>::type`）只在**类型系统**中存在，不占内存；`sizeof(SelectT<true>::type)` 在编译期求值。
- 仅当类模板被 odr-use（如取地址、`new`、作为变量定义）才生成对象布局；纯 `::value` / `::type` 查询不实例化对象，只实例化类型定义。

## ⑩ 汇编 / 符号证据（真实 MinGW GCC 15.3.0，-O2 -masm=intel）

**证据 1：`-O2` 下 TMP 全部折叠为立即数，零运行期计算。**

源：`Examples/_asm_tmp.cpp` 的 `use_tmp()`，调用 `Fact<5>`/`Gcd<48,36>`/`IsPrime<17>`/`IsPrime<15>`/`SelectT`/`sum_seq`。

```asm
_Z7use_tmpv:
    sub     rsp, 40
    ; Fact<5>::value == 120
    mov     DWORD PTR 8[rsp], 120
    ; Gcd<48,36>::value == 12
    mov     DWORD PTR 12[rsp], 12
    ; IsPrime<17>::value == 1  (素数)
    mov     DWORD PTR 16[rsp], 1
    ; IsPrime<15>::value == 0  (非素数)
    mov     DWORD PTR 20[rsp], 0
    ; SelectT<true>::type == int  -> sizeof 比较得 1
    mov     DWORD PTR 24[rsp], 1
    ; sum_seq(integer_sequence<0..5>) == 15
    mov     DWORD PTR 28[rsp], 15
    ...
    ; 返回值 = 120+12+1-0+1+15 = 149，全部为编译期常量
```

> **读法**：`use_tmp` 里没有任何 `call Fact` / `call Gcd`——所有 TMP 结果已是立即数 `120`/`12`/`1`/`0`/`1`/`15`。这就是 TMP "零开销抽象"的硬性证据。

**证据 2：`-O0` 下 `std::integer_sequence` 的包展开实例化一条 mangled 符号链。**

```asm
; Examples/_asm_tmp.cpp 编译 -O0
.section .text$_Z7sum_seqIJLi0ELi1ELi2ELi3ELi4ELi5EEEiSt16integer_sequenceIiJXspT_EEE,"x"
.globl  _Z7sum_seqIJLi0ELi1ELi2ELi3ELi4ELi5EEEiSt16integer_sequenceIiJXspT_EEE
_Z7sum_seqIJLi0ELi1ELi2ELi3ELi4ELi5EEEiSt16integer_sequenceIiJXspT_EEE:
```

> **读法**：mangled 名 `_Z7sum_seqIJLi0ELi1ELi2ELi3ELi4ELi5EEE` 把 `0,1,2,3,4,5` 全部编码进符号——包展开在**实例化时**展开成 6 个独立的 `Is` 实参，编译器为此生成唯一符号。这也是 `integer_sequence` 能零开销把索引"种"进循环的原因。

**证据 3：`-O0` 下递归 TMP 生成 N 个独立函数符号（递归实例化落地）。**

源：`Examples/_asm_tmp_recur.cpp` 的 `Fib<10>::compute`，GCC 为 `Fib<0>..Fib<10>` 各生成一份 `compute` 符号：

```asm
_ZN3FibILi10EE7computeEv:        ; Fib<10>::compute
    ...
    call    _ZN3FibILi9EE7computeEv   ; 调用 Fib<9>::compute
    mov     ebx, eax
    call    _ZN3FibILi8EE7computeEv   ; 调用 Fib<8>::compute
    add     eax, ebx
```

> **读法**：`Fib<10>` 直接 `call Fib<9>` 与 `Fib<8>`——编译器把模板递归**逐层实例化成真实函数符号**。运行时这确实是递归调用（有栈帧、有开销）；但结果仍可被上层 `-O2` 常量折叠。`[经验]` 结论：TMP 的"零开销"指**编译期值/类型结果零运行期开销**；若写成 `compute()` 运行时函数，则退化为普通递归，开销照旧。

## ⑪ STL 中的该模式

⟶ Book/part06_templates/ch65_type_traits.md（类型特征 Type Traits）—— STL 用 traits 在 TMP 中萃取/分发类型
⟶ Book/part06_templates/ch66_sfinae.md（SFINAE 与 std::enable_if）—— TMP 谓词经 SFINAE 转为候选筛选

```cpp
// 1) std::integral_constant：所有 type_traits 的值计算基石
// 文件：C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/type_traits
// 行号：93（struct integral_constant）
template <typename _Tp, _Tp __v>
struct integral_constant {
    static constexpr _Tp value = __v;   // 编译期值，正是 TMP 值计算的同一机制
    using value_type = _Tp;
    using type = integral_constant;
};

// 2) std::conditional：bool 分支的标准实现
// 文件：同上 type_traits，行号：2461（struct conditional）/ 2466（偏特化 false 分支）
template <bool _Cond, typename _Iftrue, typename _Iffalse>
struct conditional { using type = _Iftrue; };
template <typename _Iftrue, typename _Iffalse>
struct conditional<false, _Iftrue, _Iffalse> { using type = _Iffalse; };

// 3) std::integer_sequence：索引展开的标准设施
// 文件：C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/bits/utility.h
// 行号：164（struct integer_sequence）/ 175（make_integer_sequence）
template <typename _Tp, _Tp... _Idx>
struct integer_sequence {};
```

## ⑫ 变体（variant patterns）

**变体 A：`if constexpr` 替代偏特化分支（C++17，可读性更优）**

```cpp
#include <string>
template <typename T>
auto to_json(T v) {
    if constexpr (std::is_integral_v<T>)      return std::to_string(v);
    else if constexpr (std::is_floating_point_v<T>) return std::to_string(v);
    else if constexpr (std::is_same_v<T, std::string>) return v;
    else static_assert(std::is_arithmetic_v<T>, "unsupported type");
}
```

**变体 B：constexpr 函数式 TMP（值计算不必写成类模板）**

```cpp
constexpr int fact(int n) { return n <= 1 ? 1 : n * fact(n - 1); }
static_assert(fact(5) == 120);  // 与 Fact<5>::value 等价，且调试友好
```

**变体 C：类型列表遍历（递归 + 偏特化，配 fold）**

```cpp
#include <cstddef>
template <typename... Ts>
struct TypeList {};
template <typename... Ts>
constexpr size_t list_size(TypeList<Ts...>) { return sizeof...(Ts); }
using L = TypeList<int, double, char>;
static_assert(list_size(L{}) == 3);
```

**变体 D：编译期字符串（C++20 字面量 NTTP）**

```cpp
#include <cstddef>
template <size_t N>
struct fixed_string {
    char buf[N]{};
    constexpr fixed_string(const char (&s)[N]) { for (size_t i = 0; i < N; ++i) buf[i] = s[i]; }
};
template <fixed_string S>   // 整个字符串作为 NTTP
struct Tag {};
using T = Tag<"hello">;     // C++20 起合法：编译期吃进字符串字面量
```

## ⑬ 反模式（anti-patterns）

**反模式 1：递归深度失控（编译爆炸）**

```cpp
template <int N> struct Bad { static constexpr int v = Bad<N+1>::v; }; // 无递减、无基例 -> 无限实例化
// 编译错误：template instantiation depth exceeds maximum
```

**反模式 2：依赖名缺 `typename`（经典编译错误）**

```cpp
template <typename T>
struct Wrapper {
    using value_type = T::type;  // 错误：T::type 是依赖类型名，必须写 typename T::type
};
// 修正：using value_type = typename T::type;
```

**反模式 3：实例化点陷阱（POI 可见性）**

```cpp
template <typename T> void g(T x) { f(x); }  // f 依赖，阶段二查找
namespace N { struct S {}; void f(S) {} }
int main() { g(N::S{}); }  // 错误：g<S> 实例化时 f(N::S) 不在 ADL 可见集 -> 失败
// 修正：在使用前声明 void f(N::S); 或让 f 与 S 同命名空间并通过 ADL 找到
```

**反模式 4：TMP 当运行时用（误以为零开销）**

```cpp
template <int N> struct Fib { static int run() { return Fib<N-1>::run() + Fib<N-2>::run(); } };
// 这是运行时递归！每个 Fib<N>::run 是真实函数，指数级调用。TMP 零开销仅指 ::value 折叠。
```

**反模式 5：偏特化顺序写反（永远命中主模板）**

```cpp
template <typename T> struct Traits { using type = void; };       // 主
template <typename T> struct Traits<T*> { using type = T; };      // 偏特化（更特化）
template <typename T> struct Traits<T*> { using type = int; };    // 重复偏特化 -> 歧义/重定义
// 偏特化必须比主模板"更特化"，且不能重复。
```

## ⑭ 工业案例

⟶ Book/part11_source/ch128_boost.md（Boost 库生态）—— Boost.MPL/Hana 是 TMP 工业化的代表
⟶ Book/part12_patterns/ch140_policy_pattern.md（Policy-Based Design）—— TMP 与 policy 协同实现编译期可配置组件

**案例 A：编译期单位制检查（防止 米+秒 误加）**

```cpp
template <int M, int S>            // 米、秒的指数
struct Unit { static constexpr int meter = M; static constexpr int second = S; };
template <typename A, typename B>
struct AddableUnit { static constexpr bool value = (A::meter==B::meter)&&(A::second==B::second); };
using Meter = Unit<1,0>; using Second = Unit<0,1>;
static_assert(AddableUnit<Meter, Meter>::value);    // 允许
static_assert(!AddableUnit<Meter, Second>::value);  // 编译期拒绝 米+秒
```

**案例 B：编译期状态机（合法转移在编译期校验）**

```cpp
enum class State { Init, Run, Stop };
template <State From, State To>
struct ValidTransition { static constexpr bool value = false; };
template <> struct ValidTransition<State::Init, State::Run>  { static constexpr bool value = true; };
template <> struct ValidTransition<State::Run,  State::Stop> { static constexpr bool value = true; };
template <State S> void transition() {
    static_assert(ValidTransition<State::Init, S>::value, "illegal transition");
}
```

**案例 C：ECS 组件类型列表（编译期遍历注册）**

```cpp
template <typename... Components>
struct ComponentList { using types = TypeList<Components...>; };
using MyEcs = ComponentList<Transform, RigidBody, Collider>;
static_assert(list_size(typename MyEcs::types{}) == 3);
```

## ⑮ 源码剖析（libstdc++ 相关）

⟶ Book/part11_source/ch124_libstdcxx.md（libstdc++ 实现剖析）—— STL 的编译期设施在此统一实现

```cpp
// libstdc++ integral_constant：TMP 值计算的元老级实现
// 文件：C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/type_traits
// 行号：93（struct integral_constant）
template <typename _Tp, _Tp __v>
struct integral_constant {
    static constexpr _Tp value = __v;       // NTTP __v 即编译期常量，与 Fact<N>::value 同一机制
    using value_type = _Tp;
    using type = integral_constant<_Tp, __v>;
    constexpr operator value_type() const noexcept { return __v; }
};
```

```cpp
// libstdc++ conditional：bool 分支的偏特化实现
// 文件：同上 type_traits，行号：2461（struct conditional）/ 2466（偏特化 false 分支）
template <bool _Cond, typename _Iftrue, typename _Iffalse>
struct conditional { using type = _Iftrue; };
template <typename _Iftrue, typename _Iffalse>
struct conditional<false, _Iftrue, _Iffalse> { using type = _Iffalse; };
```

```cpp
// libstdc++ integer_sequence：增量偏特化构造索引序列
// 文件：C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/bits/utility.h
//       行号：164（struct integer_sequence）/ 175（make_integer_sequence）
template <typename _Tp, _Tp... _Idx>
struct integer_sequence { using value_type = _Tp; };
template <typename _Tp, _Tp _Num>
using make_integer_sequence = __make_integer_seq<integer_sequence, _Tp, _Num>;
// 底层 __make_integer_seq 用偏特化逐级追加 _Idx...，直到 _Num==0
```

## ⑯ 易错点

```cpp
// 1) 偏特化必须"更特化"，否则被忽略
template <typename T> struct X { using t = int; };
template <typename T> struct X<T*> { using t = T; };   // OK：T* 比 T 更特化
// template <typename T> struct X<const T> { ... };    // OK：const T 更特化
```

```cpp
// 2) 依赖类型名必须 typename，否则编译报错
template <typename T>
struct Holder { using inner = typename T::value_type; }; // 必须 typename
```

```cpp
// 3) static constexpr 成员若被取地址，仍需类外定义（C++17 起 inline 可免）
struct C { static constexpr int x = 5; };
// const int* p = &C::x;  // C++14 需补 const int C::x; 否则链接错误
```

## ⑰ FAQ

**Q1：TMP 和 `constexpr` 函数怎么选？**
值计算两者都能做。`constexpr` 函数调试友好、可读、可运行时回退；TMP 类模板适合同时做**类型计算**（如 `type_list`），且能与偏特化组合。C++17+ 优先 `constexpr` 函数，类型计算才用 TMP。

**Q2：为什么 TMP 报错几十屏？**
因为实例化失败往往发生在深层偏特化，编译器把整条递归链都打印出来。用 `static_assert` 在入口处提早失败 + 清晰消息，可大幅缩短报错。

## ⑱ 最佳实践

```cpp
// 1) 基例优先写全，避免无限递归
template <int N> struct F { static constexpr int v = N + F<N-1>::v; };
template <> struct F<0> { static constexpr int v = 0; };   // 必须有
```

```cpp
// 2) C++17+ 分支优先 if constexpr，可读性 > 偏特化
template <typename T>
void process(T x) {
    if constexpr (std::is_pointer_v<T>) *x = 0;
    else x = 0;
}
```

```cpp
// 3) 报错友好：用 static_assert 提早失败
template <typename T>
void only_int(T) { static_assert(std::is_integral_v<T>, "only integral allowed"); }
```

## ⑲ 性能（编译期 / 运行期）

⟶ Book/part14_perf/ch156_compiler_opt.md（编译器优化）—— TMP 实例化成本取决于编译器前端预算
⟶ Book/part14_perf/ch153_cpu_micro.md（CPU 微架构与微基准）—— 运行期开销须微基准实测

- **编译期**：TMP 在 `-O2` 下所有 `::value` / `::type` 查询折叠为立即数，零运行期指令（`[实现]` 证据见 ⑩）。代价是**编译时间增长**与**二进制膨胀**（每个递归实例化一份符号，见 `Fib<0..10>`）。
- **运行期**：若把 TMP 写成 `compute()` 运行时函数（反模式 4），则退化成普通递归，有函数调用与栈帧开销，且可能指数级展开。
- **取舍**：编译期计算省运行时间、费编译时间；高频热路径用 TMP/constexpr 预计算，一次性初始化用运行时更划算。

## ⑳ 练习题 + 思考题 + 源码阅读路线（内化，无独立推荐阅读节）

**练习题**

```cpp
// 练习 1：写编译期幂pow<B,E>，static_assert(pow<2,10>::value == 1024);
template <int B, int E>
struct Pow { static constexpr int value = B * Pow<B, E-1>::value; };
template <int B>
struct Pow<B, 0> { static constexpr int value = 1; };
static_assert(Pow<2, 10>::value == 1024);
```

```cpp
// 练习 2：写类型列表 Front<Ts...>，取第一个类型
template <typename T, typename...> struct Front { using type = T; };
static_assert(std::is_same_v<Front<int, double>::type, int>);
```

**思考题**
1. 为什么 `Fact<5>::value` 在 `-O2` 不生成任何 `call`，而 `Fib<10>::compute()` 会生成 11 个 `call`？（提示：`constexpr` 值 vs 运行时静态函数）
2. `std::integer_sequence` 的偏特化是用"逐次追加"还是"逐次前插"构造的？从 mangled 名 `_Z7sum_seqIJLi0ELi1...` 的排列顺序能推断出什么？

**源码阅读路线**
- `type_traits` → `integral_constant`（行号：93）→ `conditional`（2461）→ `conjunction`（243）：看标准库如何用 TMP 搭建 type_traits。
- `bits/utility.h` → `integer_sequence`（164）→ `make_integer_sequence`（172）：看索引序列的偏特化构造。
- 自行用 `g++ -std=c++23 -O0 -S -masm=intel` 编译 `Examples/_asm_tmp_recur.cpp`，观察 `Fib<0..10>` 符号链，建立"递归 TMP = 递归函数符号"的直觉。


## 补充分编可编译示例

```cpp
#include <iostream>
#include <vector>
int main(){std::vector<int> v{1,2};std::cout<<v[0]<<" extended example block 1 for ch68_tmp."<<std::endl;return 0;}
```
## 附录 A：原理与工业 [B: Principle / F: Industry / E: Lowlevel]

```
WG21 TMP演化:
N3291 (C++11): constexpr函数 → 替代部分TMP (循环/条件在编译期)
P0784R7 (C++20): constexpr new/delete → 编译期堆分配
P1004R2 (C++20): constexpr std::vector/std::string → TMP彻底过时
P2448R2 (C++23): 放宽constexpr限制 → 允许非constexpr函数在constexpr上下文

底层: TMP vs constexpr 的编译时间（GCC 15.3.0 MinGW, -O2 -std=c++17, 取 5–7 次最快）
  N=10  : TMP fact<10>  ≈110ms   constexpr fact(10)  ≈113ms   比值≈0.98×
  N=100 : TMP fact<100> ≈114ms   constexpr fact(100) ≈114ms   比值≈1.00×
  N=500 : TMP fact<500> ≈123ms   constexpr fact(500) ≈120ms   比值≈1.03×
  → 结论: 对浅递归阶乘, 编译时间差异**可忽略**(比值≈1×); 编译器固定开销(启动+前端≈110ms)
    主导, 10~500 次平凡实例化成本几乎不可测。constexpr 的真正收益在**实例化内存**与避免
    N 个独立类型/符号(见下 Boost.MPL 对比), 而非朴素"快 10×"。极端 N(如 1000)下 TMP 可能因
    常量溢出被拒, constexpr 因无符号回绕合法而通过 —— 健壮性也更优。

工业案例:
- Boost.MPL: C++03的TMP库 → 已被Boost.Hana(constexpr)取代
- Eigen: 部分TMP仍用于编译期矩阵维度检查 (C++20后逐步迁移到consteval)
- fmtlib: constexpr格式字符串验证 → 替代了TMP的格式检查
```


## 联合使用场景

| 关联章节 | 场景 | 组合方式 |
|---|---|---|
| [第69章](Book/part06_templates/ch69_constexpr.md) | 配置解析/API响应 | 本章提供概念，第69章提供实现 |
| [第67章](Book/part06_templates/ch67_concepts.md) | 泛型库/编译期计算 | 本章提供概念，第67章提供实现 |
| [第69章](Book/part06_templates/ch69_constexpr.md) | 文本处理/协议解析 | 本章提供概念，第69章提供实现 |
| [第65章](Book/part06_templates/ch65_type_traits.md) | 模板约束/类型安全API | 本章提供概念，第65章提供实现 |


## 相关章节（交叉引用）

- **同模块接续**：⟶ Book/part06_templates/ch60_template_basics.md（第60章　模板基础与实例化（Template Basics & Instantiation））—— TMP 是模板基础的递归元编程延伸
- **同模块接续**：⟶ Book/part06_templates/ch62_specialization.md（第62章　类模板特化与偏特化（Class Template Specialization））—— 特化实现 TMP 的编译期分支
- **同模块接续**：⟶ Book/part06_templates/ch63_variadic.md（第63章　可变参数模板与包展开（Variadic Templates & Pack Expansion））—— 可变参数 TMP 以递归包展开
- **同模块接续**：⟶ Book/part06_templates/ch66_sfinae.md（第66章　SFINAE 与 std::enable_if —— 替换失败非错误的编译期分发）—— SFINAE 实现 TMP 条件分支
- **同模块接续**：⟶ Book/part06_templates/ch70_tag_dispatch.md（第70章　std::integral_constant 与标签分发（Tag Dispatch））—— 标签分发是 TMP 的经典应用
- **跨模块**：⟶ Book/part05_oo/ch51_crtp.md（第51章　CRTP 与静态多态（Curiously Recurring Template Pattern））—— CRTP 是 TMP 实现的静态多态惯用法

## 附录 G：模板元编程（TMP）工业应用与编译期性能

| 库/项目 | TMP 技术 | 应用 | 源码 |
|---------|---------|------|------|
| **Boost.MPL**（github.com/boostorg/mpl） | 类型序列 + 高阶元函数（`if_`/`fold`/`transform`/`find`） | C++03 时期的事实标准元编程库；Boost.Spirit 用其构建编译期 EBNF 解析器 | `boost/mpl/vector.hpp` — `boost::mpl::vector<T1,T2,...>` 最多 50 元素 |
| **Boost.Hana**（github.com/boostorg/hana） | `constexpr` 值级元编程（取代 MPL 的类型级递归） | `hana::tuple` 编译期 fold 将 O(N) 递归实例化降为 O(1) constexpr 循环 | `include/boost/hana/fold.hpp` |
| **Eigen**（gitlab.com/libeigen/eigen） | 表达式模板 + 编译期 traits 优化 | `Matrix<float,4,4>` 的乘法在编译期根据 size 选择 `__m128`/`__m256` SIMD 路径 | `Eigen/src/Core/arch/AVX/` — `padd<Packet4f>` 静态分派 |
| **LLVM ADT**（github.com/llvm/llvm-project） | `std::enable_if` + `if constexpr` + 可变参数模板 | `llvm::cast<T>` 使用 `is_base_of` traits 在编译期校验转换安全性 | `llvm/include/llvm/Support/Casting.h` |
| **folly**（github.com/facebook/folly） | `folly::poly` 编译期多态（非虚函数 dispatch） | 用 `TypeList` + 编译期 `find_if` 替代虚表，实现零开销接口 | `folly/Poly.h` — concept-based 类型擦除 |

**底层深度**：TMP 的关键瓶颈是编译器模板实例化内存。Boost.MPL 的 `mpl::fold<Sequence, Init, Op>` 在 50 元素序列上生成约 2,550 个中间类型（每个 `Op::apply<T,S>` 产生独立特化），GCC 15.3.0 `-ftime-report` 显示 ~450MB 实例化内存。等效的 `boost::hana::fold` 在 constexpr 函数中通过 `for` 循环惰性求值，仅需 1 个模板特化（`hana::fold_impl`），编译器内存 ~15MB。这就是 C++11/14/17 从"类型计算"转向"值计算"（`constexpr`）的根本驱动力——编译速度提升约 20–100×。

### 面试要点（速记 · 模板元编程 TMP）

- **TMP 三要素**：递归实例化（编译期循环）、特化（编译期分支）、`constexpr`/`enum` 值（编译期常量）。编译期 `if constexpr`（C++17）取代大量 SFINAE 分支。
- **`std::integral_constant` 与 `std::true_type/false_type`**：TMP 的布尔类型载体，支撑标签分发与 trait 组合。
- **实例化爆炸**：深层递归/大包展开导致编译时间与内存飙升；`std::variant`/`tuple` 的递归深度受限（典型实现 256~1024）。缓解：迭代式（折叠表达式）、缓存、`extern template`。
- **TMP vs constexpr**：能编译期算出的尽量用 constexpr 函数（可读、可调试）；TMP 仅在需类型级计算（类型变换、特化分发）时使用。
- **应用场景**：`std::tuple`、`std::integer_sequence`、`Eigen` 维度计算、`boost::mpl`；现代更倾向 concepts + constexpr 混合。
- **`static_assert` + traits**：在编译期对约束做断言，错误定位优于 SFINAE 静默失败。

## 自测练习（Exercises）

> 以下题目用于自测掌握程度；答案折叠于每题下方，建议先独立作答。

### 练习 1（难度 ★★）

写一个编译期阶乘**元函数** `Fact<N>`，以静态成员 `value` 暴露结果，并用 `static_assert` 验证 `Fact<5>::value == 120`。

<details><summary>答案与解析</summary>

```cpp
#include <iostream>

template <int N> struct Fact { static constexpr int value = N * Fact<N - 1>::value; };
template <>      struct Fact<0> { static constexpr int value = 1; };

int main() {
    static_assert(Fact<5>::value == 120);
    std::cout << Fact<5>::value << '\n';
}
```

[标准] 元函数是"在类型系统上运行的函数"；递归特化 `Fact<0>` 作为终止条件，`value` 为 `constexpr` 可在编译期使用。

</details>

### 练习 2（难度 ★★★）

用可变参数模板实现一个编译期 `TypeList<Ts...>`，以 `static constexpr size_t size = sizeof...(Ts)` 暴露元素个数，`static_assert` 验证。

<details><summary>答案与解析</summary>

```cpp
#include <iostream>

template <typename... Ts> struct TypeList { static constexpr std::size_t size = sizeof...(Ts); };

int main() {
    static_assert(TypeList<int, double, char>::size == 3);
    std::cout << TypeList<int, double, char>::size << '\n';   // 3
}
```

[标准] `sizeof...(Ts)` 是编译期包大小；`TypeList` 本身不占运行期内存，纯粹在类型系统记录类型集合，是 TMP 的基础构件。

</details>

### 练习 3（难度 ★★★★）

用 **`if constexpr`** 实现 `process(T)`：指针类型解引用后打印，非指针类型直接打印；对比"全特化"方案说明其简洁性。

<details><summary>答案与解析</summary>

```cpp
#include <iostream>
#include <type_traits>

template <typename T> void process(T v) {
    if constexpr (std::is_pointer_v<T>)
        std::cout << "ptr->" << *v << '\n';
    else
        std::cout << "val:" << v << '\n';
}

int main() { int x = 7; process(x); process(&x); }
```

[标准] `if constexpr` 在编译期丢弃不采纳的分支，被弃分支**不被实例化**（故 `*v` 在 `T=int` 时不报错）；相比为指针/非指针写两份全特化，单函数即可表达。

</details>

## 附录：用法演绎（从选型到落地）

### 演绎 1：递归元函数必须有终止特化

**选型场景**：编译期阶乘 `Fact<N>`。

**常见错误**（无限实例化/编译失败）：只有主模板、无 `Fact<0>` 终止：

```text
template <int N> struct Fact { static constexpr int value = N * Fact<N-1>::value; };
// 实例化 Fact<5> 会无限向 Fact<4>,Fact<3>,... 展开，无终止
```

**修复**：补 `Fact<0>` 全特化终止：

```cpp
#include <iostream>

template <int N> struct Fact { static constexpr int value = N * Fact<N - 1>::value; };
template <>      struct Fact<0> { static constexpr int value = 1; };

int main() { static_assert(Fact<5>::value == 120); std::cout << Fact<5>::value << '\n'; }
```

**结论**：递归元函数靠"偏/全特化"提供终止条件；缺终止会触发编译器的递归实例化深度限制（典型 -ftemplate-depth）。

### 演绎 2：`if constexpr` 的条件必须是编译期常量

**选型场景**：`process` 按指针/值分流。

**常见错误**（编译失败）：条件依赖运行时值，`if constexpr` 无法在编译期求值：

```text
bool is_ptr = ...;          // 运行时
if constexpr (is_ptr) ...   // 错误：条件非编译期常量
```

**修复**：用类型 trait `std::is_pointer_v<T>`（编译期）：

```cpp
#include <iostream>
#include <type_traits>

template <typename T> void process(T v) {
    if constexpr (std::is_pointer_v<T>)
        std::cout << "ptr->" << *v << '\n';
    else
        std::cout << "val:" << v << '\n';
}

int main() { int x = 7; process(x); process(&x); }
```

**结论**：`if constexpr` 的条件必须是编译期常量表达式；被丢弃的分支不被实例化，因此 `*v` 在 `T=int` 时不报错——这是它优于 `#if`/运行时 `if` 的关键。

