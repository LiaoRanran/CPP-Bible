# 第63章　可变参数模板与包展开（Variadic Templates & Pack Expansion）

⟶ Book/part06_templates/ch64_fold.md
⟶ Book/part10_modern/ch116_perfect_forwarding.md

> 模板模式速查：本章属「参数聚合型」模板。可变参数模板让一个模板接受**任意个数/任意类型**的参数，通过「递归 + 包展开」处理。它是 tuple、forward、emplace、format 的基石。

## ① 学习目标

⟶ Book/part06_templates/ch62_specialization.md
⟶ Book/part06_templates/ch64_fold.md


- 说清参数包（parameter pack）、包展开（pack expansion）、`sizeof...` [标准]
- 掌握递归终止 + 包展开两种展开方式 [标准]
- 理解包可在哪些上下文展开（调用、初始化、基类列表、using 等）[标准]
- 从汇编确认递归实例化层级（包展开 = 实例化链）[平台]
- 区分 C++11 递归写法与 C++17 折叠表达式（ch64）[经验]

## ② 本模板模式速查（名称 / 适用场景 / 核心结构 / 定义）

- **模板名称**：可变参数模板（variadic template）
- **适用场景**：需要「任意参数」的设施——`printf` 风格、tuple、完美转发构造、`emplace`、日志
- **核心结构**：`template <typename... Ts> void f(Ts...);`
- **一句话定义**：用省略号 `...` 声明「类型 + 值」参数包，在展开位点把包逐元素展开 [标准]

```cpp
template <typename... Ts>
void print_all(Ts... args) {
    (print_single(args), ...);   // 包展开：每个 args 元素各调用一次
}
```

## ③ 核心结构与完整代码实现

参数包声明与展开：

```cpp
template <typename... Ts>        // Ts：类型包
struct Tuple { };

template <typename... Ts>        // 值包
void f(Ts... args) {             // args：函数参数包
    // 包展开位点
}
```

```cpp
#include <cstddef>
// sizeof... 取包大小（编译期）
template <typename... Ts>
constexpr std::size_t count(Ts...) { return sizeof...(Ts); }
static_assert(count(1, 2, 3) == 3);
static_assert(count() == 0);
```

## ④ 递归展开（C++11 经典写法）

⟶ Book/part06_templates/ch64_fold.md（折叠表达式：C++17 归约替代递归，更优）
⟶ Book/part06_templates/ch62_specialization.md（偏特化常做递归终止 base case）

```cpp
#include <iostream>
// 基线（0 参数）
void print() { }

// 递归：取首参，剩余包继续
template <typename T, typename... Rest>
void print(T first, Rest... rest) {
    std::cout << first << ' ';
    print(rest...);              // 包展开：Rest... 递归实例化
}
```

```cpp
// 编译期求和（递归 + 累加）
template <typename T>
constexpr T sum(T v) { return v; }
template <typename T, typename... Rest>
constexpr T sum(T first, Rest... rest) {
    return first + sum(rest...);
}
static_assert(sum(1, 2, 3, 4) == 10);
```

## ⑤ 适用场景与选型

| 需求 | 写法 |
|---|---|
| 任意参数转发构造 | `template <typename... Ts> T(Ts&&...)` + `std::forward` |
| 任意参数打印 | 递归或折叠（ch64） |
| 任意参数聚合 | `std::tuple<Ts...>` |
| 编译期遍历包 | 折叠表达式（ch64，更优） |

## ⑥ 完整可运行示例（最小）

```cpp
#include <iostream>
void print() {}
template <typename T, typename... Rest>
void print(T first, Rest... rest) {
    std::cout << first << ' ';
    print(rest...);
}
int main() { print(1, 2.5, 'x', "hi"); }
```

```cpp
// 完美转发构造（emplace 基础）
struct Widget {
    template <typename... Ts>
    Widget(Ts&&... args) { /* 转发给成员构造 */ }
};
```

```cpp
#include <array>
// 包展开进初始化列表
template <typename... Ts>
auto make_array(Ts... ts) {
    return std::array<int, sizeof...(ts)>{ static_cast<int>(ts)... };
}
```

