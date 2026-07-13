# 第62章　类模板特化与偏特化（Class Template Specialization）

⟶ Book/part06_templates/ch60_template_basics.md
⟶ Book/part06_templates/ch68_tmp.md

> 模板模式速查：本章属「特化调度型」模板。类模板允许为**特定类型**提供完全不同实现（全特化），或为**一类类型**提供实现（偏特化）。这是 trait、allocator、智能指针的核心机制。

## ① 学习目标

⟶ Book/part06_templates/ch61_template_overload.md
⟶ Book/part06_templates/ch63_variadic.md


- 区分主模板 / 全特化 / 偏特化 [标准]
- 掌握偏序（哪份特化更特化）决定实例化选中谁 [标准]
- 理解全特化是「独立模板」，可改变成员集合 [标准]
- 从 mangled 符号确认特化选择 [平台]
- 避免「多份特化同样特化」导致的二义 [经验]

## ② 本模板模式速查（名称 / 适用场景 / 核心结构 / 定义）

- **模板名称**：类模板特化（全特化 / 偏特化）
- **适用场景**：对 bool/void/指针/引用/容器等特定类型族需要不同存储/行为（如 `std::vector<bool>` 位压缩）
- **核心结构**：`template <> struct C<T>{};` （全） / `template <typename U> struct C<U*>` （偏）
- **一句话定义**：特化为特定（或某类）实参提供「替代主模板」的实现，由偏序选出最特化者 [标准]

```cpp
template <typename T> struct Wrapper { /* 主 */ };
template <>           struct Wrapper<int> { /* 全特化 */ };
template <typename U> struct Wrapper<U*> { /* 偏特化：指针 */ };
```

## ③ 核心结构与完整代码实现

```cpp
// 主模板
template <typename T>
struct Storage {
    T value;
    void describe() const { /* 通用 */ }
};

// 全特化：为 bool 提供位压缩替代（示意）
template <>
struct Storage<bool> {
    unsigned bits;
    void describe() const { /* bool 专用 */ }
};

// 偏特化：指针
template <typename U>
struct Storage<U*> {
    U* ptr;
    void describe() const { /* 指针专用 */ }
};
```

全特化可改成员集合 [标准]：

```cpp
template <typename T> struct S { T v; };
template <> struct S<void> {            // 全特化 void：完全不同类型集
    static constexpr bool is_void = true;
    void nothing() const {}
};
```

## ④ 偏序：哪份特化更特化

```cpp
template <typename T> struct C { static const char* name() { return "primary"; } };
template <typename U> struct C<U*>   { static const char* name() { return "ptr"; } };
template <typename V> struct C<const V> { static const char* name() { return "const"; } };

// C<double>      -> 主（不匹配 ptr/const）
// C<int>         -> ? 见下：全特化需单独写
// C<int*>        -> 偏特化 ptr（U=int）
// C<const double>-> 偏特化 const（V=double）
```

```cpp
// 多份偏特化并存时的偏序
template <typename T> struct D { };
template <typename T> struct D<T*> { };        // D1
template <typename T> struct D<const T*> { };  // D2 比 D1 更特化（const 指针）
// D<const int*> -> D2（更特化）胜
```

## ⑤ 适用场景与选型

| 场景 | 选 |
|---|---|
| 单类型完全不同实现 | 全特化 |
| 一族类型（指针/引用/数组/const） | 偏特化 |
| 按 trait 分派 | 偏特化 + enable_if（ch66）/ requires（ch67） |
| 仅想换成员名 | 全特化（可改成员集） |

## ⑥ 完整可运行示例（最小）

```cpp
#include <iostream>
template <typename T> struct W { static const char* k() { return "primary"; } };
template <> struct W<int> { static const char* k() { return "int"; } };
template <typename U> struct W<U*> { static const char* k() { return "ptr"; } };
int main() {
    std::cout << W<double>::k() << '\n';   // primary
    std::cout << W<int>::k() << '\n';      // int
    std::cout << W<int*>::k() << '\n';     // ptr
}
```

