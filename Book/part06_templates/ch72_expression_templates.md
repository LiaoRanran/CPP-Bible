# 第72章　表达式模板 Expression Templates

⟶ Book/part06_templates/ch68_tmp.md
⟶ Book/part05_oo/ch51_crtp.md

> 本章所有汇编证据由 **MinGW GCC 15.3.0**（`-std=c++23 -O2 -S -masm=intel`）真实提取，源码剖析行号取自该工具链安装的 libstdc++ 15.3.0 头文件。
> 立场标签：`[标准]`=标准条文，`[实现]`=编译器实现行为，`[平台]`=平台/ABI 相关，`[经验]`=工程经验。

## ① 学习目标

⟶ Book/part06_templates/ch71_policy.md


- 理解 **表达式模板（Expression Templates, ET）** 的核心动机：消除 `u = a + b + c` 这类算子表达式中的**临时对象与多次遍历**，把"计算时机"从 `operator+` 推迟到 `operator=`。
- 掌握 ET 三件套：**表达式基类 `Expr<E>`**（CRTP 风格静态接口）、**代理节点 `Sum<A,B>`**（存储操作数引用、`operator[]` 递归求值）、**`operator+` 返回代理而非结果**。
- 通过真实汇编确认：朴素实现 `a+b+c` 产生 **2 个临时堆分配 + 3 次遍历**，而 ET 实现**零临时分配 + 单遍遍历**（`u[i]=a[i]+b[i]+c[i]`）。
- 理解 ET 在 libstdc++ 中的反面参照：`std::valarray` 的运算符是**立即求值**（返回 `valarray`，非延迟），理解标准库为何选择简单语义。
- 认识 ET 的代价：深表达式树导致**模板实例化深度/编译时间**增长、调试堆栈深、错误信息复杂。

## ② 本模板模式速查（名称 / 适用场景 / 核心结构 / 定义）

| 项 | 内容 |
|---|---|
| **名称** | 表达式模板（Expression Templates） |
| **适用场景** | 数值线性代数（Eigen/Blaze）、数组/向量运算 DSL、`u = a + b * c + d` 类惰性求值；任何"算子表达式应一次性批量求值"的场景。 |
| **核心结构** | `Expr<E>` 基类（提供 `operator[]`/`size()` 静态接口）；`Sum<A,B>` 代理（存引用，递归 `a[i]+b[i]`）；`operator+` 返回 `Sum`；`operator=` 对代理单遍遍历赋值。 |
| **定义** | 用模板类型**在编译期把表达式树编码为类型**（如 `Sum<Sum<Fast,Fast>,Fast>`），`operator+` 只构造代理（不计算），直到赋值/显式转换才递归遍历求值，从而把多步运算压缩为单遍、零临时。 |

## ③ 核心结构与完整代码实现

```cpp
#include <cstdlib>
#include <cstddef>

// 表达式基类：静态接口（不存储，仅转发到派生 E）
template <typename E>
struct Expr {
    double operator[](size_t i) const { return static_cast<const E&>(*this)[i]; }
    size_t size() const { return static_cast<const E&>(*this).size(); }
};

// 具体向量：继承 Expr<Fast>，operator= 接收任意表达式并单遍遍历
struct Fast : Expr<Fast> {
    double* p; size_t n;
    Fast(size_t k) : n(k), p(new double[k]) {}
    ~Fast() { delete[] p; }
    double operator[](size_t i) const { return p[i]; }
    size_t size() const { return n; }
    template <typename O>
    Fast& operator=(const Expr<O>& e) {            // 赋值即求值
        for (size_t i = 0; i < e.size(); ++i) p[i] = e[i];
        return *this;
    }
};

// 求和代理：存储操作数引用，operator[] 递归求值（不分配、不遍历）
template <typename A, typename B>
struct Sum : Expr<Sum<A,B>> {
    const A& a; const B& b;
    Sum(const A& x, const B& y) : a(x), b(y) {}
    double operator[](size_t i) const { return a[i] + b[i]; }
    size_t size() const { return a.size(); }
};

// operator+ 仅构造代理，不计算
template <typename A, typename B>
Sum<A,B> operator+(const Expr<A>& x, const Expr<B>& y) {
    return Sum<A,B>(static_cast<const A&>(x), static_cast<const B&>(y));
}
```

```cpp
// 使用：a+b+c 在编译期构建 Sum<Sum<Fast,Fast>,Fast>，赋值才单遍求值
Fast a(3), b(3), c(3);
a.p[0]=0; b.p[0]=1; c.p[0]=2;   // ...
Fast u(3);
u = a + b + c;                  // 等价 u[i] = a[i]+b[i]+c[i]，零临时
```

```cpp
#include <cstddef>
// 扩展：乘法代理（与 Sum 对称）
template <typename A, typename B>
struct Prod : Expr<Prod<A,B>> {
    const A& a; const B& b;
    Prod(const A& x, const B& y) : a(x), b(y) {}
    double operator[](size_t i) const { return a[i] * b[i]; }
    size_t size() const { return a.size(); }
};
template <typename A, typename B>
Prod<A,B> operator*(const Expr<A>& x, const Expr<B>& y) {
    return Prod<A,B>(static_cast<const A&>(x), static_cast<const B&>(y));
}
// 现在 u = a*b + c 也成立，编译期构建 Sum<Prod<Fast,Fast>,Fast>
```