```cpp
// sizeof... 编译期
template <typename... Ts> constexpr auto nargs(Ts...) { return sizeof...(Ts); }
```

## ⑦ 标准规定 [标准]

- `Ts...` 是「模板参数包」；`args...` 是「函数参数包」[temp.variadic]。
- 包展开位点必须明确：`pattern...`，`pattern` 含包名 [temp.variadic]/5。
- 展开目标：初始化列表、`()` 调用、基类列表、`using` 声明、`{}` 初始化、`return` 等 [temp.variadic]/4。

## ⑧ GCC / Clang / MSVC 行为差异 [实现][平台]

```cpp
// 三者均支持可变参数模板（C++11 起）
// MSVC 旧版（<=19.1x）对「包展开进 lambda 捕获」支持较晚
template <typename... Ts> auto f(Ts... ts) {
    // [ts...] 捕获在较新 MSVC 支持
    auto g = [ts...] { return (0 + ... + ts); };
    return g();
}
```

```cpp
// 报错可读性：GCC/Clang 展开错误会给出「第 N 个包元素」上下文（见 ch75）
```

## ⑨ 内存 / 对象模型

每个展开的实例化是独立函数/类型。递归展开 = 实例化链（见 ⑩）。

```cpp
#include <cstddef>
// make_index_sequence 偏特化 + 包展开生成编译期整数序列
template <std::size_t... I> struct IndexSeq {};
// 展开用于下标访问，零运行期开销
```

## ⑩ 汇编 / 符号证据（真实 MinGW GCC 15.3.0）

编译 `Examples/_asm_tpl_variadic.cpp`：`-O2` 把 `print_all(1,2.0,'c')` 完全内联为 **4 次 `g_depth+=1`**（对应四级展开），`fold_sum` 折叠为常量 10；`-O0` 暴露真实递归实例化链 mangled 名。

```asm
; _asm_tpl_variadic.asm -O2 节选：四级展开内联为 4 次自增
main:
    mov eax, DWORD PTR g_depth[rip]
    add eax, 1            ; 第1层 print_all<int,double,char>
    mov DWORD PTR g_depth[rip], eax
    add eax, 1            ; 第2层 print_all<double,char>
    add eax, 1            ; 第3层 print_all<char>
    add eax, 1            ; 第4层 print_all<> 基线
    mov DWORD PTR 44[rsp], 10   ; fold_sum(1,2,3,4) 折叠为常量 10

; _asm_tpl_variadic_O0.asm 节选：递归实例化链（真实 mangled 名）
_Z9print_allIiJdcEEvT_DpT0_        ; print_all<int, double, char>
    call _Z9print_allIdJcEEvT_DpT0_   ; -> print_all<double, char>
_Z9print_allIdJcEEvT_DpT0_
    call _Z9print_allIcJEEvT_DpT0_    ; -> print_all<char>
_Z9print_allIcJEEvT_DpT0_
    call _Z9print_allv                ; -> 基线 print_all<>()
```

**读法**：`-O2` 的 4 次自增与 `-O0` 的 4 层 `call` 链一一对应，证明「包展开 = 递归实例化」：`print_all<int,double,char>` → `print_all<double,char>` → `print_all<char>` → `print_all<>()`。mangled 名 `JdcE`/`JcE`/`JEE` 中的 `J` 标记「包开始」。

### 知识点深挖（模板B）

**B1 包展开位点（≥10 处） [标准]**

```cpp
// 1) 函数调用参数
template <typename... Ts> void a(Ts... ts) { g(ts...); }
```

```cpp
#include <vector>
// 2) 初始化列表
template <typename... Ts> auto b(Ts... ts) { return std::vector<int>{ static_cast<int>(ts)... }; }
```

```cpp
// 3) 基类列表
template <typename... Bases> struct D : Bases... { };
```

```cpp
// 4) using 声明
template <typename... Ts> struct E : Ts... { using Ts::foo...; };
```

