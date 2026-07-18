# 第61章　函数模板重载决议（Function Template Overload Resolution）

⟶ Book/part06_templates/ch66_sfinae.md
⟶ Book/part06_templates/ch67_concepts.md

> 模板模式速查：本章属「决议控制型」模板。当非模板函数、函数模板、模板特化同时候选时，C++ 有一套**优先权 + 偏序（partial ordering）**规则决定最终调用谁。掌握它才能预测 `max(1, 2.0)` 这类调用到底落到哪个重载。

## ① 学习目标

⟶ Book/part06_templates/ch60_template_basics.md
⟶ Book/part06_templates/ch62_specialization.md


- 复述重载决议的 3 阶段：候选集 → 可行集 → 最佳匹配 [标准]
- 说清「非模板函数 > 更特化的模板 > 更泛化的模板」的优先权 [标准]
- 理解模板偏序（partial ordering）如何比较「谁更特化」[标准]
- 能从汇编反推决议结果（非模板符号 vs 内联的模板体）[平台]
- 避免二义（ambiguous）与「最意外绑定」[经验]

## ② 本模板模式速查（名称 / 适用场景 / 核心结构 / 定义）

- **模板名称**：函数模板重载决议（重载集含模板）
- **适用场景**：同一操作要对多种类型/形式多样提供，且要让「最贴合」的实现被选中（如 `std::swap` 对容器有特化）
- **核心结构**：`f(args)` 同时匹配 `void f(T)` / `void f(T*)` / `void f(int)` 等多候选
- **一句话定义**：对含模板的重载集，编译器按「非模板优先、偏序定模板胜负」选出唯一最佳可行函数 [标准]

```cpp
void f(int);              // 非模板
template <typename T> void f(T);     // 泛化模板
template <typename T> void f(T*);    // 更特化的模板
```

## ③ 核心结构与完整代码实现

重载决议三阶段 [标准]（候选集 → 可行集 → 最佳匹配）：

```cpp
#include <iostream>
// 阶段1：名称查找建立候选集 {log(int)非模板, log(T)泛化, log(T*)更特化}
// 阶段2：按实参隐式转换可行性筛选可行集
// 阶段3：可行集中按转换等级/偏序选最佳
void log(int)          { std::cout << "A:log(int)\n"; }          // (A) 非模板
template <typename T> void log(T)  { std::cout << "B:log(T)\n"; }   // (B) 泛化
template <typename T> void log(T*) { std::cout << "C:log(T*)\n"; }   // (C) 更特化
int main() {
    int x = 0;
    log(42);   // A 非模板优先 → 选 A
    log(&x);   // A 不可行(int*→int)，B/C 可行，C 更特化 → 选 C
}
// 输出：A:log(int)  C:log(T*)
```

## ④ 优先权规则（非模板 > 模板）

```cpp
void g(int);                  // 非模板 优先
template <typename T> void g(T);
void t() {
    g(1);     // 两个都可行；非模板 g(int) 胜出
}
```

```cpp
// 关键：只有「同样可行」时非模板才优先；若非模板不可行，才轮到模板
void h(double);
template <typename T> void h(T*);
void u() {
    int x;
    // h(1.0) -> h(double) 非模板；h(&x) -> 仅 h(T*) 可行 -> 模板
}
```

## ⑤ 偏序（Partial Ordering）：谁更特化

```cpp
template <typename T> void f(T);      // F1 泛化
template <typename T> void f(T*);     // F2 更特化（指针）
// 偏序测试：用 F2 的形参推导 F1 成功，反之用 F1 推导 F2 失败 → F2 更特化
void k() {
    int x;
    f(&x);     // 两个都可行；F2 更特化 → 选 F2
}
```

```cpp
// 偏序也适用于多个模板之间
template <typename T> void p(T, T);           // P1
template <typename T> void p(T*, T*);         // P2 更特化
void q() {
    int a, b;
    p(&a, &b);  // P2 更特化胜出
    p(1, 2);    // 仅 P1 可行
}
```

## ⑥ 完整可运行示例（最小）