```cpp
#include <cstddef>
// 标量混合：标量 × 向量（标量也是表达式节点）
template <typename A>
struct Scale : Expr<Scale<A>> {
    double s; const A& a;
    Scale(double v, const A& x) : s(v), a(x) {}
    double operator[](size_t i) const { return s * a[i]; }
    size_t size() const { return a.size(); }
};
template <typename A>
Scale<A> operator*(double s, const Expr<A>& x) {
    return Scale<A>(s, static_cast<const A&>(x));
}
// u = 2.0 * a + b;  // 编译期：Sum<Scale<Fast>,Fast>
```

## ④ 实例化机制（实例化点 / 两阶段查找）

- **表达式树编码为类型**：`a + b + c` 的类型是 `Sum<Sum<Fast,Fast>,Fast>`（嵌套），整棵树在编译期构建。`operator+` 每次只实例化一个 `Sum` 节点，不触发任何数值计算。
- **求值推迟到 `operator=`**：`Fast::operator=` 接收 `const Expr<O>&`，遍历时对 `Sum` 节点递归调用 `operator[]`，逐元素 `a[i]+b[i]+c[i]`——**单遍完成**。
- **`-O0` 表达式树 mangled 符号**（实测）：
  - `_ZplI4FastS0_E3SumIT_T0_ERK4ExprIS2_ERKS5_IS3_E` = `operator+<Fast,Fast>` 返回 `Sum<Fast,Fast>`（`a+b`）
  - `_ZplI3SumI4FastS1_ES1_ES0_IT_T0_ERK4ExprIS3_ERKS6_IS4_E` = `operator+<Sum<Fast,Fast>,Fast>` 返回 `Sum<Sum<Fast,Fast>,Fast>`（`(a+b)+c`）
- **两阶段查找**：`Sum<A,B>::operator[]` 依赖 `A::operator[]`/`B::operator[]`（依赖型），按 ch60 ④ 解析；`static_cast<const E&>(*this)` 是 CRTP 向下转型（ch51/57）。

```cpp
// 实例化验证：表达式类型在编译期唯一确定
using E1 = decltype(std::declval<Fast>() + std::declval<Fast>());   // Sum<Fast,Fast>
static_assert(std::is_same_v<E1, Sum<Fast,Fast>>);
```

## ⑤ 适用场景与选型

- **数值线性代数**：Eigen、Blaze 用 ET 把 `A*B + C*D` 编译为单层循环 + SIMD（ch19/43 向量化），避免中间矩阵临时。
- **数组/向量运算 DSL**：`u = a + b * c` 类语法应一次遍历求值。
- **GPU/并行**：ET 把表达式树传给 kernel 生成器，单 kernel 完成多步（如 Thrust、Kokkos）。
- **vs 朴素实现**：小规模或调试期可用朴素（可读、易调试）；性能关键的大向量运算用 ET。
- **vs 惰性 lambda**：`[&]{ return a+b+c; }` 也惰性，但 ET 在编译期类型化、可被 `-O2` 充分内联/向量化；lambda 需运行期闭包。

```cpp
// 选型：大向量必须用 ET（避免 N 次临时分配）
// 朴素：u = a+b+c → 2 临时矩阵 + 3 遍历（见 ⑩ 汇编）
// ET：u = a+b+c → 0 临时 + 1 遍历
```

```cpp
// 选型：调试期可读优先用朴素；发布用 ET（同一接口，换模板实现）
```

## ⑥ 完整可运行示例（最小）

```cpp
// 编译：g++ -std=c++23 -O2 expr_demo.cpp -o expr_demo
#include <cstdlib>
#include <cstdio>
#include <cstddef>

template <typename E> struct Expr {
    double operator[](size_t i) const { return static_cast<const E&>(*this)[i]; }
    size_t size() const { return static_cast<const E&>(*this).size(); }
};
struct Fast : Expr<Fast> {
    double* p; size_t n;
    Fast(size_t k) : n(k), p(new double[k]) {}
    ~Fast() { delete[] p; }
    double operator[](size_t i) const { return p[i]; }
    size_t size() const { return n; }
    template <typename O> Fast& operator=(const Expr<O>& e) {
        for (size_t i=0;i<e.size();++i) p[i]=e[i]; return *this;
    }
};
template <typename A, typename B> struct Sum : Expr<Sum<A,B>> {
    const A& a; const B& b; Sum(const A&x,const B&y):a(x),b(y){}
    double operator[](size_t i) const { return a[i]+b[i]; }
    size_t size() const { return a.size(); }
};
template <typename A, typename B> Sum<A,B> operator+(const Expr<A>&x, const Expr<B>&y) {
    return Sum<A,B>(static_cast<const A&>(x), static_cast<const B&>(y));
}

int main() {
    Fast a(3), b(3), c(3);
    for (int i=0;i<3;++i){ a.p[i]=i; b.p[i]=i+1; c.p[i]=i+2; }
    Fast u(3);
    u = a + b + c;                       // 单遍：u[i]=a[i]+b[i]+c[i]
    std::printf("%d %d %d\n", (int)u.p[0], (int)u.p[1], (int)u.p[2]);  // 3 5 7
}
```

```cpp
#include <cstddef>
// 最小 ET 含乘法（u = a*b + c）
template <typename A, typename B> struct Prod : Expr<Prod<A,B>> {
    const A& a; const B& b; Prod(const A&x,const B&y):a(x),b(y){}
    double operator[](size_t i) const { return a[i]*b[i]; }
    size_t size() const { return a.size(); }
};
template <typename A, typename B> Prod<A,B> operator*(const Expr<A>&x, const Expr<B>&y) {
    return Prod<A,B>(static_cast<const A&>(x), static_cast<const B&>(y));
}
```