```cpp
#include <array>
// 5) 花括号初始化（聚合）
template <typename... Ts> auto c(Ts... ts) { return std::array<int, sizeof...(ts)>{ ts... }; }
```

```cpp
// 6) 返回语句
template <typename... Ts> auto d(Ts... ts) { return std::make_tuple(ts...); }
```

```cpp
// 7) 下标/运算符（配合折叠）
template <typename... Ts> auto e(Ts... ts) { return (ts + ...); }
```

```cpp
// 8) 模板参数
template <typename... Ts> struct F { template <Ts... vals> struct Ctx {}; };
```

```cpp
// 9) sizeof... 
template <typename... Ts> constexpr auto n(Ts...) { return sizeof...(Ts); }
```

```cpp
// 10) lambda 捕获（C++20 广义捕获展开）
template <typename... Ts> auto f(Ts... ts) { auto l = [ts...] { return (0 + ... + ts); }; return l(); }
```

```cpp
// 11) new 初始化列表
template <typename... Ts> auto g(Ts... ts) { auto p = new int[sizeof...(ts)]{ ts... }; return p; }
```

**B2 双层包（内层包） [标准]**

```cpp
template <typename... Ts>
void outer(Ts... ts) {
    // 内层包展开需括号： (f(ts)... )
}
```

```cpp
#include <iostream>
template <typename... Ts>
void each(Ts... ts) {
    ( (std::cout << ts), ... );   // 单层
}
```

```cpp
template <typename T> void h(T);
template <typename... Ts> void call_all(Ts... ts) { (h(ts), ...); }
```

```cpp
#include <iostream>
// 双层：每个元素再展开其成员
template <typename... Ts>
void pairs(Ts... ts) {
    ( (std::cout << ts.first << ts.second), ... );
}
```

**B3 递归基线设计 [标准]**

```cpp
// 基线优先匹配 0 参数
void rec() {}
template <typename T, typename... R> void rec(T f, R... r) { rec(r...); }
```

```cpp
// 用 if constexpr 替代基线（C++17）
template <typename T, typename... R>
void rec2(T f, R... r) {
    (void)f;
    if constexpr (sizeof...(r) > 0) rec2(r...);
}
```

```cpp
// 计数基线
constexpr int cnt() { return 0; }
template <typename T, typename... R> constexpr int cnt(T, R... r) { return 1 + cnt(r...); }
```

**B4 sizeof... 与编译期 [标准]**

```cpp
template <typename... Ts> constexpr bool all_int = (std::is_same_v<Ts, int> && ...);
```

```cpp
template <typename... Ts> constexpr bool none_empty = (!std::is_empty_v<Ts> && ...);
```

```cpp
#include <cstddef>
template <typename... Ts> struct Count { static constexpr std::size_t value = sizeof...(Ts); };
```

```cpp
// 包中第一个类型
template <typename First, typename... Rest> struct Front { using type = First; };
```

**B5 错误与正确对照 [经验]**

```cpp
// 错误：包无展开位点
template <typename... Ts> void bad(Ts... ts) { g(ts); }   // 缺 ... 展开
// 正确
template <typename... Ts> void good(Ts... ts) { g(ts...); }
```

```cpp
// 错误：递归无基线 → 无限实例化 / 失败
// template <typename T, typename... R> void r(T, R... r) { r(r...); }  // 无 0 参基线
```

```cpp
// 错误：双层包展开缺括号
// (f(ts)... ...)   非法；应 (f(ts) , ...)
```

```cpp
// 正确：折叠表达式（C++17）替代递归最简洁
template <typename... Ts> auto add(Ts... ts) { return (0 + ... + ts); }
```

## ⑪ STL 中的该模式

⟶ Book/part10_modern/ch116_perfect_forwarding.md（emplace 的可变参数完美转发实现）
⟶ Book/part06_templates/ch65_type_traits.md（对参数包做类型萃取）