```cpp
#include <iostream>
void f(int)  { std::cout << "f(int)\n"; }
template <typename T> void f(T) { std::cout << "f(T)\n"; }
template <typename T> void f(T*) { std::cout << "f(T*)\n"; }
int main() {
    int x = 0;
    f(42);    // f(int)
    f(x);     // f(int)
    f(&x);    // f(T*)
}
```

```cpp
#include <iostream>
template <typename T> void g(T) { std::cout << "g(T)\n"; }
template <typename T> void g(T*) { std::cout << "g(T*)\n"; }
int main() {
    int x; g(&x);    // g(T*) 更特化
    g(1);            // g(T) 唯一可行
}
```

```cpp
// 引用 vs 值：const 引用模板比非 const 值模板更泛化还是更特化？
template <typename T> void h(T);
template <typename T> void h(const T&);
void use() { int x; h(x); }   // 两个可行；h(T) 对 int 是直接匹配，h(const T&) 需加 const → h(T) 胜
```

## ⑦ 标准规定 [标准]

- 非模板函数在可行集中与模板平级时**优先** [temp.over.link / over.match.best]。
- 偏序用于模板之间打破平局：能推导对方但对方不能推导自己者「更特化」[temp.deduct.partial]。
- 转换序列等级：完全匹配(含派生→基/数组→指针/函数→指针) > 提升 > 标准转换 > 用户定义转换 [over.ics.rank]。

## ⑧ GCC / Clang / MSVC 行为差异 [实现][平台]

```cpp
// 三者均严格遵循偏序（现代 MSVC 已修好旧版两阶段查找不严的问题）
// 唯一常见差异：SFINAE 报错信息可读性与候选项展示（见 ch75）
```

```cpp
// MSVC 旧版在「依赖基类成员函数」决议上更宽松；GCC/Clang 更严
template <typename T> void m(T x) { foo(x); }   // foo 依赖 T，实例化点才查
```

## ⑨ 内存 / 对象模型

决议是**纯编译期**行为，不产生运行期数据。选定函数后调用约定与参数传递与普通函数一致。

```cpp
// 选定 f(int) 后，参数按普通调用约定进寄存器（见 ch47/part05 调用约定，占位）
void f(int);  // 决议结果固定，无运行期开销
```

## ⑩ 汇编 / 符号证据（真实 MinGW GCC 15.3.0，-O2 -masm=intel）

编译 `Examples/_asm_tpl_overload.cpp`（每个重载向 `volatile g_log` 写不同值，强制保留语义）。main 内联后暴露决议结果：

```asm
; _asm_tpl_overload.asm 节选（MinGW GCC 15.3.0, -O2）
_Z1fi:                          ; f(int) 非模板
    movsxd  rax, DWORD PTR g_i[rip]
    lea     edx, 1[rax]
    mov     DWORD PTR g_i[rip], edx
    lea     rdx, g_log[rip]
    mov     DWORD PTR [rdx+rax*4], 100      ; f(int) 写 100
    ret
; main 内联展开：
    mov DWORD PTR [r9+rax*4], 100    ; f(42)   -> f(int)       写 100
    mov DWORD PTR [r9+rdx*4], 100    ; f(x)    -> f(int)       写 100
    mov DWORD PTR [r9+rax*4], 300    ; f(&x)   -> f(T*) 更特化 写 300
    mov DWORD PTR [r9+rdx*4], 22     ; g(&x)   -> g(T*)        写 22
    mov DWORD PTR [r9+rax*4], 11     ; g(7)    -> g(int)       写 11
```

**读法**：`f(42)`、`f(x)` 都落到 `_Z1fi`（`f(int)`，非模板优先）；`f(&x)` 因 `int*→int` 不可隐式转换使非模板不可行，只剩两个模板，偏序选更特化的 `f(T*)`，内联体写 **300**；`g(&x)→g(T*)` 写 22，`g(7)→g(int)` 写 11。五条调用的最终写入值**逐一坐实决议规则**。

### 知识点深挖（模板B）