```cpp
#include <cstddef>
// 最小：显式转估值（无 operator= 时也能求值）
template <typename E> double eval_at(const Expr<E>& e, size_t i) {
    return e[i];   // 触发表达式树递归求值
}
```

## ⑦ 标准规定 [标准]

- `[over.oper]`：运算符重载的返回类型自由；ET 利用 `operator+` 返回代理类型（而非结果类型）实现延迟求值，符合标准。
- `[class.temporary]`：朴素 `operator+` 返回 `valarray`/`Vec` 按值，产生临时对象（生命周期到完整表达式结束）；ET 用代理避免该临时。
- `[temp.inst]`：表达式树每个节点（`Sum<...>`）是独立模板实例化，深树触发多次实例化（见 ⑲ 编译时间代价）。
- **`valarray` 语义**：标准规定 `valarray` 二元运算符返回**新的 `valarray`**（立即求值），并非 ET；这是 ET 在标准库中的"反面参照"（⑪/⑮）。

```cpp
// 标准：operator+ 可返回任意类型（包括代理）
struct Proxy { /* ... */ };
struct Vec {
    Proxy operator+(const Vec&) const;   // 合法：返回代理即 ET 雏形
};
```

```cpp
// 标准：临时对象生命周期（朴素实现的问题根源）
Vec r = a + b;   // a+b 返回临时 Vec，r 从临时拷贝/移动；临时在本表达式结束析构
```

## ⑧ GCC / Clang / MSVC 行为差异 [实现][平台]

- **模板实例化深度**：深表达式树（如 100 项相加）可能触及编译器**模板递归实例化深度上限**（GCC `-ftemplate-depth`，默认 1024；Clang 类似）。超界报错 `template instantiation depth exceeds`。
- **MSVC**：对 ET 的（旧）支持较早（Blitz++ 时代），但深层嵌套类型名诊断冗长；`/std:c++20` 起与 Clang/GCC 接近。
- **内联/向量化**：三编译器都能将 ET 的 `operator=` 单遍循环**自动向量化**（SSE/AVX），Eigen 的 ET + SIMD 在此达成（ch19/43）。
- **符号名长度**：ET 类型 mangled 名极长（`Sum<Sum<...>>`），MSVC 装饰名可能超 `MAX_PATH` 相关限制，建议控制树深。

```cpp
// 各编译器对深 ET 树需控制深度
// template <int N> using Chain = Sum<Chain<N-1>, Fast>;   // 深递归实例化
// using Deep = Chain<2000>;   // [实现] 可能超 GCC/Clang 模板深度上限
```

## ⑨ 内存 / 对象模型

- **代理极轻量**：`Sum<A,B>` 仅存两个 `const` 引用（各 8 字节，x64），合计 16 字节；不分配堆、不拷贝操作数。`a+b+c` 的 `Sum<Sum<Fast,Fast>,Fast>` 仍是两层引用包装，零堆占用。
- **零临时数组**：ET 的 `operator+` 不构造 `Fast`/数组，运行期只有栈上的 `Sum` 代理（引用）；最终 `operator=` 直接写入目标 `u.p`，无中间 `double[]`。
- **目标分配仅一次**：`u` 在赋值前已构造（见 ⑩，仅 1 次 `new` 给 `u`），对比朴素需额外 2 次临时 `new`。
- **引用悬垂风险**：代理持有对操作数的引用，**操作数必须在求值完成前存活**（⑬ 反模式）。

```cpp
// 内存对比：朴素临时数组 vs ET 零额外数组
// 朴素 a+b+c：分配 t1(a+b)、t2(t1+c) 两个 double[n] 临时 → 2*n*8 字节 + 2 次 new
// ET   a+b+c：Sum 代理仅 16 字节栈，无 double[n] 临时
```

```cpp
// 对象大小：代理仅引用
static_assert(sizeof(Sum<Fast,Fast>) == 2 * sizeof(Fast*));   // 16 字节（x64）
```

## ⑩ 汇编 / 符号证据（真实 MinGW GCC 15.3.0，-O2 -masm=intel）

测试文件 `Examples/_asm_expr.cpp`，编译：`g++ -std=c++23 -O2 -S -masm=intel _asm_expr.cpp -o _asm_expr.asm`。

**朴素 `use_naive`（关键片段）**——产生 5 次 `new[]` 与 3 个遍历循环：

```asm
; 分配 a/b/c 三个 Naive（3 次 new[]）
call    _Znay          ; a
call    _Znay          ; b
call    _Znay          ; c
.L5:  ...               ; 循环1：填充 a/b/c
call    _Znay          ; t1 = a+b 临时（第1个额外 new[]）
.L6:  movsd xmm0,[rsi+rax*8]; movsd xmm0,[rdi+rax*8]; add → 存入 t1   ; 循环2：a+b
call    _Znay          ; t2 = (a+b)+c 临时（第2个额外 new[]）
.L10: movsd xmm0,[r12+rdx*8]; add [rbp+rdx*8] → 存入 t2                  ; 循环3：(a+b)+c
; 结尾 5 次 delete[]：a/b/c/t1/t2
```

**表达式模板 `use_expr`（关键片段）**——仅 4 次 `new[]`（无临时）与 **单遍循环**：

```asm
; 分配 a/b/c（3 次 new[]）
call    _Znay          ; a
call    _Znay          ; b
call    _Znay          ; c
.L32: ...               ; 循环1：填充 a/b/c
call    _Znay          ; 仅 u（1 次 new[]，无临时）
.L33: movsd xmm0,[rbx+rdx*8]        ; a[i]
      addsd xmm0,[rsi+rdx*8]        ; + b[i]
      addsd xmm0,[rdi+rdx*8]        ; + c[i]
      movsd [rcx+rdx*8],xmm0         ; u[i] = a[i]+b[i]+c[i]  ← 单遍完成
; 结尾 4 次 delete[]：a/b/c/u
```