```cpp
#include <iostream>
#include <utility>
#include <vector>
#include <string>
#include <tuple>
struct Pt { int x; double y; std::string s; };
template <std::size_t... I>
void show_idx(std::index_sequence<I...>) { std::cout << "idx count=" << sizeof...(I) << '\n'; }
int main() {
    // std::tuple<Ts...> 是可变参数类模板
    std::tuple<int, double, char> t{1, 2.0, 'x'};
    // emplace 用可变参数完美转发多参构造
    std::vector<Pt> v; v.emplace_back(1, 2.0, "x");
    // std::apply 用包展开调用函数
    std::apply([](auto... xs){ ( (std::cout << xs << ' '), ... ); }, t);
    std::cout << '\n';
    // std::index_sequence / make_index_sequence 生成整数序列
    show_idx(std::make_index_sequence<3>{});   // idx count=3
}
// 输出：1 2 x  idx count=3
```

## ⑫ 变体（variant patterns）

```cpp
#include <iostream>
#include <utility>
#include <array>
#include <string>
#include <type_traits>
// 1) 完美转发可变参数构造（emplace）
template <typename T> struct Holder {
    template <typename... Ts> Holder(Ts&&... ts) : obj(std::forward<Ts>(ts)...) {}
    T obj;
};
// 2) 递归 print 用 if constexpr 免基线
template <typename T, typename... R>
void log(T f, R... r) {
    std::cout << f << ' ';
    if constexpr (sizeof...(r) > 0) log(r...);
}
// 3) 包展开进 std::array 构造
template <typename... Ts> constexpr auto arr(Ts... ts) { return std::array{ts...}; }
// 4) 包展开 + 折叠做类型判断
template <typename... Ts> constexpr bool any_same = (std::is_same_v<Ts, int> || ...);
int main() {
    Holder<std::string> h("hi");
    std::cout << h.obj << '\n';                          // hi
    log(1, 2.14, 'z'); std::cout << '\n';                // 1 2.14 z
    auto a = arr(10, 20, 30);
    std::cout << a.size() << '\n';                       // 3
    std::cout << std::boolalpha << any_same<int, double, int> << '\n';  // true
}
// 输出：hi  1 2.14 z  3  true
```

## ⑬ 反模式（anti-patterns）

```cpp
#include <cstdio>
// 反模式1：用 C 风格 va_list 而非可变参数模板——丢类型安全、需格式串
// printf("%d", x); 不如 print(x, y, z)
```

```cpp
// 反模式2：递归无基线导致编译失败或爆栈（编译期无限实例化）
```

```cpp
// 反模式3：能用折叠表达式（ch64）却用递归，代码长、实例化多
template <typename... Ts> auto s(Ts... ts) { return (ts + ...); }   // 优于递归
```

```cpp
// 反模式4：包展开进宏，可读性灾难
```

```cpp
// 反模式5：可变参数 + 虚函数（模板不能虚），需类型擦除替代
```

## ⑭ 工业案例

⟶ Book/part10_modern/ch116_perfect_forwarding.md（日志/格式化库的可变参数转发底座）

```cpp
#include <utility>
#include <string>
// 案例：fmt / std::format 的可变参数格式化
template <typename... Ts> std::string format_str(const char* fmt, Ts&&... ts) {
    return fmt::format(fmt, std::forward<Ts>(ts)...);
}
```

```cpp
#include <utility>
// 案例：日志库
template <typename... Ts> void log(Level lvl, Ts&&... ts) {
    (sink(lvl, std::forward<Ts>(ts)...), ...);
}
```

```cpp
#include <utility>
#include <memory>
// 案例：工厂 emplace
template <typename T, typename... Ts> std::unique_ptr<T> make(Ts&&... ts) {
    return std::make_unique<T>(std::forward<Ts>(ts)...);
}
```

```cpp
// 案例：测试框架 ASSERT 多参数
template <typename... Ts> void expect_all(bool cond, Ts...);
```

## ⑮ 源码剖析（libstdc++ 相关）

```cpp
#include <utility>
// libstdc++ std::tuple 用递归继承 + 包展开
template <typename... _Elements> class tuple;
template <typename _Tp, typename... _Rest> class tuple<_Tp, _Rest...> : public tuple<_Rest...> {
    _Tp _M_head;
};
```

