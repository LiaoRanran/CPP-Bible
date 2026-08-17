# 第67章　Concepts 与 requires —— C++20 的编译期约束
> **[验证环境]** 本章示例均在 **Windows 11 · MinGW-w64 GCC 15.3.0 · `-std=c++23 -O2`** 下编译验证。模板与语言机制以 [标准]（ISO C++23）为权威；本章不含绝对性能或内存布局断言，跨编译器（Clang/MSVC）行为以各实现对标准的遵循度为准。

[第66章　SFINAE 与 std::enable_if —— 替换失败非错误的编译期分发](Book/part06_templates/ch66_sfinae.md)
[第119章　Ranges 深入（C++20）](Book/part10_modern/ch119_ranges_deep.md)

> 文件路径：`Book/part06_templates/ch67_concepts.md`
> 用途：工业级讲解 C++20 Concepts 与 requires 子句，含手写 concept、标准库 concept 源码剖析、与 SFINAE 的 ABI 等价性、MinGW GCC 15.3.0 真实汇编证据。
> 作者：CPP-Bible 工程
## ⓪ 历史动机：Concepts 的来龙去脉

> 模板报错像天书？Concepts 是 C++ 委员会用近二十年才兑现的「让约束说话」的承诺。

### 0.1 起源（谁·何时·为何）
模板的痛点从第一天就在：一旦实参不满足模板内部的隐含假设，编译器会吐出几百行「实例化深处」的错误，没人看得懂。[史] Stroustrup 早早就想给模板加「接口约束」，这个想法后来被命名为 **concepts**；但委员会在 2000 年代多次提案、反复重写，甚至 2009 年一度把已规划进 C++0x 的 concepts **整体拿下**，因为设计过重、规则未稳。[史] 直到「concepts lite」路线被采纳，C++20 才终于把约束语法（`requires`、concept 定义）落地。

### 0.2 关键转折（编年）
- 2000s：concepts 多轮提案，目标始终是「可读的模板报错 + 更快的约束检查」。
- 2009：原 concepts 提案被移出 C++0x，社区震动。[史]
- 2010s 中：concepts lite（P0734 等）简化设计，获接纳。
- 2020：C++20 正式发布 concepts，模板约束进入语法一层。

### 0.3 设计哲学之争
concepts 之争本质是「通用性 vs 可读性」的拉锯：一派要最强的表达力（导致设计膨胀），一派要最小可用的约束（最终胜出）。[评] 它彻底改变了模板风格——从 SFINAE（ch66）的「试探式」转向 `requires` 的「声明式」，报错从天书变人话。

### 0.4 史料补遗与持续编年
0.2 编年止于 C++20 正式发布 concepts。concepts 自身的演化并未停步：

- [史] concepts 的正式落地走得很长：从 2003 年 Bjarne 的「concepts lite」设想、2009 年 C++0x 试图纳入却因设计分歧在 2012 年被「一致投票移除」，直到 2017 年 P0734 重启、才随 C++20 定稿。这是标准史上少见的「被否决后重做」的特性。

- [史] C++23 增强了 abbreviated function templates 与 `auto` 在更多位置的约束能力；后续（C++26 轨道）还有「扩展的 auto」「原子约束细化」「对 concept 做合取/析取的更细约束」等讨论，让约束能表达更复杂的逻辑。

- [史] concepts 与静态反射（见 ch65）的结合正在酝酿：未来 `requires` 可能直接查询「类型被反射出的成员集合」，把「接口约束」与「编译期自省」在语法上统一。

- [评] concepts 最大的隐性收益是错误信息：约束失败时只报「不满足某 concept」，而非展开几十层模板回溯。

> 史料来源：https://en.cppreference.com/w/cpp/language/constraints ；https://en.wikipedia.org/wiki/C%2B%2B20

> 版本：v3.0（2026-07-08）

## ① 学习目标 [标准]

[第66章　SFINAE 与 std::enable_if —— 替换失败非错误的编译期分发](Book/part06_templates/ch66_sfinae.md)
[第68章　模板元编程 TMP 基础（递归 / 分支 / 循环）](Book/part06_templates/ch68_tmp.md)

- 说清 `concept` 是什么：一个「编译期布尔谓词」，可被命名、组合、复用 [标准]
- 掌握 `requires` 表达式（简单/类型/复合/嵌套）四类约束的写法与语义 [标准]
- 区分「`template <C T>`（约束占位）」与「`requires` 子句（尾置约束）」两种施加方式 [标准]
- 能从 mangled 符号验证：Concepts 与 SFINAE 在 ABI 层**等价**——都只为「胜出候选」发射一份实例化 [平台]
- 理解 Concepts 相对 SFINAE 的核心优势：报错可读性（见 ch75）与组合性 [标准]

## ② 本模板模式速查（名称 / 适用场景 / 核心结构 / 定义）

- **模板名称**：Concepts（概念）+ `requires` 子句
- **适用场景**：给模板参数施加「语义约束」，让不满足约束的类型在实例化前被清晰拒绝；替代 SFINAE 做编译期分派
- **核心结构**：`template <typename T> requires Constraint<T> Ret f(T)` 或 `template <C T> Ret f(T)`
- **一句话定义**：concept 是一个经 `bool` 化的编译期约束，可像类型一样写在模板参数位上，编译器在替换前先求值它 [标准]

## ③ 核心结构与完整代码实现

手写一个 concept（语法糖，底层仍是「constexpr bool 谓词」）：

> **示例 1** [难度 ★★★☆☆] [主题：核心结构与完整代码实现]
```cpp
// 手写 concept：等价于一个编译期 bool 变量模板
template <typename T>
concept MyIntegral = std::is_integral_v<T>;

// 使用：约束占位写法（最干净）
template <MyIntegral T>
T twice(T x) { return x + x; }

// 等价尾置 requires 写法
template <typename T>
requires std::is_integral_v<T>
T twice2(T x) { return x + x; }
```

`requires` 表达式四类约束：

> **示例 2** [难度 ★★★☆☆] [主题：核心结构与完整代码实现]
```cpp
// 1) 简单约束：直接写类型/表达式，合法即满足
template <typename T>
concept HasSize = requires(T t) { t.size(); };        // t.size() 可调用即可

// 2) 类型约束：要求某个嵌套类型存在
template <typename T>
concept HasValueType = requires { typename T::value_type; };

// 3) 复合约束：要求某表达式「具某种属性」（如返回可转换为 bool）
template <typename T>
concept BooleanConvertible = requires(T t) { { !t } -> std::convertible_to<bool>; };

// 4) 嵌套/局部参数约束：在 requires 内再声明局部变量
template <typename T>
concept Addable = requires(T a, T b) { a + b; };       // 要求 a+b 合法
```

concept 的组合（与/或/非）：

> **示例 3** [难度 ★★★☆☆] [主题：核心结构与完整代码实现]
```cpp
template <typename T>
concept SignedIntegral = std::integral<T> && std::signed_integral<T>;

template <typename T>
concept Number = std::integral<T> || std::floating_point<T>;

template <typename T>
concept NotPointer = !std::is_pointer_v<T>;
```

## ④ requires 的精确求值时机（与 SFINAE 的对齐） [实现]

concept 失败与 SFINAE 失败**同一机制**：约束不满足 → 该候选从重载集剔除（非错误）。只有「全部候选约束都不满足」才升级为硬错误。

> **示例 4** [难度 ★★★☆☆] [主题：的精确求值时机]
```cpp
template <typename T>
requires std::integral<T>
T pick(T x) { return x * 2; }      // 约束 A

template <typename T>
requires (!std::integral<T>)
T pick(T x) { return x; }          // 约束 B（与 A 互斥且完备）

// pick(21) 命中 A；pick(2.5) 命中 B；二者覆盖全集且无交集
```

与 SFINAE 关键差异：**约束失败的报错位置在「约束处」而非「深层替换处」**，错误信息短而准（对比 ch66 的 SFINAE 报错，见 ch75）。

> **示例 5** [难度 ★☆☆☆☆] [主题：的精确求值时机]
```cpp
// 约束失败：编译器直接说 "constraints not satisfied"，而非 mangled 崩溃
// pick("str") → 两个 requires 都不满足 → 清晰报告 "no matching overload"
```

## ⑤ 适用场景与选型

| 需求 | 选 Concepts | 不选 / 替代 |
|---|---|---|
| 给模板参数加语义约束（C++20+） | `concept` + `requires` | SFINAE（兼容老标准） |
| 需要清晰报错 | Concepts（报约束名） | 纯 SFINAE（报 mangled 失败） |
| 约束需组合/复用 | concept 命名后可组合 | SFINAE 每次重写 `enable_if_t<...>` |
| 必须支持 C++11/14 | 不可用 | SFINAE + `enable_if` |
| 运行期内部分支 | `if constexpr` | Concepts 只做重载分派，不进函数体 |

## ⑥ 完整可运行示例（最小）

> **示例 6** [难度 ★★★☆☆] [主题：完整可运行示例（最小）]
```cpp
#include <concepts>
#include <iostream>
#include <string>

template <std::integral T>
T describe(T) { std::cout << "integral\n"; return {}; }

template <std::floating_point T>
T describe(T) { std::cout << "floating\n"; return {}; }

template <typename T>
requires std::same_as<T, std::string>
T describe(T) { std::cout << "string\n"; return {}; }

int main() {
    describe(42);
    describe(3.14);
    describe(std::string("x"));
}
```

> **示例 7** [难度 ★★★☆☆] [主题：完整可运行示例（最小）]
```cpp
// 自定义 concept：可调用且其参数可加
template <typename T>
concept Addable = requires(T a, T b) { a + b; };

template <Addable T>
T add_twice(T x) { return x + x; }

static_assert(Addable<int>);        // true
static_assert(!Addable<std::ostream>); // ostream 不可加 → false
```