**B1 三阶段决议逐步推演 [标准]**（≥10 例）

```cpp
void f(short);              template <typename T> void f(T);
void a(){ f(1); }           // int->short 标准转换 vs int->int 完全匹配：模板 f(int) 完全匹配胜
```

```cpp
void f(long); f(int);       template <typename T> void f(T);
void b(){ f(1L); }          // 1L: f(long) 完全匹配，模板 f(long) 也匹配；非模板优先 → f(long)
```

```cpp
template <typename T> void f(T);  template <typename T> void f(T*);
void c(){ int x; f(&x); }   // f(T*) 更特化胜
```

```cpp
void f(int);  template <typename T> void f(T);
void d(){ const int x=0; f(x); }  // f(int) 非模板优先（const int->int 限定转换，平级时非模板胜）
```

```cpp
template <typename T> void f(T);  template <typename T> void f(const T&);
void e(){ int x; f(x); }   // f(T) 完全匹配（无 const 加），f(const T&) 需加 const；f(T) 胜
```

```cpp
template <typename T> void f(T);  template <typename T> void f(volatile T*);
void g(){ volatile int x; f(&x); }  // 仅 f(volatile T*) 可行
```

```cpp
void f(int*);  template <typename T> void f(T*);
void h(){ int x; f(&x); }   // 两者同：f(int*) 非模板优先
```

```cpp
template <typename T> void f(T);  template <typename T, typename U> void f(T, U);
void i(){ f(1); }        // 单参数版胜（参数个数更少，更匹配）
```

```cpp
template <typename T> void f(T); template <typename T> void f(T, int=0);
void j(){ f(1); }        // 单参数版胜（无默认实参参与匹配优先级）
```

```cpp
struct B{}; struct D: B{};
void f(B);  template <typename T> void f(T);
void k(){ f(D{}); }       // f(B) 需派生->基（标准转换）；f(D) 完全匹配；模板 f(D) 胜
```

```cpp
void f(B);  void f(D);
void m(){ f(D{}); }       // f(D) 更匹配（派生类优先于基类转换）
```

**B2 偏序推导双向测试 [标准]**

```cpp
template <typename T> void p(T);
template <typename T> void p(T*);
// 用 p(T*) 推导 p(T)：成功；用 p(T) 推导 p(T*)：失败 → p(T*) 更特化
```

```cpp
template <typename T> void q(const T&);
template <typename T> void q(T&);
// q(T&) 比 q(const T&) 更特化（非 const 引用更窄）
```

```cpp
template <typename T> void r(T, T);
template <typename T, typename U> void r(T, U);
// r(T,U) 更特化（参数间关联更强）
```

```cpp
#include <vector>
template <typename T> void s(std::vector<T>&);
template <typename T> void s(T&);
// s(vector<T>&) 更特化
```

**B3 SFINAE 在决议中的角色 [标准]**

```cpp
template <typename T> auto f(T x) -> decltype(x.foo(), void()) { }
template <typename T> auto f(T x) -> decltype(x.bar(), void()) { }
// 推导 substitution 失败者被静默移出候选集（SFINAE）
```

```cpp
template <typename T, typename = std::enable_if_t<std::is_integral_v<T>>>
void g(T);
template <typename T, typename = std::enable_if_t<std::is_floating_point_v<T>>>
void g(T);
// 浮点实参：整数版 enable_if 失败 → 移出候选
```

```cpp
template <typename T> void h(T, std::enable_if_t<std::is_pointer_v<T>, int> = 0);
template <typename T> void h(T, std::enable_if_t<!std::is_pointer_v<T>, int> = 0);
```

**B4 二义（ambiguous）触发条件 [经验]**

```cpp
template <typename T> void f(T);
template <typename T> void f(T, T = T{});
// f(1) 两候选同等级 → 二义（不同模板参数数但都匹配单一实参）
```

```cpp
template <typename T> void g(T);  template <typename U> void g(U);
// 同一模板两次声明 → 不是重载，重复定义
```