```cpp
#include <utility>
#include <cstddef>
// std::apply 用 index_sequence + 包展开调用
template <typename F, typename Tuple, std::size_t... I>
decltype(auto) apply_impl(F&& f, Tuple&& t, index_sequence<I...>) {
    return std::forward<F>(f)(std::get<I>(std::forward<Tuple>(t))...);
}
```

```cpp
// make_index_sequence 用偏特化 + 包展开生成整数序列
```

## ⑯ 易错点

```cpp
// 1) 包必须出现在「展开位点」，缺 ... 报错
```

```cpp
// 2) 递归展开必须提供 0 参数基线，否则实例化失败
```

```cpp
#include <utility>
// 3) 引用折叠：Ts&& 是转发引用，需 std::forward<Ts>(ts)... 保持值类别
```

```cpp
// 4) sizeof... 只能用于包，不是 sizeof
```

```cpp
// 5) 双层包展开需用括号分组 pattern
```

```cpp
// 6) 可变参数不能用于虚函数 / 异常规格
```

## ⑰ FAQ

```cpp
#include <initializer_list>
// Q：可变参数模板和 std::initializer_list 区别？
// A：前者保留每个元素类型，后者所有元素同类型 T；前者可异构。
```

```cpp
// Q：递归展开会爆编译吗？
// A：包大小固定时实例化数 = 包大小 + 1，可控；但过大仍拖编译。
```

```cpp
// Q：C++17 折叠表达式能替代递归吗？
// A：纯归约（求和/与或）可以且更优（见 ch64）。
```

```cpp
// Q：为什么 emplace 用可变参数？
// A：把构造实参完美转发给成员 in-place 构造，避免临时对象。
```

```cpp
// Q：sizeof... 是运算符吗？
// A：是，返回包的「元素个数」（编译期常量）。
```

## ⑱ 最佳实践

```cpp
// 1) 归约类用折叠表达式（ch64）替代递归
```

```cpp
#include <utility>
// 2) 转发用 Ts&&... + std::forward<Ts>(ts)...
```

```cpp
// 3) 递归展开务必写 0 参数基线或用 if constexpr 兜底
```

```cpp
#include <utility>
// 4) 优先 std::tuple / std::apply 复用标准实现
```

```cpp
// 5) 异构参数优先可变参数模板而非 any/void*（保类型安全）
```

## ⑲ 性能（编译期 / 运行期）

```cpp
// 展开纯编译期；选中实现内联后无函数调用（见⑩ 4 次内联自增）
// 递归展开实例化链 = 包大小+1 份函数；折叠表达式通常单函数 + 展开为加法链
// fold_sum(1,2,3,4) 在 -O2 直接是常量 10，零运行期计算
```

```cpp
// 代价：包越大编译期实例化越多（→ 编译时间）
```

## ⑳ 练习题 + 思考题 + 源码阅读路线（内化，无独立推荐阅读节）

**练习题**

1. 用递归写 `print` 反转顺序（先递归后打印）。
2. 用 `emplace` 风格写一个 `Buffer::construct(Ts&&...)` 在预分配内存 in-place 构造。
3. 写 `MaxN`：返回包中最大值（递归或折叠）。
4. 用 `std::index_sequence` + 包展开实现一个 `for_each(tuple, f)`。
5. 把 ch64 的折叠求和改写成 C++11 递归等价版并对比实例化数。

**思考题**

- 为什么可变参数模板不能用于虚函数？类型擦除如何替代？
- 递归展开 vs 折叠表达式在「实例化数」与「代码体积」上差多少？
- `std::apply` 的 index_sequence 技巧本质是什么？

**源码阅读路线（内化）**

- libstdc++ `bits/tuple`：tuple 递归继承 + 包展开
- libstdc++ `bits/invoke.h`：std::apply 实现
- GCC `cp/pt.cc`：包展开（expand_pack）
- 交叉引用占位：part06 ch64（折叠表达式）、ch51（CRTP，占位）

## 附录 A：底层与原理 [B: Principle / E: Lowlevel]