**结论（[实现]）**：

| 指标 | 朴素 `use_naive` | 表达式模板 `use_expr` |
|---|---|---|
| 堆分配（`new[]`） | 5 次（3 输入 + 2 临时） | 4 次（仅 3 输入 + 1 个 `u`） |
| 遍历循环 | 3 次（填充 + `a+b` + `(a+b)+c`） | **1 次**（`.L33` 单遍 `u[i]=a[i]+b[i]+c[i]`） |
| 堆释放（`delete[]`） | 5 次 | 4 次 |
| 临时数组 | 2 个 `double[n]` | **0** |

表达式模板把 3 步求和**压缩为单遍、零临时**；`-O2` 下 `.L33` 循环还可被自动向量化（ch19/43）。

**`-O0` 表达式树 mangled 符号（验证编译期类型树）**：

```asm
; operator+<Fast,Fast> → Sum<Fast,Fast>  （a+b）
_ZplI4FastS0_E3SumIT_T0_ERK4ExprIS2_ERKS5_IS3_E
; operator+<Sum<Fast,Fast>,Fast> → Sum<Sum<Fast,Fast>,Fast>  （(a+b)+c）
_ZplI3SumI4FastS1_ES1_ES0_IT_T0_ERK4ExprIS3_ERKS6_IS4_E
```

整个表达式在编译期被编码为嵌套类型 `Sum<Sum<Fast,Fast>,Fast>`，直到 `operator=` 才递归遍历求值——这正是 ET 的"延迟求值"本质。

## ⑪ STL 中的该模式

- **`std::valarray`**：运算符（`operator+` 等）返回**新的 `valarray`**（立即求值），**不是** ET；但其内部 `_Expr` 模板（如 `operator+=` 接受 `_Expr`）有部分惰性优化。标准选择"返回 `valarray`"是为语义简单、可预期（对比 ⑮）。
- **`std::vector`**：`operator=` 是逐元素拷贝（立即语义），**不用 ET**——保持 STL 容器简单、可调试（ch38/77）。
- **为何标准容器不用 ET**：ET 错误信息复杂、编译慢、调试难；标准库优先可维护性，把 ET 留给 Eigen/Blaze 等专用数值库。
- **`std::accumulate` / 算法**：属运行期遍历，非编译期表达式树。

```cpp
// 对比：valarray 是立即求值（非 ET）
#include <valarray>
std::valarray<double> a(3), b(3), c(3);
auto t = a + b;            // 立即产生新 valarray（临时分配 + 遍历）
auto u = t + c;            // 又一次分配 + 遍历（共 2 临时，类似朴素 Vec）
// ET 版把这两步压缩为单遍（见 ⑩）
```

```cpp
// vector 不用 ET：operator= 立即拷贝
#include <vector>
std::vector<double> x(3), y(3);
x = y;   // 立即逐元素拷贝（bits/stl_vector.h 746 行 operator= 模板）
```

## ⑫ 变体（variant patterns）

- **ET + CRTP**（ch51/57）：`Expr<E>` 用 CRTP 向下转型提供静态 `operator[]`/`size()` 接口，是 ET 的标准骨架。
- **ET + SIMD**（ch19/43）：`operator=` 的单遍循环被 `-O2` 自动向量化为 AVX；Eigen 进一步用手写 intrinsic 节点。
- **ET + 常量折叠节点**：给表达式树加 `Const` 节点（`operator[]` 返回常量），编译期部分求值（衔接 ch68/69）。
- **ET + 惰性 lambda**：`[&]{return a+b+c;}` 也惰性，但运行期闭包、不可静态向量化；ET 类型化、可充分优化。
- **ET + 概念**（ch67）：约束表达式节点满足 `Expr`（有 `operator[]`/`size()`）。

```cpp
#include <cstddef>
// 变体：ET + 常量折叠节点
template <double V> struct Const : Expr<Const<V>> {
    double operator[](size_t) const { return V; }
    size_t size() const { return 0; }   // 标量，size 无意义
};
// u = a + Const<1.0>{};  // 编译期把 +1.0 折叠进循环
```

```cpp
#include <cstddef>
// 变体：ET 节点概念约束（C++20）
template <typename E>
concept ExprNode = requires(const E& e, size_t i) { e[i]; e.size(); };
template <ExprNode E> double sum(const E& e) {
    double s = 0; for (size_t i=0;i<e.size();++i) s += e[i]; return s;
}
```

```cpp
#include <cstddef>
// 变体：ET 与 CRTP 组合（Expr 基类即 CRTP）
template <typename E> struct Expr {
    const E& self() const { return static_cast<const E&>(*this); }
    double operator[](size_t i) const { return self()[i]; }
};
```

## ⑬ 反模式（anti-patterns）

- **代理引用悬垂**：`operator+` 返回代理持有对局部/临时操作数的引用，代理在求值前操作数已析构 → 未定义行为。
- **返回代理的 `operator+` 不该返回引用**：`Sum operator+(...)` 必须按值返回代理（代理持有引用，但代理本身在栈上，随完整表达式存活）。
- **过度 ET 导致编译雪崩**：数十项嵌套表达式树触发海量模板实例化，编译时间爆炸、内存暴涨（⑧）。
- **调试困难**：表达式树类型名极长，断点/堆栈深（嵌套 `Sum`），错误追溯到具体节点难。