```cpp
struct A{}; struct B{};
template <typename T> void h(T, int);
template <typename T> void h(int, T);
void u(){ h(1, 1); }   // 两候选转换等级相同 → 二义
```

**B5 错误与正确对照 [经验]**

```cpp
// 错误：以为模板一定优先
void f(int);  template <typename T> void f(T);
void bad(){ f(1); }    // 实际 f(int) 非模板优先，不是模板
```

```cpp
// 正确：想用模板请去掉同名非模板，或用不同名字
template <typename T> void f_tmpl(T) { }
```

```cpp
// 错误：重载集二义
template <typename T> void k(T);  template <typename T> void k(const T&);
void bad(){ int x; k(x); }   // 注意：k(T) 对 int 完全匹配，k(const T&) 需加 const → 不二义；但若都 const 则二义
```

## ⑪ STL 中的该模式

```cpp
#include <iostream>
#include <vector>
#include <utility>
int main() {
    // std::swap：对 std::vector 选中容器特化版（O(1) 交换内部指针）
    std::vector<int> a{1, 2}, b{3, 4};
    std::swap(a, b);                 // 选中 vector 特化 swap
    // std::begin / std::end：对数组、容器、initializer_list 多候选
    int arr[3] = {10, 20, 30};
    std::cout << *std::begin(arr) << '\n';   // 数组重载 → 10
    // std::distance：随机迭代器 O(1)
    std::cout << std::distance(std::begin(arr), std::end(arr)) << '\n'; // 3
    // std::forward / std::move：引用折叠 + 重载实现完美转发
    int v = 5;
    std::cout << std::move(v) << '\n';        // 5
}
// 输出：10  3  5
```

## ⑫ 变体（variant patterns）

```cpp
#include <iostream>
#include <concepts>
#include <type_traits>
// 1) 标签调度：用空标签类型区分重载
struct tag_int {}; struct tag_str {};
void proc(tag_int, int)  { std::cout << "int\n"; }
void proc(tag_str, const char*) { std::cout << "str\n"; }
// 2) 约束重载：C++20 用 requires 区分
template <typename T> requires std::integral<T>      void f(T) { std::cout << "integral\n"; }
template <typename T> requires std::floating_point<T> void f(T) { std::cout << "floating\n"; }
// 3) 尾置返回类型 + decltype 参与决议
template <typename T> auto g(T x) -> decltype(x + 0) { return x; }
// 4) 转发引用重载(T&&)易劫持拷贝构造，需用 enable_if/requires 排除自身类型（见⑬/⑯）
int main() {
    proc(tag_int{}, 1);        // int
    proc(tag_str{}, "hi");     // str
    f(42);                     // integral
    f(3.14);                   // floating
    std::cout << g(7) << '\n'; // 7
}
// 输出：int  str  integral  floating  7
```

## ⑬ 反模式（anti-patterns）

```cpp
// 反模式1：重载集二义导致编译失败
template <typename T> void f(T);  template <typename T> void f(T*);
// 这其实 OK；但若再加 template <typename T> void f(const T*) 就可能二义
```

```cpp
// 反模式2：用模板重载替代虚函数做运行期多态 → 失去运行时分发
// 模板是编译期决议，异构容器无法用函数模板重载处理
```

```cpp
// 反模式3：在头文件大量重载模板拖慢编译且报错难读
// 用 Concepts（ch67）替代 SFINAE 重载群
```

```cpp
// 反模式4：转发引用重载与构造冲突
struct S {
    template <typename T> S(T&&) {}   // 劫持拷贝/移动构造
};
```

```cpp
// 反模式5：依赖隐式转换做重载，可读性差、易二义
void f(int);  void f(double);  f(1.0f);  // float->int 与 float->double 谁优先？易踩坑
```

## ⑭ 工业案例