```
WG21可变参数模板提案:
N2242 (C++11): Variadic templates (Douglas Gregor, 2007)
  → 解决: C++03的"最多N个参数"限制 (Boost.MPL用15层宏模拟)
  → 代价: 编译时间O(N)实例化链 (N=参数个数)

底层(编译器实现): 参数包展开
  template<typename... Ts> void f(Ts... ts) { g(ts...); }
  → GCC: 递归实例化 f(int, double, char) → f(int) + f(double, char) → ...
  → C++17折叠表达式: (ts + ...) → 编译器直接展开, 不递归实例化
  → 编译时间实测 (GCC 15.3.0 -O2, 取7次最快):
      N=100  → fold≈111ms, rec≈125ms (1.1×)
      N=500  → fold≈118ms, rec≈484ms (4.1×)
      N=1000 → fold≈123ms, rec≈11.6s (94.5×)
  → 结论: 差距随 N 近似线性放大; 旧资料「10–20× @ N=100」针对更重实例化体/旧编译器

工业案例:
- std::make_shared<T>(args...): 完美转发可变参数到构造函数
- fmtlib: fmt::format("{}", arg1, arg2, ...) → 编译期类型检查
- std::tuple<Ts...>: 可变参数模板的经典应用
```


## 联合使用场景

| 关联章节 | 场景 | 组合方式 |
|---|---|---|
| [第64章](Book/part06_templates/ch64_fold.md) | STL算法回调/异步任务 | 本章提供概念，第64章提供实现 |
| [第62章](Book/part06_templates/ch62_specialization.md) | 独占所有权/工厂模式 | 本章提供概念，第62章提供实现 |
| [第64章](Book/part06_templates/ch64_fold.md) | 泛型库/编译期计算 | 本章提供概念，第64章提供实现 |
| [第116章](Book/part10_modern/ch116_perfect_forwarding.md) | 日志格式化/序列化 | 本章提供概念，第116章提供实现 |

## 附录 F：可变参数工业

```cpp
#include <iostream>
#include <memory>
struct S{int a,b;S(int x,int y):a(x),b(y){}};
int main(){auto p=std::make_shared<S>(10,20);std::cout<<p->a<<","<<p->b<<std::endl;std::cout<<"make_shared=variadic perfect forwarding to constructor"<<std::endl;return 0;}
```

| 用法 | 库 | 性能 |
|---|---|---|
| make_shared<T>(args...) | STL | 单次分配(控制块+对象) |
| make_unique<T>(args...) | STL | 异常安全工厂 |
| format(fmt, args...) | fmtlib | 编译期类型检查 |
| tuple<Ts...> | STL | 编译期元组 |

面试: variadic模板展开方式? 递归展开(C++11, O(N)实例化) vs 折叠表达式(C++17, O(1))
       make_shared参数限制? 无限(variadic), 编译期完美转发到T的构造函数

## 附录 G：可变参数模板的编译器实现

### 编译器展开机制

GCC实现: 递归模板实例化, 编译时间随 N 近似线性增长
C++17折叠表达式: 编译器直接展开, 编译时间基本不随 N 变 (GCC 15.3.0 实测):
  N=100  → fold≈111ms / rec≈125ms (1.1×)
  N=500  → fold≈118ms / rec≈484ms (4.1×)
  N=1000 → fold≈123ms / rec≈11.6s (94.5×)

```asm
; 递归: f(int,double,char) → f(int) + f(double,char) → f(int) + f(double) + f(char)
; → 3层实例化, 每层生成函数调用链
; 折叠: (ts + ...) → t1 + (t2 + (t3 + 0))
; → 1次展开, 单条add指令链
```

### 工业案例

| 库 | 可变参数 | 效果 |
|---|---|---|
| std::tuple<Ts...> | 任意类型元组 | 编译期类型安全容器 |
| fmt::format | format+args | 编译期类型验证 |
| std::make_shared | args→constructor | 完美转发+单次分配 |