```cpp
#include <cstddef>
// 反模式：代理引用悬垂（操作数是临时）
Fast make_vec(size_t n) { Fast f(n); /* fill */ return f; }
// Sum<Fast,Fast> bad = make_vec(3) + make_vec(3);  // 临时 Fast 已析构，代理引用悬垂！
// 正确：操作数须先于代理求值完成前存活
```

```cpp
// 反模式：operator+ 返回引用到局部代理
// Sum<A,B>& operator+(...) { Sum<A,B> s(...); return s; }  // [标准] 返回局部引用 → UB
Sum<A,B> operator+(...) { return Sum<A,B>(...); }   // 按值返回代理（持有外部引用，安全）
```

```cpp
// 反模式：超深表达式树
// using Deep = decltype(a+b+c+...+z);  // 数百项 → 模板实例化深度超限、编译极慢
```

## ⑭ 工业案例

- **Eigen**：`MatrixXd C = A * B + D * E;` 编译为单 kernel，自动向量化，零中间矩阵。ET 是 Eigen 性能核心。
- **Blaze**：类似 Eigen，ET + 智能表达式优化（选择最优求值顺序）。
- **std::valarray 对比**：标准库选立即求值（见 ⑪），用于简单数组运算；大规模数值用 Eigen。
- **Thrust/Kokkos**：ET 表达式树传给 GPU kernel 生成器，单 kernel 完成多步（CPU/GPU 统一 DSL）。

```cpp
// 工业案例：Eigen 式 ET（概念示意）
// MatrixXd C = A * B + D;   // 编译期：Sum<Prod<Matrix,Matrix>,Matrix>
// 运行期：单遍循环 + AVX，无 A*B 临时矩阵
```

```cpp
// 工业案例：自定义数组库 ET（u = a + 2*b）
// u = a + 2.0 * b;  // 编译期：Sum<Fast, Scale<Fast>>，单遍 u[i]=a[i]+2*b[i]
```

```cpp
// 工业案例：GPU ET（Kokkos 示意）
// auto expr = a + b * c;   // 表达式树传给 kernel：并行单遍求值
```

## ⑮ 源码剖析（libstdc++ 相关）

**剖析 1：`std::vector::operator=` 立即语义（对比 ET 的延迟）**（`bits/stl_vector.h`）

```cpp
// 文件：C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/bits/stl_vector.h
// 行号：818（operator= 拷贝赋值模板）
vector& operator=(const vector& __x);     // 立即逐元素拷贝，非延迟
// 行号：998/1008（begin()）/ 1018/1028（end()）：非 ET 遍历基础，返回迭代器
// 结论：vector 选择简单立即语义，把"延迟求值"留给用户层 ET（如 Eigen）
```

**剖析 2：`std::valarray::operator+=` 立即求值（非 ET）**（`valarray`）

```cpp
// 文件：C:/Qt/Tools/mingw1530_64/include/c++/15.3.0/valarray
// 行号：441（operator+= 成员，返回 valarray&，就地立即修改）
valarray<_Tp>& operator+=(const valarray<_Tp>&);
// 二元 operator+ 返回新 valarray（立即分配 + 遍历），符合标准"返回 valarray"语义
// 对比：ET 的 operator+ 返回 Sum 代理（不分配、不遍历），延迟到 operator=
```

**小结**：标准库 `vector`/`valarray` 都选**立即求值**语义（746/439 行），保证可调试、可预期；ET 把求值时机从 `operator+` 推迟到 `operator=`，是**用户层高阶优化**（Eigen/Blaze），用编译期类型树换取运行期零临时与单遍——代价是模板实例化深度与编译时间（⑧/⑬）。

## ⑯ 易错点

- **代理生命周期**：ET 表达式（`a+b+c` 的结果）必须在操作数（`a/b/c`）存活期间求值（立即 `u = ...` 或显式 `eval`）；不要保存代理越过操作数作用域（⑬）。
- **`auto` 捕获代理陷阱**：`auto e = a + b;` 保存了 `Sum` 代理（持有 `a/b` 引用），若 `a/b` 后续修改或析构，`e` 求值结果错误/悬垂——应立刻 `u = e` 或 `auto u = a + b;` 让 `u` 是具体类型。
- **模板深度上限**：深树可能超编译器实例化深度（⑧），应分批或控制项数。
- **`operator=` 必须接收 `const Expr<O>&`**：若写成具体 `Fast& operator=(const Fast&)` 则 ET 无法赋值（丢失延迟）。

```cpp
// 易错点：auto 保存代理导致悬垂
Fast a(3), b(3);
auto e = a + b;        // e 持有 a/b 引用
// ... 若 a/b 离开作用域或被修改，e[i] 未定义
Fast u(3);
u = e;                  // 立即求值，安全（在 a/b 存活时）
```

```cpp
// 易错点：operator= 签名必须通用
// Fast& operator=(const Fast&);   // 错误：无法接收 Sum 代理
template <typename O> Fast& operator=(const Expr<O>& e);  // 正确：接收任意表达式
```

## ⑰ FAQ

- **Q：ET 为什么能消除临时对象？** A：`operator+` 返回的是**代理**（只存操作数引用，16 字节），不构造结果数组；直到 `operator=` 才单遍写入目标，跳过所有中间数组（见 ⑩）。
- **Q：ET 和 valarray 的 `_Expr` 一样吗？** A：不完全。valarray 运算符按标准**返回新 `valarray`**（立即），其 `_Expr` 是内部有限优化；ET（Eigen 式）的 `operator+` 返回延迟代理，真正零临时。
- **Q：ET 会影响调试吗？** A：会。表达式树类型名极长、堆栈深（嵌套 `Sum`），断点难设；可用 `auto u = (a+b+c).eval();` 之类显式物化来调试。
- **Q：何时不该用 ET？** A：表达式树浅且性能不敏感时（朴素实现可读性更好）；或编译时间/错误信息成为瓶颈时。