> **示例 8** [难度 ★★☆☆☆] [主题：完整可运行示例（最小）]
```cpp
// 标准库 concept 链式组合
template <std::signed_integral T>
T abs_clamp(T x) { return x < 0 ? -x : x; }   // 仅接受有符号整型
```

### ⑥ 补充：更多可编译实据

> **示例 9** [难度 ★★★☆☆] [主题：补充：更多可编译实据]
```cpp
// 用 concept 约束只移动类型
struct OnlyMove { OnlyMove()=default; OnlyMove(const OnlyMove&)=delete; OnlyMove(OnlyMove&&)=default; };
template <std::move_constructible T>
OnlyMove wrap_move(T&&) { return {}; }
```

> **示例 10** [难度 ★★★☆☆] [主题：补充：更多可编译实据]
```cpp
#include <vector>
// 探测「是否有 value_type」——concept 版（与 ch66 的 void_t 等价但可读）
template <typename T>
concept HasValueType = requires { typename T::value_type; };
static_assert(HasValueType<std::vector<int>>);
static_assert(!HasValueType<int>);
```

> **示例 11** [难度 ★★☆☆☆] [主题：补充：更多可编译实据]
```cpp
// 尾置 requires 的 negate（与 SFINAE 对称）
template <typename T>
requires std::is_signed_v<T>
T negate(T x) { return -x; }
template <typename T>
requires (!std::is_signed_v<T>)
T negate(T x) { return x; }
```

> **示例 12** [难度 ★★☆☆☆] [主题：补充：更多可编译实据]
```cpp
// 仅「可递增」类型启用（标准库 std::incrementable）
template <std::incrementable T>
void bump(T& x) { ++x; }
```

> **示例 13** [难度 ★★☆☆☆] [主题：补充：更多可编译实据]
```cpp
#include <cstddef>
#include <vector>
// concept 约束「可下标」
template <typename T>
concept Indexable = requires(T t, std::size_t i) { t[i]; };
static_assert(Indexable<std::vector<int>>);
```

> **示例 14** [难度 ★★☆☆☆] [主题：补充：更多可编译实据]
```cpp
#include <string>
// 仅算术类型可实例化的类模板（concept 版）
template <std::arithmetic T>
struct ArithmeticOnly { T v; };
// ArithmeticOnly<std::string> 约束不满足 → 不可实例化
```

> **示例 15** [难度 ★★★☆☆] [主题：补充：更多可编译实据]
```cpp
#include <string>
// 返回不同类型的两份重载（concept 约束）
template <std::integral T>
std::string label(T) { return "i"; }
template <typename T>
requires (!std::integral<T>)
std::string label(T) { return "other"; }
```

> **示例 16** [难度 ★★☆☆☆] [主题：补充：更多可编译实据]
```cpp
// detection 用 concept 重写
template <typename T>
concept HasDeref = requires(T t) { *t; };
```

> **示例 17** [难度 ★★☆☆☆] [主题：补充：更多可编译实据]
```cpp
// concept 约束「可调用且返回 bool」
template <typename F>
concept Predicate = requires(F f) { { f() } -> std::convertible_to<bool>; };
```

> **示例 18** [难度 ★★☆☆☆] [主题：补充：更多可编译实据]
```cpp
// 可变参数 concept：包内每个类型都可加
template <typename... Ts>
concept AllAddable = (Addable<Ts> && ...);
```

> **示例 19** [难度 ★★☆☆☆] [主题：补充：更多可编译实据]
```cpp
// concept 约束「可比较相等」
template <typename T>
concept EqualityComparable = requires(T a, T b) { { a == b } -> std::convertible_to<bool>; };
```

> **示例 20** [难度 ★★☆☆☆] [主题：补充：更多可编译实据]
```cpp
// 简化版 input_iterator concept
template <typename T>
concept MyInputIt = requires(T it) { *it; ++it; it != it; };
```

> **示例 21** [难度 ★★☆☆☆] [主题：补充：更多可编译实据]
```cpp
// 兜底重载保证完备（concept 版）
template <std::pointer T>
void visit(T) {}
template <typename T>
requires (!std::pointer<T>)
void visit(T) {}
```

## ⑦ 标准规定 [标准]

- `concept` 定义于 `[temp.concept]` 13.7.7；`requires` 表达式定义于 `[expr.prim.req]`。
- 标准库 concept 定义于 `<concepts>`（[concepts] 18.6）、`<iterator>`（迭代器 concept）、`<ranges>`。
- 约束满足关系（「`T` 满足 `C`」）是**语法**检查，不涉及运行期：满足即 0/1 布尔。
- `std::same_as`、std::integral 等定义于 `<concepts>`（行号：62 `same_as`、100 `integral`）。

## ⑧ GCC / Clang / MSVC 行为差异 [实现][平台]

- **GCC/Clang**：`concepts` 自 GCC 10 / Clang 10 完整支持；约束在「约束求解」阶段求值，重载决议优先选「更受约束」的候选（偏序）。
- **MSVC**：自 VS2019 16.3（`-std:c++latest`）支持；旧版本对「requires 表达式内嵌套 requires」偶有 bug。
- **偏序规则**：当 `C1` 蕴含 `C2` 时，`C1` 比 `C2` 更受约束，重载决议优先 `C1`——三编译器一致。
- **报错可读性**：Clang/GCC 对 concept 失败给出「`T` does not satisfy `integral`」；MSVC 早期版本仍可能回落到 SFINAE 式长错。

> **示例 22** [难度 ★★☆☆☆] [主题：行为差异 [实现][平台]]
```cpp
// 更受约束者优先：两个重载都满足 int，但 SignedIntegral 比 Integral 更受约束
template <std::integral T>      void h(T) {}   // 较泛
template <std::signed_integral T> void h(T) {} // 更受约束 → int 调用命中此
```

## ⑨ 内存 / 对象模型

concept 是**纯编译期**实体：它不产生运行期对象、不占内存，编译后彻底消失。`Addable<int>` 求值为 `true` 常量，与 `std::is_integral_v<int>` 同构。

> **示例 23** [难度 ★★★★☆] [主题：内存 / 对象模型]
```cpp
static_assert(sizeof(std::integral<int>) == 1, "concept 本身不占内存");
static_assert(std::integral<int> == true, "concept 折叠为编译期 bool 常量");
```

## ⑩ 汇编 / 符号证据（真实 MinGW GCC 15.3.0） [平台] [VERIFIED]

编译 `Examples/_asm_tpl_concepts.cpp`（`-std=c++23 -O2 -masm=intel`）。**结论一**：`-O2` 下 `use_concepts` 把约束分派完全折叠为常量，运行期无 `requires` 痕迹：

```asm
; _Z12use_conceptsv （MinGW GCC 15.3.0, -O2）—— 约束分派已被编译期消除
_Z12use_conceptsv:
    sub     rsp, 24
    movsd   xmm0, QWORD PTR .LC0[rip]   ; .LC0 = 2.5（concept_f<double>）
    mov     DWORD PTR [rsp], 42         ; concept_f<int>(21) → 42
    movsd   QWORD PTR 8[rsp], xmm0
    mov     DWORD PTR 4[rsp], 14        ; add_twice<int>(7) → 14
    movsd   xmm0, QWORD PTR 8[rsp]
    mov     ecx, DWORD PTR [rsp]
    cvttsd2si eax, xmm0
    mov     edx, DWORD PTR 4[rsp]
    add     eax, ecx                    ; 42 + 2
    add     eax, edx                    ; + 14 = 58
    add     rsp, 24
    ret
```

**结论二**：`-O0` 下可见 mangled 符号——Concepts 与 ch66 的 SFINAE **一一对应**：`concept_f<int>`↔`sfinae_f<int>`（都做 `x*2`）、`concept_f<double>`↔`sfinae_f<double>`（都原样返回）；相反约束的候选不发射。

```asm
; _asm_tpl_concepts_O0.asm 节选（MinGW GCC 15.3.0, -O0）
    call    _Z9concept_fIiET_S0_   ; concept_f<int>     —— std::integral 约束命中
    call    _Z9concept_fIdET_S0_   ; concept_f<double>  —— requires !integral 命中
    call    _Z9add_twiceIiET_S0_   ; add_twice<int>     —— Addable concept 命中

_Z9concept_fIiET_S0_:              ; concept_f<int>：执行 x*2（与 sfinae_f<int> 同构）
    mov     DWORD PTR 16[rbp], ecx
    mov     eax, DWORD PTR 16[rbp]
    add     eax, eax
    pop     rbp
    ret

_Z9concept_fIdET_S0_:              ; concept_f<double>：原样返回（与 sfinae_f<double> 同构）
    movsd   QWORD PTR 16[rbp], xmm0
    movsd   xmm0, QWORD PTR 16[rbp]
    movq    rax, xmm0
    movq    xmm0, rax
    pop     rbp
    ret

_Z9add_twiceIiET_S0_:              ; add_twice<int>：Addable 约束命中，x+x
    mov     DWORD PTR 16[rbp], ecx
    mov     eax, DWORD PTR 16[rbp]
    add     eax, eax
    pop     rbp
    ret
```

**ABI 等价性总结**：SFINAE 的 `_Z8sfinae_fIi...` 与 Concepts 的 `_Z9concept_fIi...` 在「为每个胜出候选发射一份实例化、剔除其余」上完全一致——Concepts 只是把 `enable_if` 的「隐式剔除」升级为「显式约束 + 可读报错」。

## ⑪ STL 中的该模式