```cpp
// 全特化改成员集
template <typename T> struct Info { static constexpr int tag = 0; };
template <> struct Info<void> { static constexpr int tag = -1; static const char* s() { return "void"; } };
```

```cpp
#include <cstddef>
// 偏特化：数组
template <typename T> struct ArrInfo { static constexpr bool is_arr = false; };
template <typename T, std::size_t N> struct ArrInfo<T[N]> { static constexpr bool is_arr = true; static constexpr std::size_t n = N; };
```

## ⑦ 标准规定 [标准]

- 全特化 `template <> struct C<X>` 是一个**独立模板定义**，不是主模板的「分支」[temp.spec]。
- 偏特化 `template <typename U> struct C<U*>` 仍是模板，需保留参数列表 [temp.class.spec]。
- 实例化选中「最特化」的可用特化；若两份同样特化 → 二义 [temp.class.spec.match]。

## ⑧ GCC / Clang / MSVC 行为差异 [实现][平台]

```cpp
// 三者在偏序与 SFINAE 上基本一致（现代 MSVC 已修复旧版宽松两阶段）
// 差异主要：模板报错可读性（见 ch75）与对 C++20 概念的支持进度
```

```cpp
// MSVC 对「函数模板偏序」曾与类模板偏序处理不一致；用类模板包装规避
template <typename T> struct Dispatcher { static void run(T); };
```

## ⑨ 内存 / 对象模型

每份选中的特化是**独立类型**，各自布局独立。

```cpp
static_assert(sizeof(W<int>)   != sizeof(W<int*>));   // 不同特化是不同类型
static_assert(!std::is_same_v<W<int>, W<int*>>);
```

```cpp
#include <vector>
// std::vector<bool> 偏特化位压缩：sizeof 远小于 N 字节
std::vector<bool> vb(8);   // 通常只占 1 字节（位域）
```

## ⑩ 汇编 / 符号证据（真实 MinGW GCC 13.1.0，-O2 -masm=intel）

编译 `Examples/_asm_tpl_spec.cpp`：为 4 份特化逐一取 `kind()` 地址，强制发射各自 mangled 符号：

```asm
; _asm_tpl_spec.asm 节选（MinGW GCC 13.1.0, -O2）
    .section .rdata,"dr"
.LC0:   .ascii "full-int\0"
    .globl  _ZN7WrapperIiE4kindEv          ; Wrapper<int> 全特化
_ZN7WrapperIiE4kindEv:
    lea rax, .LC0[rip]
    ret
    .globl  _ZN7WrapperIdE4kindEv          ; Wrapper<double> 主模板
_ZN7WrapperIdE4kindEv:
    lea rax, .LC1[rip]                     ; .LC1 = "primary"
    ret
    .globl  _ZN7WrapperIPiE4kindEv         ; Wrapper<int*> 偏特化指针
_ZN7WrapperIPiE4kindEv:
    lea rax, .LC2[rip]                     ; .LC2 = "partial-ptr"
    ret
    .globl  _ZN7WrapperIKdE4kindEv         ; Wrapper<const double> 偏特化 const
_ZN7WrapperIKdE4kindEv:
    lea rax, .LC3[rip]                     ; .LC3 = "partial-const"
    ret
```

**读法**：四个符号各自独立发射，返回值字符串证明选中正确：
- `Wrapper<int>` → `_ZN7WrapperIiE4kindEv`（全特化，返回 `"full-int"`）
- `Wrapper<double>` → `_ZN7WrapperIdE4kindEv`（主模板，返回 `"primary"`）
- `Wrapper<int*>` → `_ZN7WrapperIPiE4kindEv`（偏特化指针，返回 `"partial-ptr"`）
- `Wrapper<const double>` → `_ZN7WrapperIKdE4kindEv`（偏特化 const，返回 `"partial-const"`）