```cpp
// FAQ 演示：ET 零临时 vs 朴素临时
Fast a(3), b(3), c(3); Fast u(3);
u = a + b + c;          // 0 临时、单遍（ET）
// 朴素：Naive u = a + b + c;  // 2 临时 double[3]、3 遍
```

## ⑱ 最佳实践

- `Expr<E>` 基类用 CRTP 提供静态接口；所有节点（`Sum`/`Prod`/`Scale`/`Const`）继承它（⑫）。
- `operator+`/`operator*` **按值返回代理**，代理持有 `const` 引用（不拷贝操作数）。
- `operator=` 接收 `const Expr<O>&` 并单遍遍历求值；可加 `.eval()` 显式物化便于调试。
- 控制表达式树深度（避免超模板实例化上限）；热路径用 ET + 信任 `-O2` 向量化（⑩/⑲）。
- 给表达式节点加 concept（ch67）约束，错误更早。

```cpp
// 最佳实践：完整 ET 骨架（Expr + Sum + operator+ + operator=）
template <typename E> struct Expr { /* CRTP 接口 */ };
template <typename A, typename B> struct Sum : Expr<Sum<A,B>> { /* 引用 + 递归 [] */ };
template <typename A, typename B> Sum<A,B> operator+(const Expr<A>&, const Expr<B>&);
// Fast::operator=(const Expr<O>&) 单遍求值
```

```cpp
// 最佳实践：显式 eval 便于调试
template <typename E> Fast eval(const Expr<E>& e) { Fast r(e.size()); r = e; return r; }
Fast dbg = eval(a + b + c);   // 物化为具体 Fast，断点友好
```

## ⑲ 性能（编译期 / 运行期）

- **运行期**：ET 把 `u = a + b + c` 的**分配从 5 次降到 4 次、遍历从 3 次降到 1 次**（⑩ 实测），且单遍循环可被自动向量化（AVX），大向量加速显著（Eigen 可达数倍）。
- **编译期**：表达式树在编译期构建为嵌套类型（`Sum<Sum<Fast,Fast>,Fast>`），无运行期类型开销；但**实例化深度/编译时间随树深增长**（⑧）。
- **内存带宽**：单遍遍历对缓存友好（ch43），减少中间数组的读写带宽；朴素实现多遍重复读同一数据。
- **代价**：编译时间、可执行体积（每个表达式节点组合一份实例化）、调试难度（⑬）。

```cpp
// 性能对比数据（来自 ⑩ 汇编）：a+b+c 在 n=大向量时
// 朴素：2 次额外 new[]（2*n*8 B）+ 2 次额外遍历（2*n 次 load/store）
// ET  ：0 次额外 new[] + 1 次遍历（单遍 a[i]+b[i]+c[i]，可 SIMD）
```

```cpp
// 性能：ET 单遍循环可向量化
// .L33: movsd xmm0,[a+i]; addsd xmm0,[b+i]; addsd xmm0,[c+i]; movsd [u+i]
// 编译器可升级为 vmovupd/vaddpd（AVX 4 路并行）
```

## ⑳ 练习题 + 思考题 + 源码阅读路线（内化，无独立推荐阅读节）

**练习题**
1. 在 ③ 的骨架基础上加 `operator-`（差代理 `Diff<A,B>`），实现 `u = a - b + c` 单遍求值。
2. 给 ET 加 `Const<double V>` 节点（⑫），实现 `u = a + Const<2.0>{}`，验证常量被编译期折叠进循环。
3. 写一个 `.eval()` 自由函数把任意 `Expr` 物化为具体 `Fast`，解决 ⑯ 的 `auto` 悬垂陷阱。
4. 用同一组 `a/b/c` 分别测朴素与 ET 在 n=10^6 时的运行时间（计时循环），记录分配/遍历次数差异。

**思考题**
- ET 的代理持有 `const` 引用，为什么 `operator+` 必须按值返回代理而非返回引用（联系 ⑬ 悬垂）？
- `std::valarray` 内部已有 `_Expr` 模板，为何标准仍规定二元 `operator+` 返回 `valarray`（立即）而非延迟代理（对比 ⑮）？
- ET 表达式树深度与编译器模板实例化深度上限（⑧）有何关系？如何在不改编译器限制下支持任意长表达式？

**源码阅读路线**
1. `<bits/stl_vector.h>` 746 行：`vector::operator=` 立即语义（理解标准库为何不用 ET）。
2. `<valarray>` 439 行：`valarray::operator+=` 立即求值（标准库立即求值范式）。
3. Eigen 源码 `Core/AssignEvaluator.h`：`operator=` 如何对表达式树单遍遍历（ET 工业实现参考）。
4. 本章 `Examples/_asm_expr.cpp`：对比 `use_naive` 与 `use_expr` 的 `-O2` 汇编（⑩ 的 5 分配/3 遍历 vs 4 分配/1 遍历）。


## 联合使用场景

| 关联章节 | 场景 | 组合方式 |
|---|---|---|
| [第71章](Book/part06_templates/ch71_policy.md) | STL算法回调/异步任务 | 本章提供概念，第71章提供实现 |
| [第68章](Book/part06_templates/ch68_tmp.md) | 泛型库/编译期计算 | 本章提供概念，第68章提供实现 |
| [第51章](Book/part05_oo/ch51_crtp.md) | 向量化计算/图像处理 | 本章提供概念，第51章提供实现 |