```cpp
#include <iostream>
#include <array>
#include <vector>
#include <string>
// 案例1：std::array 的 swap 特化更高效（不逐元素交换，仅交换控制块）
template <typename T, std::size_t N>
void fast_swap(std::array<T,N>& a, std::array<T,N>& b) noexcept { a.swap(b); }
// 案例2：序列化框架按类型分派（自包含演示）
struct Output { void put(int v) { std::cout << v << ' '; } };
void serialize(int v, Output& o)                  { o.put(v); }            // 整数
void serialize(const std::string& s, Output& o)   { for (char c : s) o.put(c); } // 字符串
int main() {
    std::array<int, 3> a{1, 2, 3}, b{9, 8, 7};
    fast_swap(a, b);                          // 选中 array 特化 swap
    std::cout << a[0] << '\n';                // 9
    Output o; serialize(42, o); std::cout << '\n';        // 42
    serialize(std::string("hi"), o); std::cout << '\n';   // h i
}
// 输出：9  42  h i
```

## ⑮ 源码剖析（libstdc++ 相关）

```cpp
#include <utility>
// libstdc++ std::swap 主模板
template <typename _Tp>
constexpr void swap(_Tp& __a, _Tp& __b) noexcept {
    _Tp __tmp = std::move(__a);
    __a = std::move(__b);
    __b = std::move(__tmp);
}
// 各容器提供成员 swap 与特化，决议时优先选中
```

```cpp
// GCC overmatch.c：重载决议主流程；pt.cc 做偏序推导
```

## ⑯ 易错点

```cpp
// 1) 非模板优先于模板——不要以为模板会「自动」胜出
```

```cpp
// 2) 转发引用（T&&）会参与所有决议，易意外劫持拷贝构造
```

```cpp
// 3) 两候选转换等级相同 → 二义；用更特化或约束打破
```

```cpp
// 4) 函数模板不能偏特化，只能用重载或 enable_if 模拟
```

```cpp
// 5) 派生类隐藏基类同名模板 → 用 using Base::f 拉回候选集
```

```cpp
// 6) 默认实参不参与决议等级，仅用于可行性
```

## ⑰ FAQ

```cpp
// Q：为什么 f(42) 选了 f(int) 而非 f(T)？
// A：两者都可行且等级相同，非模板优先。
```

```cpp
// Q：偏序和特化有什么区别？
// A：偏序是针对「模板之间」的更特化比较；全特化是「完全指定实参」的单独实体。
```

```cpp
// Q：如何让两个模板不二义？
// A：让其一更特化（偏序胜）或用不同约束（Concepts / enable_if）。
```

```cpp
// Q：函数模板能偏特化吗？
// A：不能。用重载集合或类模板包装（见 ch62）。
```

```cpp
// Q：转发引用重载怎么避免劫持构造？
// A：用 std::enable_if / requires 排除自身类型与拷贝。
```

## ⑱ 最佳实践

```cpp
// 1) 优先 Concepts（ch67）约束重载，替代 SFINAE 重载群，报错清晰
```

```cpp
// 2) 非模板与模板同名时清楚注释优先级，避免意外
```

```cpp
// 3) 转发引用重载务必约束，或用 Tag 分发绕过构造劫持
```

```cpp
// 4) 重载集保持「正交」：每个重载覆盖不相交的类型区间
```

```cpp
// 5) 公共 API 避免依赖隐式转换做决议
```

## ⑲ 性能（编译期 / 运行期）

```cpp
// 决议纯编译期，选定后调用开销与普通函数一致（含内联）
// 代价：重载+模板候选越多，编译期决议越慢、报错越长（见 ch75）
```

```cpp
// 内联后模板重载与普通函数无差别：上文 f(&x)->300 直接内联进 main
```

```cpp
// 模板实例化数量随重载组合数增长 → 控制候选规模
```

## ⑳ 练习题 + 思考题 + 源码阅读路线（内化，无独立推荐阅读节）

**练习题**

1. 预测 `f(1.0)`, `f("hi")`, `f(std::vector<int>{})` 在含 `f(int)/f(T)/f(T*)/f(const char*)` 的候选集中各落谁。
2. 写 `print` 重载集：对整数、浮点、字符串、容器各不同实现。
3. 用偏序写一个 `min` 支持「两个相同类型」与「指针取所指向值比较」两版。
4. 构造一个会产生 ambiguous 的调用并修复它。
5. 用 Concepts 重写一个 SFINAE 重载群（见 ch67 占位）。