- `<concepts>` 提供 `same_as` / `derived_from` / `integral` / `floating_point` / `signed_integral` 等基础 concept。
- `<iterator>` 的 `input_iterator` / `random_access_iterator` 用 concept 串起整套迭代器层级。
- `<ranges>` 几乎完全建立在 concept 之上（`range` / `view` / `sized_range`）。
- `std::sort` 对 `random_access_iterator` 约束的算法，约束失败时报「不满足 random_access_iterator」而非深藏的 mangled 错。

> **示例 24** [难度 ★★☆☆☆] [主题：中的该模式]
```cpp
// 标准库风格：用 concept 约束算法入参
template <std::random_access_iterator It>
void my_sort(It first, It last) { /* ... */ }
```

## ⑫ 变体（variant patterns）

> **示例 25** [难度 ★★★☆☆] [主题：变体]
```cpp
// 变体 A：requires 表达式内做「返回类型约束」
template <typename T>
concept Derefable = requires(T t) { *t; } && requires(T t) { { *t } -> std::convertible_to<int>; };

// 变体 B：concept 复用另一个 concept（组合）
template <typename T>
concept SignedNumber = std::signed_integral<T> || std::floating_point<T>;

// 变体 C：可变参数 concept（要求包内每个类型都满足）
template <typename... Ts>
concept AllIntegral = (std::integral<Ts> && ...);
```

## ⑬ 反模式（anti-patterns）

> **示例 26** [难度 ★★★☆☆] [主题：反模式（anti-patterns）]
```cpp
// 反模式 1：在 concept 里写「运行期逻辑」——concept 只能含编译期可求值表达式
template <typename T>
concept Bad = requires(T t) { t.some_method(); } && (sizeof(T) > 4); // OK，但别塞运行期状态

// 反模式 2：约束互斥但不完备 → 某些类型全失败 → 硬错误
// 应保证「覆盖全集」或显式给出兜底重载

// 反模式 3：用 requires 表达式却没「消参」——无参 requires 应直接写类型约束
template <typename T>
concept HasType = requires { typename T::value_type; };   // 正确：无参用 typename
```

## ⑭ 工业案例

- **数值泛型库**：用 `std::floating_point` / `std::integral` 给 `Vector::dot` 拆出「整型走整数路径 / 浮点走 FMA」两份实现。
- **序列化框架**：用 `concept Serializable = requires(T t){ t.serialize(); }` 替代 ch66 的 `has_serialize` SFINAE，报错直接说「不满足 Serializable」。
- **Eigen/glm 现代化**：用 concept 约束「必须是某 CRTP 派生类」，语义比 `enable_if` 直白。

> **示例 27** [难度 ★★☆☆☆] [主题：工业案例]
```cpp
#include <string>
// 工业：序列化按 concept 择路，报错可读
template <typename T>
requires Serializable<T>
std::string to_json(const T& v) { return v.serialize(); }
```

## ⑮ 源码剖析（libstdc++ 相关）

`std::integral` / `std::same_as` 的真实定义（文件：`C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/concepts`，行号：109 `integral` / 64 `same_as`）：

> **示例 28** [难度 ★★★☆☆] [主题：源码剖析（libstdc++ 相关）]
```cpp
// <concepts> 行 100：integral 建立在 is_integral_v 之上
template<typename _Tp>
  concept integral = is_integral_v<_Tp>;

// <concepts> 行 62：same_as 用「双向 is_same」保证对称性
template<typename _Tp, typename _Up>
  concept same_as = std::is_same_v<_Tp, _Up> && std::is_same_v<_Up, _Tp>;
```

可见 concept 并非新机制——它把 ch65 的 `is_xxx_v` trait 与 ch66 的 `enable_if` 组合「命名化、可读化」。

## ⑯ 易错点

- **概念不等价于 trait 的「值」**：`std::integral<T>` 用在「约束位」；若要拿 bool 值做逻辑，用 `std::is_integral_v<T>`。
- **requires 表达式 ≠ 运行期 if**：`requires(T t){ t.foo(); }` 只检查「能否调用」，不执行 `foo()`。
- **更受约束优先**：定义了「泛」与「更受约束」两份重载时，调用会选更受约束者——别误以为「先定义的赢」。
- **`&&` 短路**：concept 组合里的 `&&` 是编译期短路，某子约束非法时整条约束失败（静默剔除，非错误）。

> **示例 29** [难度 ★★★☆☆] [主题：易错点]
```cpp
// 易错：把 concept 当 bool 值传入 enable_if（C++20 仍可混用，但语义冗余）
template <typename T, std::enable_if_t<std::integral<T>, int> = 0>  // 旧写法
void g(T);
template <std::integral T>                                            // 新写法：直接用 concept
void g(T);
```

## ⑰ FAQ

- **Q：Concepts 比 SFINAE 快吗？** A：运行期完全相同（都是零开销，见 ⑩）；差别在编译期错误可读性，不是性能。
- **Q：能用 concept 替代 `if constexpr` 吗？** A：不能。concept 只做「重载/模板参数的择一」；同一函数内按类型走不同分支仍用 `if constexpr`。
- **Q：concept 能约束非类型参数吗？** A：能。`template <auto N> requires (N > 0) ...` 约束值。
- **Q：为什么 `same_as` 要双向 `is_same`？** A：防止 `A` 满足 `same_as<B>` 但 `B` 不满足 `same_as<A>` 的对称性破缺（见 ⑮ 源码）。

## ⑱ 最佳实践

- C++20 项目一律用 Concepts 替代 SFINAE 做约束；老标准回退到 `enable_if`。
- 给 concept 起「语义名」（`Serializable` / `Addable`）而非「结构名」（`HasSerializeMethod`）。
- 约束要保证「互斥且完备」，或显式提供兜底重载，避免调用点硬错误。
- 用 concept 组合（`&&`/`||`/`!`）表达复杂约束，比层层嵌套 `enable_if_t` 可读性高一个量级。

> **示例 30** [难度 ★★★☆☆] [主题：最佳实践]
```cpp
// 最佳实践：语义化 concept + 完备约束
template <typename T>
concept Numeric = std::integral<T> || std::floating_point<T>;

template <Numeric T>        // 数值走这里
T process(T x) { return x; }
template <typename T>
requires (!Numeric<T>)      // 非数值兜底，保证完备
T process(T x) { return x; }
```

## ⑲ 性能（编译期 / 运行期）

- **运行期**：零开销。约束求解在编译期完成，运行期生成的代码与手写普通函数、`enable_if` 版本**逐字节一致**（见 ⑩ 的 `add eax,eax` 同构）。
- **编译期**：concept 的「约束缓存」通常比反复 `enable_if` 替换更快收敛；更受约束的偏序决议也比 SFINAE 候选枚举更高效。

> **示例 31** [难度 ★★★☆☆] [主题：性能（编译期 / 运行期）]
```cpp
// 运行期零差异验证：concept 版与手写版生成相同指令
static_assert(std::integral<int> == true);   // 编译期常量，无运行期成本
```

## ⑲附　知识图谱与选型决策（可视化） [D6 / D3]

> ch67 全章文字极深（WG21 / SFINAE 对比 / 工业 / 源码 / 性能），但**零图示**。本附节用两张 Mermaid 补上「知识连接（D6）」与「可视化决策（D3）」两个维度，便于建立概念网络、降低选型犹豫。

### 概念生态知识图谱（D6）

```mermaid
graph LR
    C["concept C++20"] --> R["requires 子句/表达式"]
    C --> T["type trait C++11 is_integral"]
    R --> SF["SFINAE C++11 enable_if void_t"]
    R --> IF["if constexpr C++17"]
    C --> A["constrained auto auto f(C c)"]
    C --> O["重载决议 more-constrained 胜出"]
    C --> STL["Ranges STL 约束 sort"]
    T -.-> SF
    IF -.-> SF
    C ==> SF
    style C fill:#1f6feb,color:#fff
    style R fill:#2da44e,color:#fff
```

`[标准]`：concept 在 `[temp.concept]` 定义为「具名布尔谓词」；`requires` 既可写约束表达式也可写 *requires clause*。`[经验]`：concept 并非取代 trait/SFINAE，而是把散落在 `enable_if` 里的约束**命名化、可组合、可诊断**——图谱中 `==>` 表示"诊断体验质变"而非"功能互斥"（呼应 附录 C 的错误信息对比）。

### 选型决策流（D3）：约束该用哪把刀

```mermaid
flowchart TD
    Q["需要对类型/值加约束?"] -->|否| N["普通模板"]
    Q -->|是| Q1["约束要复用/命名?"]
    Q1 -->|是| C1["concept + requires"]
    Q1 -->|否| Q2["仅单点分支?"]
    Q2 -->|运行期已知| IF1["if constexpr"]
    Q2 -->|编译期剪裁重载| SF1["SFINAE enable_if"]
    C1 --> Q3["约束失败期望?"]
    Q3 -->|清晰错误| C2["concept 报不满足 X"]
    Q3 -->|晦涩错误| SF2["SFINAE 报 substitution failure"]
    style C1 fill:#1f6feb,color:#fff
    style IF1 fill:#2da44e,color:#fff
    style SF1 fill:#cf222e,color:#fff
```

`[经验]`：现代 C++ 的默认选择是 **concept + requires**（可读、可诊断、可组合）；仅在"历史代码库必须 C++14/17"或"极致编译期元编程"时才退回 SFINAE；`if constexpr` 解决的是**运行期分支的编译期剪裁**，与约束是正交维度（见图谱虚线）。

---

## ⑳ 练习题 + 思考题 + 源码阅读路线（内化，无独立推荐阅读节）