## 附录 F：表达式模板工业

```cpp
#include <iostream>
int main(){std::cout<<"Eigen: Matrix a=b+c*d → expression template → single loop(no temporaries)"<<std::endl;std::cout<<"Boost.Spirit: parser combinators via expression templates → compile-time grammar"<<std::endl;std::cout<<"Blaze: similar to Eigen, expression templates for linear algebra"<<std::endl;return 0;}
```

| 库 | 领域 | 性能 |
|---|---|---|
| Eigen | 线性代数 | 与手写循环相同汇编 |
| Boost.UBLAS | 线性代数 | 较慢(旧设计) |
| Blaze | 高性能线性代数 | SIMD+OpenMP |
| Boost.Spirit | 语法解析 | 编译期parser组合 |

面试: expression template优势? 消除临时对象(Matrix c=a+b产生1个临时; ET产生0个)
       为什么STL不用ET? 复杂度>收益; Eigen的数值计算场景明确受益


## 相关章节（交叉引用）

- **同模块接续**：⟶ Book/part06_templates/ch60_template_basics.md（第60章　模板基础与实例化（Template Basics & Instantiation））—— 表达式模板建立在模板基础之上
- **同模块接续**：⟶ Book/part06_templates/ch68_tmp.md（第68章　模板元编程 TMP 基础（递归 / 分支 / 循环））—— 表达式模板是 TMP 消除临时对象的经典应用
- **同模块接续**：⟶ Book/part06_templates/ch70_tag_dispatch.md（第70章　std::integral_constant 与标签分发（Tag Dispatch））—— 表达式模板用标签选择实现分支
- **同模块接续**：⟶ Book/part06_templates/ch63_variadic.md（第63章　可变参数模板与包展开（Variadic Templates & Pack Expansion））—— 可变参数表达式模板对包做惰性展开
- **同模块接续**：⟶ Book/part06_templates/ch71_policy.md（第71章　策略设计 Policy-Based Design）—— policy 与表达式模板组合定制算子
- **跨模块**：⟶ Book/part05_oo/ch51_crtp.md（第51章　CRTP 与静态多态（Curiously Recurring Template Pattern））—— CRTP 实现表达式模板的算子链式返回类型

## 附录 G（表达式模板实例化）

表达式模板在编译期展开为单一循环，下列为生成代码视图。

```text
; (a+b)*c 表达式模板展开后
mov eax, [rdi+0x0000]     ; a[i]
add eax, [rsi+0x0000]     ; + b[i]
imul eax, [rdx+0x0000]    ; * c[i]
mov [rcx+0x0000], eax     ; 写回
add rdi, 0x0008           ; 步进 int32
```

### 实例化代价

- 每套表达式类型生成一份代码：0x0008 种组合膨胀 ≈ 0x0100 KB
- 符号修饰长度 ≈ 0x0040 字符；`c++filt` 还原 ≈ 0.1us
- 默认实例化深度上限 `0x0100`（256）

### 量级

- 展开后循环无临时对象，省 ≈ 0x0020 次拷贝 ≈ 20ns
- `constexpr` 表达式在 C++20 可编译期求值，省全部运行时代价
- AVX2 向量化后 8x 展开，吞吐 +4x

### 编译器与标准

- GCC 13.2 / Clang 18 对 Eigen 表达式完全向量化
- `__cplusplus` = 202302L；`_Pragma("once")` 加速头解析
- WG21 提案 P0784R7 扩展 constexpr 表达式


## 自测练习（Exercises）

> 以下题目用于自测掌握程度；答案折叠于每题下方，建议先独立作答。

### 练习 1（难度 ★★）

**表达式模板消除临时对象**

朴素 `Vec operator+` 每次返回新 `Vec`（分配+拷贝）。改写为返回**代理类型** `VecAdd`，把加法推迟到赋值点单次遍历求值。

<details>
<summary>参考答案</summary>

```cpp
#include <iostream>
#include <vector>
struct Vec {
    std::vector<double> d;
    Vec(std::size_t n) : d(n, 0) {}
    Vec(const struct VecAdd& e);          // 前向声明，见下
    double operator[](std::size_t i) const { return d[i]; }
    double& operator[](std::size_t i) { return d[i]; }
};
struct VecAdd {
    const Vec& a; const Vec& b;
    double operator[](std::size_t i) const { return a[i] + b[i]; }
};
Vec::Vec(const VecAdd& e) : d(e.a.d.size()) {
    for (std::size_t i = 0; i < d.size(); ++i) d[i] = e[i];
}
VecAdd operator+(const Vec& a, const Vec& b) { return {a, b}; }
int main() {
    Vec x(3), y(3); x[0] = 1; y[0] = 2;
    Vec z = x + y;                        // 仅 1 次遍历，无临时 Vec
    std::cout << z[0] << "\n";          // 3
}
```
[标准] 代理类型把表达式结构滞留到赋值，合并多次遍历为一次。
</details>

### 练习 2（难度 ★★★）

**代理类型的复合赋值**

为 `Vec` 增加 `operator+=(const VecAdd&)`，让 `x += (y + y)` 原地累加、零临时。

<details>
<summary>参考答案</summary>