**思考题**

- 非模板优先规则对「给旧接口加模板重载」意味着什么风险？
- 转发引用重载劫持构造的本质原因是什么？（引用折叠 + 模板优先推导）
- 为什么 C++20 Concepts 比 SFINAE 更适合表达「更特化」？

**源码阅读路线（内化）**

- GCC `cp/call.cc`：重载决议（perform_overload_resolution）
- GCC `cp/pt.cc`：偏序推导（more_specialized）
- libstdc++ `bits/move.h`：std::swap 与特化
- 交叉引用占位：part06 ch67（Concepts）、ch66（SFINAE）

## 附录 A：原理与工业 [B: Principle / F: Industry]

```
WG21模板重载决议提案:
N3291 (C++11): SFINAE正式标准化 → enable_if成为合法的重载控制手段
P2593R0 (C++23): explicit object parameter (deducing this) → 简化CRTP重载

工业案例:
- libstdc++: std::enable_if用于vector的构造函数重载 (size_type vs initializer_list)
- Abseil: absl::enable_if_t替代std::enable_if_t (C++14前兼容)
- Eigen: 8层模板重载用于不同矩阵运算的编译期分派
- Boost.Hana: overload_linearly → 按顺序尝试多个lambda

设计权衡: SFINAE vs Concepts vs if constexpr
  SFINAE: 最灵活但错误信息最差 (100行模板实例化错误)
  Concepts: 最清晰但需要C++20 (requires clause)
  if constexpr: 最简单但不能用于重载选择 (只能选择函数体内代码)
```


## 联合使用场景

| 关联章节 | 场景 | 组合方式 |
|---|---|---|
| [第60章](Book/part06_templates/ch60_template_basics.md) | 模板约束/类型安全API | 本章提供概念，第60章提供实现 |
| [第62章](Book/part06_templates/ch62_specialization.md) | STL算法回调/异步任务 | 本章提供概念，第62章提供实现 |
| [第66章](Book/part06_templates/ch66_sfinae.md) | 泛型库/编译期计算 | 本章提供概念，第66章提供实现 |
| [第67章](Book/part06_templates/ch67_concepts.md) | 静态多态/编译期接口 | 本章提供概念，第67章提供实现 |


## 相关章节（交叉引用）

- **同模块接续**：⟶ Book/part06_templates/ch60_template_basics.md（第60章　模板基础与实例化（Template Basics & Instantiation））—— 模板基础定义实例化，重载决议在其上选择候选
- **同模块接续**：⟶ Book/part06_templates/ch62_specialization.md（第62章　类模板特化与偏特化（Class Template Specialization））—— 全特化/偏特化是重载决议的最终落点
- **同模块接续**：⟶ Book/part06_templates/ch66_sfinae.md（第66章　SFINAE 与 std::enable_if —— 替换失败非错误的编译期分发）—— SFINAE 是重载决议中剔除失败候选的核心机制
- **同模块接续**：⟶ Book/part06_templates/ch67_concepts.md（第67章　Concepts 与 requires —— C++20 的编译期约束）—— concepts 以更清晰的约束重写重载决议
- **同模块接续**：⟶ Book/part06_templates/ch64_fold.md（第64章　折叠表达式 Fold Expression（C++17））—— 折叠表达式参与包展开相关的重载
- **跨模块**：⟶ Book/part03_language/ch23_namespace_adl.md（第23章　命名空间（namespace）、using 与参数依赖查找（ADL）：隔离、版本化与隐形查找）—— ADL 在模板重载决议中决定候选函数集合

## 附录 G（工业级模板重载决议实战）

> 下列项目均在生产代码中大规模使用该特性，源码可在其公开仓库核查。