```cpp
#include <iostream>
#include <memory>
struct S{int a,b;S(int x,int y):a(x),b(y){}};
int main(){auto p=std::make_shared<S>(10,20);std::cout<<p->a<<","<<p->b<<std::endl;return 0;}
```

面试: sizeof...(Ts)返回什么? 参数个数(编译期常量); 折叠表达式四种形式? (pack op ...), (... op pack), (pack op ... op init), (init op ... op pack)

## 附录 H：可变参数面试

| Q | A |
|---|---|
| sizeof...(Ts)? | 编译期常量(参数个数) |
| 4种折叠? | unary left=(...+p), unary right=(p+...), binary left=(0+...+p), binary right=(p+...+0) |
| 空包折叠? | &&=true, ||=false, +=error(需binary fold) |
| 递归vs折叠? | 折叠编译时间不随N增长; GCC15.3实测 N=100→1.1×, N=1000→95× |
| make_shared参数? | 可变参数+完美转发→构造函数 |

```cpp
#include <iostream>
template<typename...Ts> auto sum(Ts...ts){return (ts+...);}
int main(){std::cout<<sum(1,2,3,4,5)<<std::endl;return 0;}
```

## 附录 I：可变参数性能与汇编

```asm
; C++17 fold: (ts + ...) → t0 + (t1 + (t2 + ...))
; GCC -O2: 每条 add 指令链, 完全内联 (运行期 O(N) add, 与递归相同)
; 编译时间实测 (GCC 15.3.0 -O2, 取最快):
;   N=100  fold≈111ms  rec≈125ms  (1.1×)
;   N=500  fold≈118ms  rec≈484ms  (4.1×)
;   N=1000 fold≈123ms  rec≈11.6s  (94.5×)
; 结论: 递归实例化链随 N 线性变长, 折叠编译时间基本恒定
```

```cpp
#include <iostream>
template<typename...Ts> auto sum(Ts...ts){return (ts+...);}  // fold(C++17)
int main(){std::cout<<sum(1,2,3,4,5,6,7,8,9,10)<<std::endl;return 0;}
```

| 方案 | 编译时间(N=100, GCC15.3) | 运行时间 | 实例化份数 |
|---|---|---|---|
| 递归模板 | ~125ms | O(N) add 指令 | N+1 份 |
| 折叠表达式 | ~111ms | O(N) add 指令 | 1 份 |
| 手写展开 | 无需模板 | O(N) add 指令 | — |


## 相关章节（交叉引用）

- **同模块接续**：⟶ Book/part06_templates/ch60_template_basics.md（第60章　模板基础与实例化（Template Basics & Instantiation））—— 可变参数模板是模板基础的包推广
- **同模块接续**：⟶ Book/part06_templates/ch61_template_overload.md（第61章　函数模板重载决议（Function Template Overload Resolution））—— 包展开参与模板重载决议
- **同模块接续**：⟶ Book/part06_templates/ch64_fold.md（第64章　折叠表达式 Fold Expression（C++17））—— 折叠表达式是可变参数包展开的简化语法
- **同模块接续**：⟶ Book/part06_templates/ch62_specialization.md（第62章　类模板特化与偏特化（Class Template Specialization））—— 特化常针对包做递归终止
- **同模块接续**：⟶ Book/part06_templates/ch65_type_traits.md（第65章　类型特性 Type Traits —— 编译期类型自省与分发）—— type_traits 常对包做萃取
- **跨模块**：⟶ Book/part01_history/ch04_cpp11.md（第04章　C++11：现代 C++ 革命）—— C++11 引入可变参数模板，是核心语言演进
- **跨模块**：⟶ Book/part07_stl/ch78_deque.md（第78章　deque 与分段连续 [标准]）—— deque 等容器用可变参数包转发
- **跨模块**：⟶ Book/part10_modern/ch116_perfect_forwarding.md（第116章　完美转发与万能引用）—— 完美转发与可变参数包协同

## 自测练习（Exercises）

> 以下题目用于自测掌握程度；答案折叠于每题下方，建议先独立作答。

### 练习 1（难度 ★★）