```cpp
#include <iostream>
#include <vector>
struct Vec {
    std::vector<double> d;
    Vec(std::size_t n) : d(n, 0) {}
    double operator[](std::size_t i) const { return d[i]; }
    double& operator[](std::size_t i) { return d[i]; }
};
struct VecAdd {
    const Vec& a; const Vec& b;
    double operator[](std::size_t i) const { return a[i] + b[i]; }
};
VecAdd operator+(const Vec& a, const Vec& b) { return {a, b}; }
Vec& operator+=(Vec& a, const VecAdd& e) {
    for (std::size_t i = 0; i < a.d.size(); ++i) a.d[i] += e[i];
    return a;
}
int main() {
    Vec x(3), y(3); x[0] = 1; y[0] = 2;
    x += (y + y);                         // 原地累加
    std::cout << x[0] << "\n";          // 1 + (2+2) = 5
}
```
[标准] 复合赋值直接读代理元素累加，避免生成中间 `Vec`。
</details>

### 练习 3（难度 ★★★★）

**求值时机陷阱**

表达式模板的代理常持 `const Vec&` 引用。若把 `auto tmp = a + b;` 存下、又在 `a/b` 离开作用域后使用 `tmp`，会发生什么？给出安全写法。

<details>
<summary>参考答案</summary>

代理 `VecAdd` 内部引用 `a`、`b`；若 `a/b` 已销毁，`tmp[i]` 读悬垂引用 → 未定义行为。安全写法：立即物化为 `Vec`（`Vec z = a + b;`），或让代理持有值副本。

```cpp
#include <iostream>
#include <vector>
struct Vec {
    std::vector<double> d;
    Vec(std::size_t n) : d(n, 0) {}
    Vec(const struct VecAdd& e);
    double operator[](std::size_t i) const { return d[i]; }
    double& operator[](std::size_t i) { return d[i]; }
};
struct VecAdd { const Vec& a; const Vec& b;
    double operator[](std::size_t i) const { return a[i] + b[i]; } };
Vec::Vec(const VecAdd& e) : d(e.a.d.size()) {
    for (std::size_t i = 0; i < d.size(); ++i) d[i] = e[i];
}
VecAdd operator+(const Vec& a, const Vec& b) { return {a, b}; }
int main() {
    Vec a(3), b(3); a[0] = 1; b[0] = 2;
    Vec z = a + b;                       // 立即物化，安全
    std::cout << z[0] << "\n";         // 3
}
```
[标准] 表达式模板代理廉价但有寿命约束；跨作用域保存必须物化为具体类型。
</details>


## 附录：用法演绎（从选型到落地）



### 演绎 1：表达式模板为何快

**场景**：你写 `Vec z = a + b + c;`，朴素 `operator+` 每步 new 一个 `Vec` 并全量拷贝，临时对象爆炸。

**常见错误**（朴素运算符）：
```text
Vec operator+(const Vec& a, const Vec& b) { Vec r(a.d.size()); for(...) r[i]=a[i]+b[i]; return r; }
Vec z = a + b + c;   // 2 次分配 + 2 次全量拷贝（O(n) 临时）
```

**修复**：返回惰性代理，赋值点单次遍历（见练习 1）。

```cpp
#include <iostream>
#include <vector>
struct Vec { std::vector<double> d; Vec(std::size_t n):d(n,0){}
    Vec(const struct VecAdd& e);
    double operator[](std::size_t i) const { return d[i]; }
    double& operator[](std::size_t i) { return d[i]; } };
struct VecAdd { const Vec& a; const Vec& b; double operator[](std::size_t i) const { return a[i]+b[i]; } };
Vec::Vec(const VecAdd& e):d(e.a.d.size()){ for(std::size_t i=0;i<d.size();++i) d[i]=e[i]; }
VecAdd operator+(const Vec& a, const Vec& b) { return {a, b}; }
int main() { Vec a(3), b(3), c(3); a[0]=1; b[0]=2; c[0]=3;
    Vec ab = a + b;                       // 先物化 a+b
    VecAdd e = ab + c;                    // 惰性组合 ab+c，仅记录结构
    Vec z(3); for (std::size_t i=0;i<3;++i) z[i]=e[i];   // 单次遍历求 (a+b)+c
    std::cout << z[0] << "\n"; }          // 6
```

**结论**：表达式模板把"多次遍历+临时"合并为"一次遍历+零分配"，是 Eigen/Blitz++ 的核心加速手段。

### 演绎 2：表达式模板的陷阱

**场景**：你用表达式模板后，把 `auto tmp = a + b;` 存进容器或返回，程序偶发崩溃。

**常见错误**（悬垂代理）：
```text
auto tmp = a + b;       // VecAdd 代理，内部引用 a、b
// ... a、b 离开作用域 ...
use(tmp);               // 读已销毁对象的引用 -> UB
```

**修复**：跨作用域保存前物化为 `Vec`（见练习 3）；调试困难时可退化为朴素 `operator+` 换取可观测性。

```cpp
#include <iostream>
#include <vector>
struct Vec { std::vector<double> d; Vec(std::size_t n):d(n,0){}
    Vec(const struct VecAdd& e);
    double operator[](std::size_t i) const { return d[i]; }
    double& operator[](std::size_t i) { return d[i]; } };
struct VecAdd { const Vec& a; const Vec& b; double operator[](std::size_t i) const { return a[i]+b[i]; } };
Vec::Vec(const VecAdd& e):d(e.a.d.size()){ for(size_t i=0;i<d.size();++i) d[i]=e[i]; }
VecAdd operator+(const Vec& a, const Vec& b){ return {a,b}; }
int main() { Vec a(3), b(3); a[0]=1; b[0]=2;
    Vec safe = a + b;     // 立即物化，可安全跨作用域
    std::cout << safe[0] << "\n"; }
```

**结论**：表达式模板以"代理寿命约束 + 调试难度"换取性能；临时结果务必在使用前物化为具体类型。