- **Google** — Abseil `absl::Overload` 用重载实现 visitor
- **LLVM** — Clang Sema 实现完整重载决议算法
- **Chromium** — base::Overloaded 提供重载辅助
- **Boost** — Boost.Hana / Boost.CallableTraits 操作重载
- **Qt ** — QOverload 宏消歧信号重载
- **Eigen** — 标签分发用重载选择 kernel
- **folly** — folly::overload 组合多个 callable
- **ClickHouse** — 函数注册用重载匹配参数类型
- **RocksDB** — 迭代器用重载区分键值类型
- **V8** — API 用重载暴露多形态接口
- **DPDK** — 重载封装不同 mbuf 操作
- **gRPC** — 序列化用重载区分消息类型
- **spdlog** — 日志 API 用重载接受多参数
- **fmt** — format 用重载解析参数包
- **Unreal** — UE 模板用重载实现 traits
- **WebKit** — WTF 用重载实现智能指针转换
- **Mozilla** — mfbt 用重载实现元组访问
- **Abseil** — Abseil `absl::visit` 基于重载
- **Blink** — Blink 用重载实现样式计算分派
- **Chromium** — base 用重载实现回调绑定


## 附录 H（模板实例化与符号修饰）

重载决议在实例化期展开，下列为典型代价与底层表示。

```text
; 实例化 foo<int>(x) 调用点
mov edi, 0x0005          ; 实参
call _Z3fooIiEiT_        ; 修饰后符号（mangled）
; 递归模板深度限制检查
cmp rsp, 0x0010          ; 栈余量
jbe .depth_error
```

### 实例化代价

- 每套实参生成一份代码：模板在 0x0008 种实参下二进制膨胀 ≈ 0x0100 KB
- 符号修饰（mangling）长度 ≈ 0x0040 字符；`c++filt` 还原 ≈ 0.1us
- 默认实例化深度上限 `0x0100`（256），超出报 `template instantiation depth`

### 决议时序

- 重载集排序（partial ordering）≈ 0.3us/候选（小集合）
-  SFINAE 失败分支被静默丢弃，不计入生成代码
- `constexpr if` 在 C++17 去虚化选择分支，省 ≈ 3.2ns/调用

### 编译器与标准

- GCC 13.2 / Clang 18 对 `absl::Overload` 完全支持
- `__cplusplus` = 202302L；`_Pragma("once")` 加速头解析
- WG21 提案 P0784R7 扩展 constexpr 模板能力

### 面试要点（速记 · 模板重载决议）

- **重载决议顺序**：非模板 > 模板特化 > 基模板；更特化的模板（partial ordering）优先。函数与模板函数同名时，先尝试普通函数，失败再走模板。
- **SFINAE 本质**：替换失败不是错误，仅将该重载从候选集移除；配合 `std::enable_if` / `void_t` 做编译期 trait 分发。
- **实参推导陷阱**：`vector<int>` 与 `initializer_list` 重载歧义、`T&` vs `T&&` 转发引用优先级；`auto` 参数（C++20 缩写函数模板）不参与偏序。
- **concepts 替代 SFINAE**：`requires` 约束更清晰、编译错误信息更短、实例化更快（C++20）。
- **二阶段查找**：模板定义期只查非依赖名，实例化期查依赖名；ADL 在实例化期对依赖调用生效。

## 自测练习（Exercises）

> 以下题目用于自测掌握程度；答案折叠于每题下方，建议先独立作答。

### 练习 1（难度 ★★）

**重载决议：模板 vs 非模板**

给定：
```cpp
template <class T> T id(T x) { return x; }
int id(int x) { return x + 1; }
```
- 调用 `id(42)` 选择哪个重载？`id(3.14)` 呢？写出规则并验证。

<details>
<summary>参考答案</summary>

非模板 `int id(int)` 对 `int` 实参是**精确匹配**，优先于模板实例化；`id(3.14)` 只能由模板 `T=double` 匹配。

```cpp
#include <iostream>
template <class T> T id(T x) { return x; }
int id(int x) { return x + 1; }
int main() {
    std::cout << id(42)   << "\n";   // 非模板：43
    std::cout << id(3.14) << "\n";   // 模板 T=double：3.14
}
```
[标准] 重载决议中，非模板函数比模板实例化更特化，精确匹配胜出。
</details>