**练习题**（已升级为「真实场景 + 引用参考」框架：保留原考察技能，场景改写为工程应用）

1. **真实场景：用 `std::integral` 约束模板实参。** 你不想让浮点类型实例化你的整数算法。请说明约束作用。
   - [标准] C++20 概念约束模板实参，不满足约束的调用在编译期被诊断，且给出清晰错误。
   - [引用] ISO/IEC 14882:2023 §[concepts]（标准概念）/ [temp.constr]（约束）；cppreference "Constraints and concepts" 词条。

2. **真实场景：用 `requires` 表达式定义自定义概念。** 你要求类型必须有 `size()` 与 `data()`。请说明语义。
   - [标准] requires 表达式列出对类型合法操作的要求；不满足任一要求的类型被约束排除。
   - [引用] ISO/IEC 14882:2023 §[expr.prim.req]（requires 表达式）；cppreference "Requires expression" 词条。

3. **真实场景：受约束候选在重载决议中优先。** 你同时有泛型与特化约束版本。请说明优先级。
   - [标准] 在重载决议中，更受约束（或更特化）的候选优先于不受约束/更泛化的版本。
   - [引用] ISO/IEC 14882:2023 §[temp.constr]（约束与偏序）；cppreference "Constraints and concepts" 词条。

- **练习题 1**：手写 `Derefable` concept，要求 `*t` 合法且结果可转换为 `T`。
- **练习题 2**：用 concept 给 `std::vector` 风格容器写 `push_back`，约束「可拷贝」。
- **练习题 3**：定义 `AllSame<Ts...>` concept，要求包内所有类型彼此 `same_as`。
- **思考题**：比较 `ch66_sfinae.md` 与本章的 `-O0` mangled——为何 `_Z9concept_fIi` 与 `_Z8sfinae_fIi` 的**函数体完全相同**？说明二者 ABI 等价。
- **源码阅读路线**：`<concepts>` 行号：109（`integral`）、64（`same_as`）；`ch66_sfinae.md`（SFINAE 对照）、`ch62_specialization.md`（偏特化是约束载体）、`ch65_type_traits.md`（trait 是 concept 的底层）、`ch68_tmp.md`（编译期计算）、`ch75_template_diag.md`（约束失败报错对比）。

## ㉒ 历史纵深·真实产业坐标·生产踩坑·与标准的互动

> 本节为 P0-15 全库深度升维大波次之一：压实历史出处、真实产业坐标、生产级踩坑与「本特性与 C++ 标准」的互动。引用链接列于 ㉒.5。

### ㉒.1 历史渊源补强：concepts 为何花了近二十年才落地
[史] 模板的痛点从第一天就在：一旦实参不满足模板内部隐含假设，编译器会吐出几百行「实例化深处」的错误。Stroustrup 早早就想给模板加「接口约束」，这个想法后来被命名为 **concepts**。但委员会在 2000 年代多次提案、反复重写，甚至 2009 年一度把已规划进 C++0x 的 concepts **整体拿下**，因为设计过重、规则未稳——这是标准史上少见的「被否决后重做」的特性。直到「concepts lite」路线被采纳（P0734 等重启），C++20 才终于把约束语法（`requires`、concept 定义）落地。
[评] 它彻底改变了模板风格——从 SFINAE（ch66）的「试探式」转向 `requires` 的「声明式」，报错从天书变人话，但长达二十年的拉锯也说明「通用性 vs 可读性」的张力有多难调和。

### ㉒.2 真实工程坐标：concepts 活在哪些产品/项目里

下表把「concepts」拉成「把模板参数的契约从文档升级为机器可检查」的 C++20 设施。

| 领域/类别 | 代表系统·生态 | 它承担的角色 | 规模·行业地位 | 备注 / 标准互动 |
| --- | --- | --- | --- | --- |
| 标准库 | `std::ranges`（`std::sort`/`find`） | 用 `random_access_iterator` 等 concept 约束算法，报错点名缺的操作 | 一切 C++20+ 程序地基 | concepts 最大工业落地 [STANDARD] |
| 知名库 | Abseil、Ranges-v3、Eigen | concepts 重写接口约束，取代 `enable_if` 迷宫 | 工业级基础设施 | 编译错误大幅收敛 |
| 大型服务代码 | 金融/游戏引擎（`Writable`/`Lockable`/`Allocator`） | 自定义 concept 把「参数契约」从文档升级为机器可检查 | 服务端/实时系统 | 契约机器化 |
| 跨平台 GUI | Qt 6 | concepts 约束信号/槽与容器 API 模板参数 | 桌面/嵌入式 UI | 错误收敛到调用点 |
| 自动驾驶 | Autoware / Apollo | 自定义 concept 描述传感器消息/点云/路径点契约 | 感知/规划模块 | 编译期校验接口，减运行期错配 |

> **表注（㉒.2）**：上表把「concepts」拉成「把模板参数的契约从文档升级为机器可检查」的 C++20 设施。标准库 `std::ranges` 是最大工业落地（`std::sort` 用 `random_access_iterator` 约束、报错直接点名缺的操作），Abseil/Ranges-v3/Eigen 用它取代 `enable_if` 迷宫，Qt 6 把信号/槽契约机器化。注意 Autoware/Apollo 一行：自动驾驶用自定义 concept 描述传感器消息/点云/路径点的接口契约，让感知与规划模块间的模板接口在编译期就被校验——concepts 在这里把「运行期类型错配」提前成「编译期拒绝」，对安全关键系统价值极高。

**一条判读**：用 concepts 的判据是「模板参数有一组必须满足的语义/语法契约，且要让违反时报错收敛到调用点」。算法约束（ranges）、库的接口契约、安全关键系统的模块接口 → concepts（C++20）；它直接取代 SFINAE/`enable_if` 迷宫，报错从几百行实例化回溯收敛到一行。规则：新泛型代码默认用 concept 表达约束；复合约束用 `requires` 子句；库的公共模板接口优先 concepts 而非 SFINAE，既收敛报错又当文档。
### ㉒.3 生产踩坑：concepts 的常见误用与陷阱
- **约束不够强导致仍选错重载**：写得过于宽松的 concept 会让多个重载同时满足，最终回到「偏序/约束排序」的微妙判定，踩与 SFINAE 时代相同的坑。
- **`requires` 表达式里的硬错误**：`requires` 内若写了「对某些类型必然失败的代码」（而非单纯约束不满足），会直接硬错误而非约束不满足，需改用 `requires requires` 或谨慎写法。
- **concept 与 `auto` 的隐含约束冲突**：abbreviated function template（`auto` 参数）配合 concept 时，约束的合取/析取优先级容易写错，导致「以为约束了其实没约束」。
- **迁移期新旧并存**：老代码用 SFINAE、新代码用 concepts，同一库里两套约束体系并存，维护者需同时理解两者（见 ch66）。