`mangled` 名中 `Ii`=int、`Id`=double、`IPi`=int*`、`IKd`=const double，直接编码了选中哪份特化。

### 知识点深挖（模板B）

**B1 全特化语法与语义 [标准]**（≥10 例）

```cpp
template <typename T> struct A { T v; };
template <> struct A<int> { int v; void f(){} };   // 全特化 int
```

```cpp
template <typename T, typename U> struct B {};
template <> struct B<int, double> {};              // 双参数全特化
```

```cpp
template <typename T> void foo(T);
template <> void foo<int>(int) {};                 // 函数模板全特化
```

```cpp
template <typename T> struct C { static constexpr int x = 0; };
template <> struct C<char> { static constexpr int x = 1; };
```

```cpp
template <typename T> struct D { using type = T; };
template <> struct D<void> { using type = int; };   // 全特化改 type
```

```cpp
template <typename T> struct E { void f(); };
template <> void E<bool>::f() {};                   // 类外定义全特化成员
```

```cpp
// 全特化必须匹配主模板参数数目
template <typename T, typename U> struct F {};
// template <> struct F<int> {};   // 错误：参数数不匹配
```

```cpp
// 全特化可加 constexpr 不同行为
template <typename T> struct G { static constexpr bool small = false; };
template <> struct G<char> { static constexpr bool small = true; };
```

```cpp
// 函数模板全特化不参与重载决议优先级（它等同具体函数）
template <typename T> void h(T);
template <> void h(int) {}   // 等同 void h(int)，非模板优先
```

```cpp
// 变量模板全特化（C++14）
template <typename T> constexpr T eps = T(1e-6);
template <> constexpr float eps<float> = 1e-4f;
```

```cpp
// 成员模板全特化
template <typename T> struct H { template <typename U> void m(U); };
template <> template <typename U> void H<int>::m(U) {}
```

**B2 偏特化模式 [标准]**

```cpp
template <typename T> struct P { };
template <typename T> struct P<T*> { };        // 指针偏特化
```

```cpp
template <typename T> struct Q { };
template <typename T> struct Q<T&> { };         // 左值引用偏特化
```

```cpp
template <typename T> struct R { };
template <typename T> struct R<T&&> { };        // 右值引用偏特化
```

```cpp
#include <cstddef>
template <typename T> struct S { };
template <typename T, std::size_t N> struct S<T[N]> { };  // 数组偏特化
```

```cpp
template <typename T> struct V { };
template <typename T> struct V<const T> { };     // const 偏特化
```

```cpp
template <typename T> struct W { };
template <typename T> struct W<volatile T> { };  // volatile 偏特化
```

```cpp
template <typename T> struct X { };
template <template <typename> class C, typename T> struct X<C<T>> { };  // 模板模板偏特化
```

```cpp
#include <vector>
template <typename T> struct Y { };
template <typename T> struct Y<std::vector<T>> { };  // 具体模板实例偏特化
```

```cpp
template <typename T> struct Z { };
template <typename T> struct Z<T(*)()> { };       // 函数指针偏特化
```

```cpp
#include <functional>
template <typename T> struct M { };
template <typename T> struct M<std::function<T()>> { };  // std::function 偏特化
```

**B3 偏序推导 [标准]**

```cpp
template <typename T> struct A { };
template <typename T> struct A<T*> { };
template <typename T> struct A<const T*> { };
// A<const int*> -> const T* 比 T* 更特化 → 选中
```

```cpp
template <typename T> struct B { };
template <typename T> struct B<T*> { };
template <typename T> struct B<T* const> { };
// B<int* const> -> T* const 更特化
```

```cpp
#include <vector>
template <typename T> struct C { };
template <typename T> struct C<std::vector<T>> { };
template <typename T> struct C<std::vector<T>*> { };  // 指针版更特化
```

```cpp
template <typename T> struct D { };
template <typename T> struct D<T&> { };
template <typename T> struct D<const T&> { };   // const T& 更特化？注意引用折叠
```

**B4 trait 中的特化 [标准]**

```cpp
template <typename T> struct is_pointer : std::false_type {};
template <typename T> struct is_pointer<T*> : std::true_type {};
```

```cpp
template <typename T> struct is_const : std::false_type {};
template <typename T> struct is_const<const T> : std::true_type {};
```

```cpp
#include <cstddef>
template <typename T> struct is_array : std::false_type {};
template <typename T, std::size_t N> struct is_array<T[N]> : std::true_type {};
```

```cpp
template <typename T> struct remove_const { using type = T; };
template <typename T> struct remove_const<const T> { using type = T; };
```

```cpp
#include <cstddef>
template <typename T> struct rank { static constexpr std::size_t value = 0; };
template <typename T, std::size_t N> struct rank<T[N]> { static constexpr std::size_t value = 1 + rank<T>::value; };
```

**B5 二义与错误对照 [经验]**

```cpp
// 二义：两份偏特化同样特化
template <typename T> struct A { };
template <typename T> struct A<T*> { };
template <typename T> struct A<const T*> { };
// A<const int*> OK（const T* 更特化）；
// 若再加 template <typename T> struct A<T* const> 与 A<const T*> 同等级 → 二义
```

```cpp
// 错误：偏特化参数必须从主模板「可推导」
template <typename T> struct B { };
// template <typename T> struct B<T*> { };   // OK
// template <typename T> struct B<int> { };   // 错：偏特化不能写死非参数，那是全特化写法但形式不对
```

```cpp
// 错误：主模板未声明就特化
// template <> struct C<int> {};   // 必须先有 template <typename T> struct C {}
```

```cpp
// 正确：先主后特
template <typename T> struct D { };
template <> struct D<void> { };
```

```cpp
// 错误：函数模板偏特化非法
// template <typename T> void f<T*>(T*) {}   // 非法；用重载或类模板包装
```

## ⑪ STL 中的该模式

```cpp
#include <vector>
// std::vector<bool> 偏特化：位压缩，与普通 vector 布局完全不同
```

```cpp
// std::is_pointer / std::is_array / std::is_const 全靠偏特化实现（见 ch65）
```

```cpp
#include <cstddef>
#include <string>
// std::hash 对每种类型全特化
template <> struct std::hash<std::string> { std::size_t operator()(const std::string&) const; };
```

```cpp
// std::allocator_traits 偏特化处理不同 allocator
```

```cpp
// std::tuple_element 偏特化按索引取类型
```

## ⑫ 变体（variant patterns）

```cpp
#include <type_traits>
#include <concepts>
// 用偏特化实现「按类别分流」的 dispatch
template <typename T> struct Handler { static void run() { /* 通用 */ } };
template <typename T> struct Handler<T*> { static void run() { /* 指针 */ } };
// SFINAE 偏特化（ch66）：用 enable_if 选特化
template <typename T, typename = void> struct HasFoo : std::false_type {};
template <typename T> struct HasFoo<T, std::void_t<decltype(std::declval<T>().foo())>> : std::true_type {};
// Concepts 偏特化（ch67）
template <typename T> struct Proc { };
template <std::integral T> struct Proc<T> { };
// 递归偏特化（typelist）
template <typename... Ts> struct TypeList;
template <typename Head, typename... Tail> struct TypeList<Head, Tail...> { using first = Head; using rest = TypeList<Tail...>; };
// 空基类 EBO 与特化结合（见 ch52 占位）
template <typename T> struct Wrapper : private T { };