### 练习 2（难度 ★★★）

**重载歧义与消歧**

```cpp
template <class T> void f(T)  { /* 通用 */ }
template <class T> void f(T*) { /* 指针 */ }
```
调用 `f((int*)nullptr)` 是否歧义？给出两种消除歧义的写法（`enable_if` 或标签）。

<details>
<summary>参考答案</summary>

`f((int*)nullptr)` 中 `T=int*` 同时匹配两式（`T*` 版 `T=int`），两模板同等特化 → **歧义**。消歧写法：

写法 A——`enable_if` 把指针版限定为指针类型：
```cpp
#include <type_traits>
template <class T, class = void> void f(T) { /* 通用 */ }
template <class T>
void f(T*, std::enable_if_t<std::is_pointer_v<T>, int> = 0) { /* 指针 */ }
```

写法 B——`std::true_type` 标签分发（见 ch70）：
```cpp
#include <type_traits>
template <class T> void f_impl(T, std::false_type) { /* 通用 */ }
template <class T> void f_impl(T*, std::true_type)  { /* 指针 */ }
template <class T> void f(T v) { f_impl(v, std::is_pointer<T>{}); }
```
</details>

### 练习 3（难度 ★★★★）

**运算符模板与 ADL 冲突**

在全局命名空间定义 `template <class T> bool operator==(const T&, const T&)`，会与标准库大量 `operator==` 经 ADL 冲突（如比较两个 `std::vector`）。给出安全写法。

<details>
<summary>参考答案</summary>

全局运算符模板会经实参依赖查找（ADL）污染所有类型，与 `std` 内 `operator==` 冲突。安全做法：定义为**类内友元**，仅对自定义类型生效：

```cpp
#include <iostream>
struct Point {
    int x, y;
    friend bool operator==(const Point& a, const Point& b) {
        return a.x == b.x && a.y == b.y;
    }
};
int main() {
    Point a{1, 2}, b{1, 2};
    std::cout << std::boolalpha << (a == b) << "\n";   // true
}
```
[标准] 类内友元运算符不污染全局命名空间，避免与标准库 ADL 候选冲突。
</details>


## 附录：用法演绎（从选型到落地）



### 演绎 1：重载决议——模板并非总是优先

**场景**：你写了一个通用 `id` 模板，期望所有整数都走它，却发现 `id(42)` 返回 43 而非 42。

**常见错误**（直觉写法）：
```text
template <class T> T id(T x) { return x; }
int id(int x) { return x; }   // 顺手加的非模板重载
id(42);                       // 期望 42，得到 43
```
非模板 `int id(int)` 对 `int` 是精确匹配，重载决议中非模板优先于模板实例化。

**修复**：明确要哪个——若所有整数统一走模板，删掉非模板重载；若 `int` 需特殊行为，保留并意识到它胜出。

```cpp
#include <iostream>
template <class T> T id(T x) { return x; }
int main() { std::cout << id(42) << "\n"; }   // 42
```

**结论**：重载决议优先级——非模板精确匹配 > 模板实例化 > 转换序列。别假设"模板更通用就更优先"。

### 演绎 2：运算符模板别放全局

**场景**：想给自定义类型加通用 `operator==`，于是在全局写 `template<class T> bool operator==(const T&, const T&)`。

**常见错误**（编译失败 / 无限递归）：
```text
template <class T> bool operator==(const T& a, const T& b) { return a == b; }
std::vector<int> v1, v2;
bool eq = (v1 == v2);   // 与 std::vector 的 operator== 经 ADL 冲突 / 递归
```

**修复**：放进类内作友元（见练习 3 答案），作用域仅限该类型。

```cpp
#include <iostream>
struct Point { int x, y;
    friend bool operator==(const Point& a, const Point& b) {
        return a.x == b.x && a.y == b.y; } };
int main() { Point a{1,2}, b{1,2};
    std::cout << std::boolalpha << (a == b) << "\n"; }
```

**结论**：通用比较逻辑用类内友元或限定命名空间自由函数，绝不在全局铺运算符模板。