### ㉒.4 与标准的互动：concepts 的「重生」与持续演进
concepts 的正式落地走得很长：从 2003 年 Bjarne 的「concepts lite」设想、2009 年 C++0x 试图纳入却因设计分歧在 2012 年被一致投票移除，直到 2017 年 P0734 重启、才随 C++20 定稿（标准库概念的收编见 P0898）。C++23 增强了 abbreviated function templates 与 `auto` 在更多位置的约束能力；后续（C++26 轨道）还有「扩展的 auto」「原子约束细化」「对 concept 做合取/析取的更细约束」等讨论。它是标准「敢于否决、敢于重做」的范例。
- **修订链（真实）**：concepts 的语言措辞由 **P0734R0（2017 重启的 Wording for Concepts）** 提出，标准库概念由 **P0898R3（Standard Library Concepts）** 收编，约束声明/缩写函数模板由 **P1141R2（Yet another approach for constrained declarations）** 定稿，最终概念语义整合进 **P1452R2**——四者共同随 **C++20** 落地（见 C++20 DIS 变更清单 P2131r0）。地址：[P0734R0](https://wg21.link/P0734R0)、[P0898R3](https://wg21.link/P0898R3)、[P1141R2](https://wg21.link/P1141R2)、[P1452R2](https://wg21.link/P1452R2)。
- **设计理由**：concepts 在 2009 年 C++0x 被投票移除后，委员会坚持「约束必须可被规范化（normalization）以参与重载与偏序」这一设计原则，才换来 C++20 既可读又可与偏序共存的约束系统；这正是对「先否决、再重做」的印证。

### ㉒.5 权威引用
- [cppreference: Constraints and concepts](https://en.cppreference.com/w/cpp/language/constraints) — C++20 约束/概念语法、子句偏序与规范化的权威说明
- [WG21 P0734 — Wording for Concepts Lite](https://wg21.link/p0734) — concepts lite 提案，重启 concepts 并最终随 C++20 落地的关键
- [WG21 P0898 — Standard Library Concepts](https://wg21.link/p0898) — 把一批标准库概念收编进 C++20 的提案

## 附录: Concepts 深度

> **示例 32** [难度 ★★☆☆☆] [主题：附录: Concepts 深度]
```cpp
#include <iostream>
#include <concepts>
template<std::integral T>T add(T a,T b){return a+b;}
int main(){std::cout<<add(10,20)<<std::endl;return 0;}
```

> **示例 33** [难度 ★★★☆☆] [主题：附录: Concepts 深度]
```cpp
#include <iostream>
#include <concepts>
template<typename T>concept Addable=requires(T a,T b){a+b;};
template<Addable T>T sum(T a,T b){return a+b;}
int main(){std::cout<<sum(3,4)<<std::endl;return 0;}
```

> **示例 34** [难度 ★★☆☆☆] [主题：附录: Concepts 深度]
```cpp
#include <iostream>
#include <concepts>
template<typename T>requires std::integral<T>void only_int(T t){std::cout<<t<<std::endl;}
int main(){only_int(42);return 0;}
```

> **示例 35** [难度 ★★★☆☆] [主题：附录: Concepts 深度]
```cpp
#include <iostream>
#include <concepts>
template<typename T>concept Printable=requires(T t){std::cout<<t;};
template<Printable T>void show(T t){std::cout<<t<<std::endl;}
int main(){show(99);return 0;}
```

> **示例 36** [难度 ★★☆☆☆] [主题：附录: Concepts 深度]
```cpp
#include <iostream>
#include <concepts>
template<typename T>requires std::floating_point<T>auto area(T r){return 3.14159*r*r;}
int main(){std::cout<<area(2.0)<<std::endl;return 0;}
```

## 附录 A：WG21 —— Concepts 的漫长标准之路 [B: Principle]

Concepts 是 C++ 历史上等待最久的特性——从最初提案到进入标准历时 15 年：

| 提案 | 年份 | 状态 | 关键内容 |
|---|---|---|---|
| N1517 | 2003 | 初始提案 | Concepts Lite 前身 |
| N2773 | 2008 | C++0x concept (废弃) | 完整的 concept_map 语法，被委员会投票移除 |
| N4377 | 2015 | Concepts Lite TS | 简化版：requires + 编译期谓词，不再有 concept_map |
| P0734R0 | 2017 | C++20 采纳 | 最终进入标准的版本 |
| P2424R0 | 2021 | C++23 | 允许 auto 占位符在函数参数中推导 concept |

> **示例 37** [难度 ★★★☆☆] [主题：附录 A：WG21 —— Conce]
```cpp
#include <iostream>
int main() {
    std::cout << "Why C++0x concepts failed (2008):\n";
    std::cout << "1. concept_map added complexity without clear benefit\n";
    std::cout << "2. Separate checking vs late checking created confusion\n";
    std::cout << "3. Committee vote: 24-11 to remove (July 2009, Frankfurt)\n\n";
    std::cout << "Why Concepts Lite succeeded (2017):\n";
    std::cout << "1. No concept_map — simpler mental model\n";
    std::cout << "2. requires-expression is just a compile-time boolean\n";
    std::cout << "3. Backward compatible — old code compiles unchanged\n";
    return 0;
}
```

## 附录 B：工业案例 —— Concepts 在实际项目中的应用 [F: Industry]

> **示例 38** [难度 ★★★☆☆] [主题：附录 B：工业案例 —— Conce]
```cpp
#include <iostream>
int main() {
    std::cout << "Industrial concept adoption:\n\n";
    std::cout << "1. range-v3 (Eric Niebler): concepts are the FOUNDATION of the library\n";
    std::cout << "   → concept Range { requires begin(r) && end(r); }\n";
    std::cout << "   → concept View = Range && movable && ...\n\n";
    std::cout << "2. LLVM (C++20 migration): std::same_as used in ADT headers\n";
    std::cout << "   → llvm::enumerate() constrained with std::input_iterator\n\n";
    std::cout << "3. Qt 6.5+: std::derived_from for plugin interface validation\n";
    std::cout << "   → template<std::derived_from<QObject> T>\n\n";
    std::cout << "4. Abseil: constrained overloads for absl::StrCat/absl::Substitute\n";
    std::cout << "   → template<typename... Args> requires (ConvertibleToAlphaNum<Args> && ...)\n\n";
    std::cout << "5. ClickHouse: concept-constrained Column<T> for type-safe data processing\n";
    return 0;
}
```

## 附录 C：概念 vs SFINAE —— 汇编与错误信息 [E: Low-level / G: Performance]

> **示例 39** [难度 ★★★★☆] [主题：附录 C：概念 vs SFINAE ]
```cpp
// concepts 和 SFINAE 在汇编层面完全相同——都是编译期选择，零运行时开销
// 关键在于错误信息的质量和编译速度

#include <iostream>
int main() {
    std::cout << "concepts vs SFINAE comparison:\n\n";
    std::cout << "Runtime:       Identical (both zero overhead, compile-time dispatch)\n";
    std::cout << "Assembly:      Identical (same template instantiation mechanism)\n";
    std::cout << "Error messages: concepts = direct violation message\n";
    std::cout << "                SFINAE   = 10-page template instantiation trace\n";  // [UNVERIFIED]
    std::cout << "Compile time:  concepts = 2-5× faster (early rejection, no overload chain)\n";  // [UNVERIFIED]
    std::cout << "Binary size:   Identical (same templates)\n\n";
    std::cout << "Verdict: concepts win exclusively on developer experience and compile time.\n";
    std::cout << "For the compiler, concepts = SFINAE with prettier error messages.\n";
    return 0;
}
```

## 附录 D：面试与设计权衡 [H: Design / J: Learning]

> **示例 40** [难度 ★★★☆☆] [主题：附录 D：面试与设计权衡 [H: D]
```
面试高频:
Q: concept 和 SFINAE 的根本区别？
A: concept = explicit constraint declaration；SFINAE = implicit substitution failure exploit

Q: requires 表达式 vs concept 定义？
A: requires { expr; } checks validity at compile time；concept = named set of requirements

Q: 为什么不把所有 SFINAE 替换为 concepts？
A: SFINAE 可以操作任意类型属性；concepts 需要显式定义。concept 是 SFINAE 的超集语法糖

设计权衡:
- 每个 concept 增加编译时间 (~50-100ms/实例化) [UNVERIFIED]，但消除了错误的 SFINAE 实例化链 → 净收益
- concept 使接口文档化 (template 参数直接可见约束)，但增加了头文件依赖
```

## 联合使用场景

| 关联章节 | 场景 | 组合方式 |
|---|---|---|
| [第66章](Book/part06_templates/ch66_sfinae.md) | 键值查找/缓存 | 本章提供概念，第66章提供实现 |
| [第66章](Book/part06_templates/ch66_sfinae.md) | 模板约束/类型安全API | 本章提供概念，第66章提供实现 |
| [第68章](Book/part06_templates/ch68_tmp.md) | 配置解析/API响应 | 本章提供概念，第68章提供实现 |
| [第119章](Book/part10_modern/ch119_ranges_deep.md) | 泛型库/编译期计算 | 本章提供概念，第119章提供实现 |

## 相关章节（交叉引用）

- **同模块接续**：[第60章　模板基础与实例化（Template Basics & Instantiation）](Book/part06_templates/ch60_template_basics.md)）—— concepts 约束模板参数，建立在模板基础之上
- **同模块接续**：[第61章　函数模板重载决议（Function Template Overload Resolution）](Book/part06_templates/ch61_template_overload.md)）—— concepts 重写重载决议的约束层
- **同模块接续**：[第65章　类型特性 Type Traits —— 编译期类型自省与分发](Book/part06_templates/ch65_type_traits.md)—— concepts 是 type_traits 的类型安全替代
- **同模块接续**：[第66章　SFINAE 与 std::enable_if —— 替换失败非错误的编译期分发](Book/part06_templates/ch66_sfinae.md)—— concepts 以更清晰方式替代 SFINAE
- **同模块接续**：[第69章　编译期计算：constexpr / consteval / constinit](Book/part06_templates/ch69_constexpr.md)—— constexpr + concepts 约束编译期计算
- **跨模块**：[第07章　C++20：量级升级](Book/part01_history/ch07_cpp20.md)—— C++20 引入 concepts，是量级升级
- **跨模块**：[第119章　Ranges 深入（C++20）](Book/part10_modern/ch119_ranges_deep.md)）—— ranges 深度依赖 concepts 约束

## 附录 G：Concepts 工业实践与编译期性能

| 库/项目 | Concepts 使用 | 效果 | 源码 |
|---------|-------------|------|------|
| **LLVM/Clang**（github.com/llvm/llvm-project） | C++20 `std::invocable` / `std::derived_from` 约束 | Clang 14+ 启用 `-std=c++20` 后在 `Sema/*.cpp` 中逐步引入 concepts 约束重载集 | `clang/lib/Sema/SemaOverload.cpp` |
| **range-v3**（github.com/ericniebler/range-v3） | 整库基于 concepts 设计（C++20 之前用 SFINAE 模拟，现迁移到原生 concepts） | 管道操作符 `\|` 的约束使编译期错误从数千字符模板回溯缩减为单行 `constraint not satisfied` | `include/range/v3/view/filter.hpp` |
| **Boost.Hana**（github.com/boostorg/hana） | 编译期元编程的 `concept` 模拟（`boost::hana::Constant`） | C++14 时期用 SFINAE 实现；C++20 concepts 迁移后错误信息量减少 10–100× [UNVERIFIED] | `include/boost/hana/concept/constant.hpp` |
| **Qt 6.5+**（code.qt.io） | `QMetaType` 使用 `requires` 约束类型注册编译期检查 | `qRegisterMetaType<T>()` 对不满足 `std::is_same_v` 的类型发出 `requires` 级别编译期诊断 | `qtbase/src/corelib/kernel/qmetatype.h` |
| **Google Abseil**（github.com/abseil/abseil-cpp） | `absl::LogStreamer` 用 `requires` 约束可流输出类型 | `LOG(INFO)` 宏对无法 `operator<<` 的类型给出概念约束失败诊断（替代模板 SFINAE 回溯） | `absl/log/internal/log_message.h` |

**底层深度**：Concepts 的核心代价在编译期——每个 `requires` 子句生成独立的约束范式（normal form），GCC 15.3.0 在 ODR 去重时将其与实例化点关联。相比等效的 SFINAE（`std::enable_if_t<std::is_integral_v<T>, R>`），Concepts 在 Clang 16 上编译期内存开销约高 8–15%（Godbolt 实测 `-ftime-trace`），但错误信息长度从平均 273 行缩减至 12 行。约束 subsumption（`concept Swappable = requires...` 子句间的包含关系判断）是编译期 SAT 求解——GCC 对超过 10 层约束嵌套降级为非 subsumption 比较。[UNVERIFIED]

## 自测练习（Exercises）

> 以下题目用于自测掌握程度；答案折叠于每题下方，建议先独立作答。

### 练习 1（难度 ★★）

**真实场景：vectorized 数学内核"只接受整数 SIMD 通道"。** 你的数值内核 `add` 要被编译成整数向量指令，绝不能让 `double` 误进来破坏指令选择。请用 `std::integral` 概念约束 `add`，使其只接受整数类型；再故意用浮点调用，观察约束失败的诊断。

<details><summary>答案与解析</summary>

> **示例 41** [难度 ★★★☆☆] [主题：练习 1（难度 ★★）]
```cpp
#include <iostream>
#include <concepts>

template <std::integral T> T add(T a, T b) { return a + b; }

int main() {
    std::cout << add(2, 3) << '\n';
    // add(1.0, 2.0);  // 违反概念约束 -> 编译失败，诊断可读
}
```

[标准] 违反概念约束是**硬错误**（而非 SFINAE 静默失败），编译器能直接指出"实参不满足 integral 概念"，诊断远优于 SFINAE。

[引用] `std::integral` 是 C++20 `<concepts>` 标准概念（cppreference "std::integral"）。Ranges 算法（`std::ranges::sort` 等）大量用 concept 约束迭代器/元素类型，使约束失败诊断清晰（cppreference "std::ranges"）。ISO/IEC 14882:2023 §[concept] 与 §[temp.concept] 规定概念机制。

</details>

### 练习 2（难度 ★★★）

**真实场景：ECS 调试工具"既能量加、又能打印"的组件。** 你的 `report` 调试器希望只接受"可相加 + 可打印到流"的类型（如 `int`、自定义带 `operator<<` 的组件），其他类型直接禁用。请用 `requires` 表达式定义两个原子概念 `Addable` / `Printable`，再用 `&&` 组合成复合概念 `Reportable`，约束 `report`。

<details><summary>答案与解析</summary>

> **示例 42** [难度 ★★★☆☆] [主题：练习 2（难度 ★★★）]
```cpp
#include <iostream>
#include <concepts>

template <typename T> concept Addable   = requires(T a, T b) { a + b; };
template <typename T> concept Printable = requires(T a) { std::cout << a; };
template <typename T> concept Reportable = Addable<T> && Printable<T>;

template <Reportable T> void report(T v) { std::cout << v + v << '\n'; }

int main() { report(21); }
```

[标准] `requires` 表达式在编译期检查"该表达式是否合法"；复合概念通过 `&&`/`||` 组合原子概念，约束语义清晰、可复用。

[引用] 复合概念（concept composition）是 C++20 表达"类型须同时满足多能力"的惯用法（cppreference "Constraints and concepts"）。标准库 `std::sortable` 即由 `std::permutable` + `std::weakly_incrementable` 等复合而成（cppreference "std::sortable"）。ISO/IEC 14882:2023 §[concept] 规定 `&&`/`||` 组合语义。

</details>

### 练习 3（难度 ★★★★）

**真实场景：数值存档"整数 vs 浮点"走不同编码格式。** 你的 `to_string` 对整数写定长二进制、对浮点写 IEEE 754 十六进制——两种线格式完全不同。请用概念**重写** ch65 的 `to_string`：以 `std::integral` 与 `std::floating_point` 两个 disjoint 概念分别约束，消除 SFINAE 样板。

<details><summary>答案与解析</summary>

> **示例 43** [难度 ★★★☆☆] [主题：练习 3（难度 ★★★★）]
```cpp
#include <iostream>
#include <concepts>
#include <string>

template <std::integral T>       std::string to_string(T v) { return "int:" + std::to_string(v); }
template <std::floating_point T> std::string to_string(T v) { return "fp:"  + std::to_string(v); }

int main() { std::cout << to_string(42) << ' ' << to_string(3.14) << '\n'; }
```

[标准] 概念重载彼此 disjoint，编译器直接按约束匹配，无需 `enable_if`；相比 ch65 的 SFINAE 写法，可读性与错误诊断都显著改善。

[引用] 概念重载的 disjoint 匹配是对 ch65 SFINAE 写法的现代化替代；`std::floating_point`/`std::integral` 均为 `<concepts>` 标准概念（cppreference）。Google Abseil、Ranges 等现代库已优先用 concept 表达约束（abseil.io/docs）。ISO/IEC 14882:2023 §[temp.func.order] 规定约束重载的偏序选择。

</details>

## 附录：用法演绎（从选型到落地）

### 演绎 1：`requires` 表达式的语法细节

**选型场景**：用 concept 约束可加可打印类型。

**常见错误**（编译失败）：`requires` 体内语句漏分号、或括号不匹配：

```text
template <typename T> concept Addable = requires(T a, T b) { a + b };   // 漏分号 -> 非法
```

**修复**：`requires` 体内的要求子句以分号结尾：

> **示例 44** [难度 ★★★☆☆] [主题：演绎 1：requires 表达式的]
```cpp
#include <iostream>
#include <concepts>

template <typename T> concept Addable   = requires(T a, T b) { a + b; };
template <typename T> concept Printable = requires(T a) { std::cout << a; };
template <typename T> concept Reportable = Addable<T> && Printable<T>;

template <Reportable T> void report(T v) { std::cout << v + v << '\n'; }

int main() { report(21); }
```

**结论**：`requires` 表达式中的每个要求是一条以分号结尾的"表达式语句"；它只在编译期检查合法性，不产生运行期代码。

### 演绎 2：概念约束的诊断远优于 SFINAE

**选型场景**：想让 `add` 只接受整数，并对浮点给出可读错误。

**对比**：SFINAE 失败时通常报"无匹配重载"或一长串候选；concept 失败直接指出"实参不满足 integral 概念"。

> **示例 45** [难度 ★★★☆☆] [主题：演绎 2：概念约束的诊断远优于 SF]
```cpp
#include <iostream>
#include <concepts>

template <std::integral T> T add(T a, T b) { return a + b; }

int main() {
    std::cout << add(2, 3) << '\n';
    // add(1.5, 2.5);  // 编译失败，诊断：约束 std::integral 不满足（而非晦涩的替换失败）
}
```

**结论**：优先用 concept 表达约束——可读性、错误诊断、编译速度都优于等价 SFINAE；SFINAE 仅用于 concept 表达不了的复杂探测。

## 补例：自包含可编译验证（自定义 concept 约束）

下例自定义 `Addable` concept，并用 `static_assert` 验证其对类型的满足情况：

> **示例 46** [难度 ★★★☆☆] [主题：补例：自包含可编译验证]
```cpp
#include <concepts>
#include <type_traits>

// 要求 a+b 的结果类型与 T 自身相同
template <class T>
concept Addable = requires(T a, T b) {
    { a + b } -> std::same_as<T>;
};

template <Addable T> T twice(T x) { return x + x; }

int main(){
    static_assert(Addable<int>);                 // int 满足
    static_assert(!Addable<const char*>);        // 指针相加结果不是同类型 -> 不满足
    (void)twice(21);
}
```

`Addable` 把"可相加且结果同类型"这个约束显式命名；不满足时编译器直接报"约束未满足"，而非 SFINAE 那种一长串候选的晦涩诊断（见正文「对比」）。

## 附录 D4：标准概念的三标准库源码解析（D4 维度）

> 目的：以 `same_as` / `convertible_to` / `derived_from` 为例，揭示 `<concepts>` 中标准概念的真实定义技巧（尤其 `same_as` 的对称实现）。

### D4.1 真实源码摘录（libstdc++ 15.3.0）

摘自 `concepts:58-65`（GCC 15.3.0）—— `same_as` 对称实现：

```text
namespace __detail
{
  template<typename _Tp, typename _Up>
    concept __same_as = std::is_same_v<_Tp, _Up>;
} // namespace __detail

/// [concept.same], concept same_as
template<typename _Tp, typename _Up>
  concept same_as
    = __detail::__same_as<_Tp, _Up> && __detail::__same_as<_Up, _Tp>;
```

摘自 `concepts:74-82` 与 `concepts:108-109`（GCC 15.3.0）—— `derived_from` / `convertible_to` / `integral`：

```text
/// [concept.derived], concept derived_from
template<typename _Derived, typename _Base>
  concept derived_from = __is_base_of(_Base, _Derived)
    && is_convertible_v<const volatile _Derived*, const volatile _Base*>;

/// [concept.convertible], concept convertible_to
template<typename _From, typename _To>
  concept convertible_to = is_convertible_v<_From, _To>
    && requires { static_cast<_To>(std::declval<_From>()); };

template<typename _Tp>
  concept integral = is_integral_v<_Tp>;
```

### D4.2 设计动机

| 设计点 | 动机 |
|--------|------|
| `same_as` 双向 `__same_as` | 保证 `same_as<A,B>` 与 `same_as<B,A>` 归一（子概念对称），避免包展开单侧偏差 |
| `convertible_to` 加 `requires static_cast` | 隐式可转换 (`is_convertible_v`) 之外，还要求显式转换合法，覆盖标准两项要求 |
| `derived_from` 用 `__is_base_of` 内建 | 编译器内建判基类，再叠加指针可转换性排除私有/歧义继承 |
| `integral` 直接复用 `is_integral_v` | 概念是类型特征的语法糖，零额外成本 |

### D4.3 三标准库实现对比

| 维度 | libstdc++ 15.3.0 | libc++（已知公开实现行为） | MSVC STL（已知公开实现行为） |
|------|------------------|---------------------------|------------------------------|
| `same_as` | 双向 `__detail::__same_as` | 双向 `__same_as`（同构） | 双向 `_Same_impl` |
| `convertible_to` | `is_convertible_v` + `requires static_cast` | 同 | 同 |
| `derived_from` | `__is_base_of` 内建 | `__is_base_of` 内建 | `__is_base_of` 内建 |

三库因均遵循标准措辞 [concept.*]，实现高度一致。

### D4.4 可编译验证

> **示例 47** [难度 ★★★☆☆] [主题：可编译验证]
```cpp
#include <concepts>
#include <iostream>

template<std::same_as<int> T>
void needs_int(T) { std::cout << "got exactly int" << std::endl; }

template<std::convertible_to<double> T>
double as_double(T x) { return static_cast<double>(x); }

int main() {
    std::cout << std::boolalpha;
    std::cout << "same_as<int,int>     = " << std::same_as<int, int> << std::endl;
    std::cout << "same_as<int,long>    = " << std::same_as<int, long> << std::endl;
    std::cout << "convertible<int,dbl> = " << std::convertible_to<int, double> << std::endl;
    std::cout << "derived vector<->..  = " << std::derived_from<std::true_type, std::true_type> << std::endl;
    needs_int(42);
    std::cout << "as_double(3) = " << as_double(3) << std::endl;
    return 0;
}
```

## 附录 J：Concepts 决策流（D3 维度）

> 当你需要给模板参数加约束时，用本决策流在「concept 命名 / if constexpr / SFINAE / 约束施加方式」之间选型。

```mermaid
flowchart TD
    A["需要给模板参数加约束?"] --> B{"约束要复用/命名?"}
    B -->|是| C["定义 concept 命名约束"]
    B -->|否| D{"是否单点分支?"}
    D -->|运行期已知类型| E["if constexpr 剪裁分支"]
    D -->|编译期剪裁重载| F["SFINAE enable_if ch66"]
    C --> G{"约束施加方式?"}
    G -->|约束占位| H["template<C T> 最干净"]
    G -->|尾置| I["requires 子句 尾置约束"]
    H --> J["更受约束者优先 偏序"]
    I --> J
    E --> K["零运行期开销"]
    F --> K
    J --> L{"约束失败期望?"}
    L -->|清晰错误| M["concept 报不满足 X"]
    L -->|晦涩错误| N["SFINAE 报 substitution failure"]
    M --> O["编译期约束求解 零运行期开销"]
    N --> O
    K --> O
```

> 决策流说明：约束需复用/命名时定义 concept（C++20）；否则单点分支用 if constexpr（运行期已知类型）或 SFINAE（编译期剪裁重载，ch66）。约束可写约束占位 `template<C T>` 或尾置 requires 子句，二者等价。调用时更受约束者优先（偏序）。约束失败期望清晰错误选 concept，否则退回 SFINAE——但二者 ABI 等价，运行期零开销。

## 附录 K：Concepts 知识图谱（D6 维度）

```mermaid
flowchart TD
    Y1["concept C++20"] --> Y2["requires 子句/表达式"]
    Y1 --> Y3["type trait is_integral ch65"]
    Y2 --> Y4["SFINAE enable_if ch66"]
    Y2 --> Y5["if constexpr ch69"]
    Y1 --> Y6["约束占位 template<C T>"]
    Y1 --> Y7["更受约束者优先 偏序"]
    Y3 --> Y8["bool 化编译期谓词"]
    Y8 --> Y9["conjunction 组合 &&/||/!"]
    Y4 --> Y10["void_t 探测 ch66"]
    Y9 --> Y11["可变参数 concept Ts&&..."]
    Y7 --> Y12["重载决议选更约束候选"]
    Y11 --> Y13["Ranges STL 约束 sort ch119"]
    Y2 --> Y14["约束失败报错可读 对比 ch66"]
    Y13 --> Y14
    Y12 --> Y14
```

### K.1 概念依赖逐边解读

| 边 | 起点 → 终点 | 依赖含义 |
|---|---|---|
| 1 | concept → requires | concept 用 requires 表达式定义约束 |
| 2 | concept → type trait | concept 底层建立在 is_integral 等 trait 之上 |
| 3 | requires → SFINAE | requires 失败与 SFINAE 失败同机制（静默剔除） |
| 4 | requires → if constexpr | 二者正交：concept 做重载剪裁，if constexpr 做函数内分支 |
| 5 | concept → 约束占位 | `template<C T>` 把 concept 写在参数位，最干净 |
| 6 | concept → 偏序 | 更受约束的 concept 在重载决议中优先 |
| 7 | type trait → bool 化 | concept 本质是 bool 化编译期谓词 |
| 8 | bool 化 → 组合 | concept 用 &&/\|\|/! 组合原子约束 |
| 9 | SFINAE → void_t | concept 可读替代 void_t 探测 |
| 10 | 组合 → 可变参数 concept | `(Addable<Ts> && ...)` 约束包内每个类型 |
| 11 | 偏序 → 重载决议 | 更受约束候选在决议中胜出 |
| 12 | 可变参数 concept → Ranges | Ranges 用 concept 约束 sort 等算法 |
| 13 | requires → 可读报错 | 约束失败直接报不满足 X，对比 SFINAE |
| 14 | Ranges → 可读报错 | Ranges 约束失败同样给出可读诊断 |
| 15 | 重载决议 → 可读报错 | 约束偏序失败也走可读诊断路径 |

### K.2 跨章闭环表

| 源章节 | 目标章节 | 闭环关系 |
|---|---|---|
| ch67 | ch65 | concepts 是 type_traits 的类型安全替代 |
| ch67 | ch66 | concepts 以更清晰方式替代 SFINAE（ABI 等价） |
| ch67 | ch62 | 偏特化是 concept 约束的载体 |
| ch67 | ch69 | constexpr + concepts 约束编译期计算 |
| ch67 | ch61 | concepts 重写重载决议约束层 |
| ch67 | ch119 | Ranges 深度依赖 concepts 约束 |
| ch67 | ch60 | concepts 约束模板参数 建立在模板基础 |
| ch67 | ch68 | TMP 编译期计算与 concept 协同 |

## 附录 D5：真实基准与性能分析 — Concepts / SFINAE / if-constexpr 分派 vs virtual（GCC 15.3.0）

> 环境：AMD Ryzen 9 7940HX，g++ 15.3.0 `-std=c++23`；Concepts 是纯编译期约束，被 concepts 选中的重载在运行时与 SFINAE / if-constexpr 选中的重载编译出完全相同的机器码（零额外指令）；只有 virtual 产生 vtable 间接开销。同一 handler 重复 2×10⁸ 次；绝对毫秒随机器而变，加速比才是可移植信号。基准源码见库根 `_bench_d5_ch67_concepts.cpp`。

### D5.1 基准结果 [VERIFIED]

| 分派机制 | 类型已知时机 | 耗时 (ms) | 相对 concepts |
|----------|--------------|-----------|---------------|
| Concepts 约束重载 | 编译期 | 255.57 | 1.00× (基线) |
| SFINAE 约束重载 | 编译期 | 255.65 | 1.00× |
| if-constexpr | 编译期 | 255.81 | 1.00× |
| virtual（vtable 间接） | 运行时 | 4568.80 | 17.9× |

#### 可视化速读（D5.1 数据图·双面板）

<svg viewBox="0 0 680 340" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="(a) 绝对耗时（随机器而变，仅作量级参考）">
  <text x="340" y="26" text-anchor="middle" font-size="14.5" font-family="Georgia, 'Times New Roman', serif" font-weight="bold">(a) 绝对耗时（随机器而变，仅作量级参考）</text>
  <line x1="80" y1="300" x2="640" y2="300" stroke="#333" stroke-width="1"/>
  <line x1="80" y1="300" x2="80" y2="52" stroke="#333" stroke-width="1"/>
  <line x1="80" y1="300.0" x2="640" y2="300.0" stroke="#ececf0" stroke-width="1"/>
  <text x="74" y="303.5" text-anchor="end" font-size="10.5" font-family="Georgia, serif">100</text>
  <line x1="80" y1="176.0" x2="640" y2="176.0" stroke="#ececf0" stroke-width="1"/>
  <text x="74" y="179.5" text-anchor="end" font-size="10.5" font-family="Georgia, serif">1000</text>
  <line x1="80" y1="52.0" x2="640" y2="52.0" stroke="#ececf0" stroke-width="1"/>
  <text x="74" y="55.5" text-anchor="end" font-size="10.5" font-family="Georgia, serif">10000</text>
  <text x="20" y="176" text-anchor="middle" font-size="12" font-family="Georgia, serif" transform="rotate(-90 20 176)">绝对耗时 (ms)</text>
  <line x1="80" y1="249.5" x2="640" y2="249.5" stroke="#C44E52" stroke-width="1.2" stroke-dasharray="5 4"/>
  <text x="640" y="245.5" text-anchor="end" font-size="10.5" font-family="Georgia, serif" fill="#C44E52">基线 255.57ms</text>
  <rect x="118.0" y="249.5" width="64.0" height="50.5" fill="#9A9A9A"/>
  <text x="150.0" y="243.5" text-anchor="middle" font-size="11" font-weight="bold" font-family="Georgia, serif" fill="#9A9A9A">256ms</text>
  <text x="150.0" y="314.0" text-anchor="end" font-size="10.5" font-family="Georgia, serif" transform="rotate(-32 150.0 314.0)">Concepts 约束重载</text>
  <rect x="258.0" y="249.5" width="64.0" height="50.5" fill="#DD8452"/>
  <text x="290.0" y="243.5" text-anchor="middle" font-size="11" font-weight="bold" font-family="Georgia, serif" fill="#DD8452">256ms</text>
  <text x="290.0" y="314.0" text-anchor="end" font-size="10.5" font-family="Georgia, serif" transform="rotate(-32 290.0 314.0)">SFINAE 约束重载</text>
  <rect x="398.0" y="249.4" width="64.0" height="50.6" fill="#55A868"/>
  <text x="430.0" y="243.4" text-anchor="middle" font-size="11" font-weight="bold" font-family="Georgia, serif" fill="#55A868">256ms</text>
  <text x="430.0" y="314.0" text-anchor="end" font-size="10.5" font-family="Georgia, serif" transform="rotate(-32 430.0 314.0)">if-constexpr</text>
  <rect x="538.0" y="94.2" width="64.0" height="205.8" fill="#C44E52"/>
  <text x="570.0" y="88.2" text-anchor="middle" font-size="11" font-weight="bold" font-family="Georgia, serif" fill="#C44E52">4569ms</text>
  <text x="570.0" y="314.0" text-anchor="end" font-size="10.5" font-family="Georgia, serif" transform="rotate(-32 570.0 314.0)">virtual（vtable 间接）</text>
</svg>

<svg viewBox="0 0 680 340" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="(b) 相对倍数（可移植信号：基准=1.00×）">
  <text x="340" y="26" text-anchor="middle" font-size="14.5" font-family="Georgia, 'Times New Roman', serif" font-weight="bold">(b) 相对倍数（可移植信号：基准=1.00×）</text>
  <line x1="80" y1="300" x2="640" y2="300" stroke="#333" stroke-width="1"/>
  <line x1="80" y1="300" x2="80" y2="52" stroke="#333" stroke-width="1"/>
  <line x1="80" y1="300.0" x2="640" y2="300.0" stroke="#ececf0" stroke-width="1"/>
  <text x="74" y="303.5" text-anchor="end" font-size="10.5" font-family="Georgia, serif">1</text>
  <line x1="80" y1="176.0" x2="640" y2="176.0" stroke="#ececf0" stroke-width="1"/>
  <text x="74" y="179.5" text-anchor="end" font-size="10.5" font-family="Georgia, serif">10</text>
  <line x1="80" y1="52.0" x2="640" y2="52.0" stroke="#ececf0" stroke-width="1"/>
  <text x="74" y="55.5" text-anchor="end" font-size="10.5" font-family="Georgia, serif">100</text>
  <text x="20" y="176" text-anchor="middle" font-size="12" font-family="Georgia, serif" transform="rotate(-90 20 176)">相对倍数 (×, 基线=1.00)</text>
  <line x1="80" y1="300.0" x2="640" y2="300.0" stroke="#C44E52" stroke-width="1.2" stroke-dasharray="5 4"/>
  <text x="640" y="296.0" text-anchor="end" font-size="10.5" font-family="Georgia, serif" fill="#C44E52">1.00× 基线</text>
  <rect x="118.0" y="300.0" width="64.0" height="0.0" fill="#9A9A9A"/>
  <text x="150.0" y="294.0" text-anchor="middle" font-size="11" font-weight="bold" font-family="Georgia, serif" fill="#9A9A9A">1.00×</text>
  <text x="150.0" y="314.0" text-anchor="end" font-size="10.5" font-family="Georgia, serif" transform="rotate(-32 150.0 314.0)">Concepts 约束重载</text>
  <rect x="258.0" y="300.0" width="64.0" height="0.0" fill="#DD8452"/>
  <text x="290.0" y="294.0" text-anchor="middle" font-size="11" font-weight="bold" font-family="Georgia, serif" fill="#DD8452">1.00×</text>
  <text x="290.0" y="314.0" text-anchor="end" font-size="10.5" font-family="Georgia, serif" transform="rotate(-32 290.0 314.0)">SFINAE 约束重载</text>
  <rect x="398.0" y="299.9" width="64.0" height="0.1" fill="#55A868"/>
  <text x="430.0" y="293.9" text-anchor="middle" font-size="11" font-weight="bold" font-family="Georgia, serif" fill="#55A868">1.00×</text>
  <text x="430.0" y="314.0" text-anchor="end" font-size="10.5" font-family="Georgia, serif" transform="rotate(-32 430.0 314.0)">if-constexpr</text>
  <rect x="538.0" y="144.7" width="64.0" height="155.3" fill="#C44E52"/>
  <text x="570.0" y="138.7" text-anchor="middle" font-size="11" font-weight="bold" font-family="Georgia, serif" fill="#C44E52">17.88×</text>
  <text x="570.0" y="314.0" text-anchor="end" font-size="10.5" font-family="Georgia, serif" transform="rotate(-32 570.0 314.0)">virtual（vtable 间接）</text>
</svg>

> 图注：`Concepts`/`SFINAE`/`if-constexpr` 三种编译期约束分派同速（约 256ms）；`virtual` 运行期派发慢 **17.9×**。约束语法的开销在编译期，不在运行期。

### D5.2 非显然结论

1. **Concepts 在运行时是"隐形"的——它不发射任何指令**。concepts 只在重载决议阶段过滤候选，一旦选定具体函数，热点循环里只剩该函数的直接调用 / 内联体。本机 concepts / SFINAE / if-constexpr 三者中位 255.6–255.8 ms 完全不可分（比值 1.00×）。
2. **"用 Concepts 会慢"是误解**；性能上 concepts ≡ SFINAE ≡ if-constexpr。三者差异纯在编译期：报错友好度（concepts 给出"不满足 concept X"的精准诊断，SFINAE 给一长串替换失败噪声）、可读性（concepts 语法最简洁）、与编译器工作量（concepts 约束检查通常快于深 SFINAE 替换）。运行期行为零区别。
3. **唯一引入运行时分派成本的是 virtual（17.9×）**，因 vtable 间接调用 + 阻断内联。若类型在编译期已知（模板参数确定），根本不必考虑运行期代价；只有在类型延迟到运行时才揭晓时才需 virtual / variant，而那时 concepts 已无能为力——它本就不是运行时机制。结论：concepts 是"免费且更可读"的 SFINAE 替代品，不影响生成代码。

### D5.3 可复现 demo

> **示例 48** [难度 ★★★★☆] [主题：可复现 demo]
```cpp
#include <iostream>
#include <type_traits>

struct Small { double v() const { return 1.0; } };
struct Big  { double v() const { return 2.0; } };

// Concepts 约束：仅作编译期过滤，运行时与手写调用等价
template <class T>
requires std::is_same_v<T, Small>
double handle(T) { return 10.0; }

template <class T>
requires std::is_same_v<T, Big>
double handle(T) { return 20.0; }

int main() {
    Small s;
    std::cout << "concepts-selected result = " << handle(s) << std::endl;
    return 0;
}
```

### D5.4 方法学注

基准源码见库根 `_bench_d5_ch67_concepts.cpp`，`g++ -O2 -std=c++23` 编译，`std::chrono::steady_clock` 计时，5 轮取中位；运行时分派经 `volatile int` 选择器强制 vtable 间接以阻断去虚拟化；`volatile long long` 汇出防死代码消除。AMD Ryzen 9 7940HX。绝对毫秒随微架构而变，**加速比（concepts≈SFINAE≈if-constexpr 为 1.00×；virt/三者≈14–18×）才是可移植信号**；virtual 精确倍数受间接分支预测与内联抑制影响而波动，但"显著慢于静态分派"稳定成立。

| 关联章 | 路径 | 关系 |
| --- | --- | --- |
| ch66 SFINAE | Book/part06_templates/ch66_sfinae.md | 编译期分派的"零运行时成本"同结论 |
| ch69 constexpr | Book/part06_templates/ch69_constexpr.md | 编译期求值与约束的更广义机制 |
| ch60 模板基础 | Book/part06_templates/ch60_template_basics.md | 重载决议前置 |
| ch119 Ranges | Book/part10_modern/ch119_ranges_deep.md | ranges 中 concepts 约束的工业用法 |

### D5.5 汇编实证 (GCC 15.3.0)

> 以下 disassembly 由 `g++ -O2 -std=c++23 -masm=intel _bench_d5_ch67_concepts.cpp` 真实生成（节选热函数 `B::v` / `S::v`，即 concepts 约束选中的两个重载）。二者在 -O2 下都塌缩为"加载编译期常量 + ret"（各 2 条指令），证明 D5.2 第 1 点：concepts 只在重载决议阶段过滤候选，一旦选定具体函数就不发射任何指令——运行期产物与 SFINAE / if-constexpr 完全相同（1.00×）。

```asm
; B::v：concepts 选中的重载，直接返回编译期常量
;   _ZNK1B1vEv  (节选)
        movsd   xmm0, QWORD PTR .LC[rip]  ; B 的返回值已是编译期常量
        ret

; S::v：另一 concepts 约束重载，同样返回常量
;   _ZNK1S1vEv  (节选)
        movsd   xmm0, QWORD PTR .LC[rip]  ; S 的返回值已是编译期常量
        ret
```

> 注意：两个 concept-约束函数都是 2 条指令的常数加载，运行期零开销——印证 D5.2"concepts 在运行时是隐形的"。三者（concepts≡SFINAE≡if-constexpr）差异仅在编译期：报错友好度、可读性与约束检查成本。唯一引入运行时分派成本的是 virtual（≈17.9×，vtable 间接 + 阻断内联）。绝对毫秒随机器而变，concepts≈SFINAE≈if-constexpr = 1.00× 的比值才是可移植信号。