int main() {
    return 0;
}
```

## ⑬ 反模式（anti-patterns）

```cpp
// 反模式1：特化顺序导致意外二义
template <typename T> struct A { };
template <typename T> struct A<T*> { };
template <typename T> struct A<const T*> { };
// 看似 OK，但若需求演变为 A<const T> 与 A<const T*> 同等级会二义
```

```cpp
#include <vector>
// 反模式2：在命名空间 std 里特化非用户定义的模板（仅允许对用户类型特化 std 模板）
// template <> struct std::less<MyType> {};  // OK（用户类型）
// template <> struct std::vector<int> {};   // 错误：不能特化标准模板
```

```cpp
// 反模式3：偏特化写死类型当全特化用，导致永远命中
template <typename T> struct B<T*> { };   // 若想只针对 int*，应写全特化 B<int*>
```

```cpp
// 反模式4：函数模板想偏特化 → 用类模板包装
```

```cpp
// 反模式5：特化改变接口契约，调用方依赖主模板成员名 → 运行期/编译期错配
```

## ⑭ 工业案例

```cpp
// 案例：type traits 库（Boost.TypeTraits / std）全靠偏特化萃取类型属性
template <typename T> struct is_integral : std::false_type {};
template <> struct is_integral<int> : std::true_type {};
template <> struct is_integral<long> : std::true_type {};
```

```cpp
#include <vector>
// 案例：序列化框架按类型特化
template <typename T> struct Codec { static void write(Output&, const T&); };
template <> struct Codec<int> { static void write(Output&, int); };  // 定长快路径
template <typename T> struct Codec<std::vector<T>> { static void write(Output&, const std::vector<T>&); };
```

```cpp
// 案例：Eigen 对固定尺寸/动态尺寸矩阵用不同存储特化
template <typename Scalar, int Rows, int Cols> class Matrix;   // 固定
template <typename Scalar> class Matrix<Scalar, Eigen::Dynamic, Eigen::Dynamic>;  // 动态
```

## ⑮ 源码剖析（libstdc++ 相关）

```cpp
// libstdc++ std::is_pointer（简化）
template <typename> struct is_pointer : false_type {};
template <typename _Tp> struct is_pointer<_Tp*> : true_type {};
```

```cpp
#include <vector>
// std::vector<bool> 偏特化：_Bit_type 位数组，operator[] 返回代理引用
// bits/stl_bvector.h 中 vector<bool> 是独立实现，并非 vector 的子类
```

```cpp
// GCC pt.cc do_class_deduction / partial_inst：偏序比较
```

## ⑯ 易错点

```cpp
// 1) 偏特化必须从主模板推导参数，不能写死（写死应全特化）
```

```cpp
// 2) 函数模板不能偏特化，用重载或类模板包装
```

```cpp
// 3) 全特化是独立模板，可改成员集，但与主模板「同名不同类型」
```

```cpp
// 4) 多份偏特化同样特化 → 二义
```

```cpp
// 5) 在命名空间 std 只能为用户类型特化标准模板
```

```cpp
// 6) 特化需可见（通常放头文件），否则 ODR 违规
```

## ⑰ FAQ

```cpp
// Q：全特化与偏特化区别？
// A：全特化实参完全固定（一份具体类型）；偏特化仍留参数给一类类型。
```

```cpp
// Q：为什么不能直接偏特化函数模板？
// A：标准未提供；用重载（决议能选更特化）或类模板静态成员替代。
```

```cpp
// Q：偏序怎么比？
// A：用一份特化的形参去推导另一份，能单向推导者更特化。
```

```cpp
#include <vector>
// Q：std::vector<bool> 为什么奇怪？
// A：它是主模板的偏特化，用位压缩，operator[] 返回代理而非 bool&。
```

```cpp
// Q：特化能改成员吗？
// A：全特化可以；偏特化也可以（它仍是独立定义）。但接口契约应保持一致。
```

## ⑱ 最佳实践

```cpp
// 1) trait 用偏特化萃取，全特化铺叶子类型（int/long/...）
```

```cpp
// 2) 需要「改成员集」用全特化；只是「换实现」用偏特化
```

```cpp
// 3) 避免二义：偏特化层次保持严格更特化关系
```

```cpp
// 4) 命名空间 std 仅特化用户类型；其余放进自己命名空间
```

```cpp
// 5) 用 Concepts（ch67）替代 enable_if 偏特化，可读性更好
```

## ⑲ 性能（编译期 / 运行期）

```cpp
#include <vector>
// 特化选择纯编译期；选中后类型独立，零运行期分支
// std::vector<bool> 偏特化以空间换时间（位压缩省内存，访问多一次位运算）
```

```cpp
// 实例化成本：每份特化 = 一份类型定义；收敛方式同 ch60（extern template 不适用全特化但适用主模板）
```

```cpp
// trait 偏特化多在编译期 ::value 求值，无运行期开销
```

## ⑳ 练习题 + 思考题 + 源码阅读路线（内化，无独立推荐阅读节）

**练习题**

1. 写 `is_reference` trait：主模板 false，偏特化 `T&` 与 `T&&` 为 true。
2. 写 `remove_reference`：去掉一层引用。
3. 为 `Matrix<T, Rows, Cols>` 写一个「行优先」偏特化与一个「列优先」偏特化（用标签区分）。
4. 预测 `A<const int*>`、`A<int* const>`、`A<const int* const>` 在 `A<T>/A<T*>/A<const T*>` 下的选中。
5. 用类模板包装实现函数模板的「偏特化」效果。

**思考题**

- 全特化「改成员集」会破坏什么设计契约？何时该允许？
- 为什么 `std::vector<bool>` 的偏特化被视为「设计错误」？它在哪些场景真省内存？
- 偏序与函数模板重载偏序（ch61）是同一套规则吗？

**源码阅读路线（内化）**

- libstdc++ `bits/type_traits.h`：is_pointer/is_array/is_const 偏特化
- libstdc++ `bits/stl_bvector.h`：vector<bool> 偏特化
- GCC `cp/pt.cc`：类模板偏特化偏序比较
- 交叉引用占位：part06 ch65（type traits）、ch66（SFINAE）、ch67（Concepts）


## 联合使用场景

| 关联章节 | 场景 | 组合方式 |
|---|---|---|
| [第61章](Book/part06_templates/ch61_template_overload.md) | 泛型库/编译期计算 | 本章提供概念，第61章提供实现 |
| [第63章](Book/part06_templates/ch63_variadic.md) | 内存管理/PMR定制 | 本章提供概念，第63章提供实现 |
| [第60章](Book/part06_templates/ch60_template_basics.md) | 文本处理/协议解析 | 本章提供概念，第60章提供实现 |
| [第68章](Book/part06_templates/ch68_tmp.md) | 模板约束/类型安全API | 本章提供概念，第68章提供实现 |

## 附录 E：模板特化工业

libstdc++特化: vector<bool>位压缩(1bit/bool); hash<string>→FNV-1a; char_traits→memcmp
Eigen特化: Matrix<float,4,4>完全特化→4条mulps; Dynamic列向量偏特化

```cpp
#include <iostream>
#include <vector>
int main(){std::vector<bool> v{true,false,true};std::cout<<v[0]<<std::endl;return 0;}
```

| 特化 | 目的 | 注意 |
|---|---|---|
| vector<bool> | 位压缩 | 非容器, &v[0]不工作 |
| Matrix<float,4,4> | SIMD | 4条指令vs16条 |

面试: vector<bool>位压缩导致reference是代理(非bool&); 全特化vs偏特化=参数固定vs部分固定

## 附录 F：特化工业案例

```cpp
#include <iostream>
#include <vector>
int main(){std::vector<bool> v{true,false};std::cout<<v[0]<<std::endl;std::cout<<"Partial spec=fix some params; full spec=fix all params"<<std::endl;return 0;}
```

| 特化 | 库 | 效果 |
|---|---|---|
| vector<bool> | libstdc++/libc++ | 位压缩(1bit/bool存8x) |
| hash<string> | 所有STL | FNV-1a算法(优于默认hash) |
| char_traits<char> | 所有STL | memcmp替代逐字节比较 |

面试: 偏特化vs全特化? 偏特化=部分参数固定(T*); 全特化=全部固定(int)
       vector<bool>为什么不是容器? 位压缩导致reference是代理, &v[0]返回中间类型

## 附录 G：模板特化的编译器实现

### GCC/libstdc++特化机制

```asm
; 全特化: template<> struct Trait<int> { ... };
; 编译器直接生成特化版本的代码——不与主模板共享代码
; → 每个特化都是独立的TU实例化