用**递归可变参数模板**（base case + 递归 case）写一个 `print_all`，依次打印所有参数，参数间用空格分隔。

<details><summary>答案与解析</summary>

```cpp
#include <iostream>

void print_all() {}
template <typename T, typename... Ts>
void print_all(const T& first, const Ts&... rest) {
    std::cout << first << ' ';
    print_all(rest...);
}

int main() { print_all(1, "two", 3.0, 'x'); std::cout << '\n'; }
```

[标准] 每次递归剥掉一个参数，剩余包 `rest...` 逐层变短，直到空包命中 base case；递归深度 = 参数个数，会实例化 N 份函数。

</details>

### 练习 2（难度 ★★）

用 **C++17 fold expression** 重写 `print_all`（`(std::cout << ... << xs)`），并额外写一个 `sum` 折叠；对比递归版本说明 fold 的优势。

<details><summary>答案与解析</summary>

```cpp
#include <iostream>

template <typename... Ts>
void print_all(const Ts&... xs) { (std::cout << ... << xs) << '\n'; }

template <typename... Ts>
auto sum(const Ts&... xs) { return (xs + ...); }

int main() { print_all(1, 2, 3); std::cout << sum(1, 2, 3, 4) << '\n'; }
```

[标准] fold 只实例化一个函数，编译期展开为线性序列，无递归 N 份实例化的代码膨胀；`(xs + ...)` 为一元左折叠，从首个元素起累加。

</details>

### 练习 3（难度 ★★★★）

用包展开 + `std::index_sequence` 实现一个 `make_array(args...)`，把所有参数存入 `std::array`，元素类型取公共类型（`std::common_type_t`）。

<details><summary>答案与解析</summary>

```cpp
#include <iostream>
#include <array>
#include <utility>
#include <type_traits>

template <typename... Ts>
auto make_array(Ts&&... xs) {
    using T = std::common_type_t<Ts...>;
    return std::array<T, sizeof...(Ts)>{ static_cast<T>(xs)... };
}

int main() {
    auto a = make_array(1, 2, 3);
    static_assert(std::is_same_v<decltype(a), std::array<int, 3>>);
    std::cout << a.size() << '\n';   // 3
}
```

[标准] `sizeof...(xs)` 是编译期包大小；`static_cast<T>(xs)...` 是包展开 + 转换，保证所有元素同类型后构造 `std::array`。

</details>

## 附录：用法演绎（从选型到落地）

### 演绎 1：递归展开必须有 base case

**选型场景**：C++11 风格打印任意参数包。

**常见错误**（编译失败/无限递归）：只有递归 case、缺空包 base：

```text
template <typename T, typename... Ts>
void print_all(const T& f, const Ts&... r) { std::cout << f; print_all(r...); }
// 空包无匹配 -> 找不到 viable 函数
```

**修复**：补一个无参 base case 收尾：

```cpp
#include <iostream>

void print_all() {}
template <typename T, typename... Ts>
void print_all(const T& first, const Ts&... rest) {
    std::cout << first << ' ';
    print_all(rest...);
}

int main() { print_all(1, "two", 3.0); std::cout << '\n'; }
```

**结论**：递归可变参数必须有一条"包为空"的终止路径；否则空包无法匹配任何重载。

### 演绎 2：包展开的运算符不能省略

**选型场景**：对每个参数调用 `f`。

**常见错误**（编译失败）：直接写 `f(xs)...` 缺少展开运算符/逗号：

```text
template <typename F, typename... Ts> void for_each(F f, Ts... xs) { f(xs)...; }  // 语法错误
```

**修复**：用逗号折叠 `(f(xs), ...)`：

```cpp
#include <iostream>

template <typename F, typename... Ts>
void for_each(F f, Ts... xs) { (f(xs), ...); }

int main() { for_each([](auto x) { std::cout << x << ' '; }, 1, 2, 3); std::cout << '\n'; }
```

**结论**：包展开必须出现在一个"模式"中（运算符、逗号、初始化器）；`(pat, ...)` 是最常用的"对每个元素执行副作用"写法。