; 偏特化: template<typename T> struct Trait<T*> { ... };
; 编译器在实例化时先匹配偏特化, 未匹配才fallback到主模板
; → 匹配顺序: 全特化 > 偏特化 > 主模板
```

### 面试巩固

Q: 全特化vs偏特化的成员可以不同吗? A: 可以。全特化可以完全重新定义类(不同成员), 偏特化受限

Q: 为什么vector<bool>是"不完整"的容器? A: 特化后成员bit_reference替代bool&, 破坏STL容器契约

Q: 函数模板可以偏特化吗? A: 不可以(语言限制)。用重载替代偏特化, 或类模板偏特化+成员函数

```cpp
#include <iostream>
#include <type_traits>
template<typename T> struct is_pointer: std::false_type {};          // primary
template<typename T> struct is_pointer<T*>: std::true_type {};       // partial spec
int main() { std::cout << is_pointer<int*>::value << is_pointer<int>::value << std::endl; return 0; }
```


## 附录 H：特化面试

```cpp
#include <iostream>
template<typename T> struct Traits{static const char* name(){return"T";}};
template<> struct Traits<int>{static const char* name(){return"int";}};  // full spec
int main(){std::cout<<Traits<int>::name()<<std::endl;return 0;}
```

| 特化 | 语法 | 例子 |
|---|---|---|
| 全特化 | template<> struct X<int>{} | vector<bool> |
| 偏特化 | template<T> struct X<T*>{} | 指针版本 |

面试: 函数模板偏特化? 不可(语言限制), 用重载替代; vector<bool>=位压缩特化

## 真实开源项目参考（可查证链接）

> 本节补可查证的真实项目引用（非虚构），与上方「工业案例」的定性叙述互补。

- **Boost（boost.org / github.com/boostorg）**：`Boost.TypeTraits` 与 `Boost.MPL` 大量使用模板特化实现编译期分派；`std::hash` 的自定义特化是工业中定制键值哈希的标准做法（如 `Boost.Hash` 的 `extend_hash`）。
- **Abseil（github.com/abseil/abseil-cpp）**：`absl::Hash` 通过特化其 traits 支持用户类型，是 `std::hash` 的高性能替代。

**常见陷阱 / 最佳实践**：
- 特化 `std::hash<T>` 必须把特化写在**命名空间 `std` 内**（或 ADL 能找到的关联命名空间），否则不生效且无报错。
- 偏特化顺序错误会导致 `ambiguous` 或落到主模板；用 `if constexpr` / concepts 往往比层层偏特化更可读。

> 交叉引用：特化与 `type_traits` 联动见 [ch65](Book/part06_templates/ch65_type_traits.md)；与 SFINAE 选拔见 [ch66](Book/part06_templates/ch66_sfinae.md)。

## 附录 I：模板特化工业实践 [F: Industry / B: Principle]

特化是泛型库把"通用算法"换成"最优实现"的核心手段：

- **Eigen**：`Eigen::NumTraits<T>` 全特化给标量类型定 `epsilon()`/`dummy_precision()`；`internal::scalar_product_traits` 特化决定是否走 SIMD。
- **Boost**：`boost::type_traits`（`is_integral`/`is_pointer`）通过偏特化萃型；`boost::multiprecision` 对 `cpp_int` 全特化 `numeric_limits`。
- **Abseil**：`absl::StrFormat` 用特化选 `FormatValue` 的编码路径；`absl::hash` 对 `std::string`/容器特化。
- **LLVM**：`llvm::DenseMapInfo<T>` 特化提供哈希/相等/空哨兵，是 LLVM 容器的关键定制点。

模式：默认模板定义算法骨架，全/偏特化替换热点分支——比运行时 `if` 早到编译期，零开销。C++17 的 `if constexpr` 与 C++20 concepts 逐步把"特化地狱"收敛为 `requires` 约束。

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

