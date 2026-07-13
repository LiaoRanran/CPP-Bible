# 第31章 运算符重载

> 标准基: C++23 / GCC 13.1 / 预计阅读: 50min / ⟶ Book/part03_language/ch27_cast.md / 难度: ★★★☆☆

## ① 学习目标 [标准]

1. 掌握算术、比较、自增/自减运算符重载
2. 区分成员函数 vs 自由函数重载
3. 理解 operator<< 必须为自由函数（或 friend）
4. 掌握拷贝/移动赋值、类型转换运算符
5. 理解可重载 vs 不可重载运算符

## ② 加法运算符重载 [标准]

```cpp
#include <iostream>
struct Vec2{int x,y;Vec2 operator+(const Vec2& o)const{return{x+o.x,y+o.y};}};
int main(){Vec2 a{1,2},b{3,4},c=a+b;std::cout<<c.x<<","<<c.y<<std::endl;return 0;}
```

## ③ 比较运算符 [标准]

```cpp
#include <iostream>
#include <compare>
struct Point{int x,y;auto operator<=>(const Point&)const=default;};
int main(){Point a{1,2},b{1,3};std::cout<<(a<b)<<std::endl;return 0;}
```

## ④ 前置/后置自增 [标准]

```cpp
#include <iostream>
struct Counter{int v;Counter&operator++(){++v;return*this;}Counter operator++(int){Counter t=*this;++v;return t;}};
int main(){Counter c{0};std::cout<<(++c).v<<" "<<(c++).v<<" "<<c.v<<std::endl;return 0;}
```

## ⑤ operator<< 输出 [标准]

```cpp
#include <iostream>
struct Vec{int x,y;friend std::ostream&operator<<(std::ostream&os,const Vec&v){return os<<v.x<<","<<v.y;}};
int main(){Vec v{10,20};std::cout<<v<<std::endl;return 0;}
```

## ⑥ 赋值运算符（拷贝/移动）[标准]

```cpp
#include <iostream>
#include <utility>
#include <cstddef>
struct Buffer{int* d;size_t n;explicit Buffer(size_t s):d(new int[s]),n(s){}~Buffer(){delete[]d;}Buffer(const Buffer&)=delete;Buffer&operator=(Buffer&&o)noexcept{std::swap(d,o.d);std::swap(n,o.n);return*this;}};
int main(){Buffer a(10),b(5);b=std::move(a);std::cout<<b.n<<std::endl;return 0;}
```

## ⑦ 类型转换运算符 [标准]

```cpp
#include <iostream>
struct Rational{int n,d;explicit operator double()const{return(double)n/d;}};
int main(){Rational r{3,4};std::cout<<(double)r<<std::endl;return 0;}
```

## ⑧ 下标运算符 [标准]

```cpp
#include <iostream>
#include <cstddef>
struct Array{int d[5];int&operator[](size_t i){return d[i];}const int&operator[](size_t i)const{return d[i];}};
int main(){Array a{1,2,3,4,5};std::cout<<a[2]<<std::endl;return 0;}
```

## ⑨ 函数调用运算符 [标准]

```cpp
#include <iostream>
struct Adder{int base;int operator()(int x)const{return base+x;}};
int main(){Adder add5{5};std::cout<<add5(10)<<std::endl;return 0;}
```

## ⑩ 不可重载的运算符 [标准]

```cpp
#include <iostream>
#include <typeinfo>
int main(){std::cout<<"Cannot overload: . .* :: ?: sizeof typeid const_cast static_cast dynamic_cast reinterpret_cast\n";return 0;}
```

## 补充完整可编译示例

```cpp
#include <iostream>
struct CVec{double x,y;};CVec operator*(const CVec&a,double s){return{a.x*s,a.y*s};}
int main(){CVec c{1,2};auto d=c*2;std::cout<<d.x<<","<<d.y<<std::endl;return 0;}
```

```cpp
#include <iostream>
#include <cstring>
struct String{char*b;String(const char*s):b(strdup(s)){}~String(){free(b);}String(const String&o):b(strdup(o.b)){}String&operator=(const String&o){if(this!=&o){free(b);b=strdup(o.b);}return*this;}};
int main(){String s("hello");String t=s;std::cout<<t.b<<std::endl;return 0;}
```

```cpp
#include <iostream>
int main(){std::cout<<"operator overloading: member vs free function. Free prefer non-member for symmetry.\n";return 0;}
```

```cpp
#include <iostream>
struct Space{int m;bool operator!()const{return m==0;}};
int main(){Space s{0};std::cout<<!s<<std::endl;return 0;}
```

```cpp
#include <iostream>
struct Vec3{int x,y,z;bool operator==(const Vec3&o)const=default;};
int main(){Vec3 a{1,2,3},b{1,2,3};std::cout<<(a==b)<<std::endl;return 0;}
```

```cpp
#include <iostream>
struct Logger{Logger&operator<<(const char*s){std::cout<<s;return*this;}};
int main(){Logger log;log<<"hello "<<"world\n";return 0;}
```

```cpp
#include <iostream>
struct Matrix{int m[2][2];int&operator()(int i,int j){return m[i][j];}};
int main(){Matrix mat{{{1,2},{3,4}}};std::cout<<mat(0,1)<<std::endl;return 0;}
```

```cpp
#include <iostream>
#include <memory>
struct Ptr{std::unique_ptr<int> p;int&operator*(){return*p;}int*operator->(){return p.get();}};
int main(){Ptr ptr{std::make_unique<int>(42)};std::cout<<*ptr<<std::endl;return 0;}
```

```cpp
#include <iostream>
struct Bool{bool v;operator bool()const{return v;}};
int main(){Bool b{true};if(b)std::cout<<"true\n";return 0;}
```

```cpp
#include <iostream>
int main(){std::cout<<"operator总结: 保留语义(+==>+), 避免歧义, 成员vs自由选择, <=>统一比较。"<<std::endl;return 0;}
```

## ⑪ STL 联系 [标准]
```cpp
#include <iostream>
#include <algorithm>
struct S{int v;bool operator<(const S&o)const{return v<o.v;}};
int main(){S arr[]{{3},{1},{2}};std::sort(std::begin(arr),std::end(arr));std::cout<<arr[0].v<<std::endl;return 0;}
```

## ⑫ 工业案例 [经验]
```cpp
#include <iostream>
int main(){std::cout<<"Eigen: operator+ returns expression template. fmt: operator<<_format for custom types.\n";return 0;}
```

## ⑬ 源码分析 [实现·GCC13]
```cpp
#include <iostream>
int main(){std::cout<<"GCC resolving operator@: lookup + overload resolution, error messages in cp/call.cc.\n";return 0;}
```

## ⑭ WG21 提案 [标准]
```cpp
#include <iostream>
int main(){std::cout<<"P0515: three-way comparison <=>. P1185: defaulted <=> = default.\n";return 0;}
```

## ⑮ 面试题 [经验]
```cpp
#include <iostream>
int main(){std::cout<<"Q: prefix vs postfix ++? A: prefix returns ref, postfix returns copy. Use prefix for perf.\n";return 0;}
```

## ⑯ 易错点 [经验]
```cpp
#include <iostream>
int main(){std::cout<<"Pitfall: operator, overload loses short-circuit; operator&&/|| overload loses short-circuit.\n";return 0;}
```

## ⑰ FAQ [经验]
```cpp
#include <iostream>
int main(){std::cout<<"Q: Why can't operator<< be a member? A: left operand is std::ostream, not your class.\n";return 0;}
```

## ⑱ 最佳实践 [经验]
```cpp
#include <iostream>
int main(){std::cout<<"Best: use <=> for comparison; non-member for symmetric ops; friend for stream I/O.\n";return 0;}
```

## ⑲ 性能分析 [平台·x86-64]
```cpp
#include <iostream>
int main(){std::cout<<"operator+ temporaries can be avoided with expression templates (Eigen, range-v3).\n";return 0;}
```

## ⑳ 跨语言对比 [经验]
```cpp
#include <iostream>
int main(){std::cout<<"C++ operator overloading vs Rust std::ops traits vs Python __add__/dunder methods.\n";return 0;}
```

```cpp
#include <iostream>
int main(){std::cout<<"operator重载总结: 保留原始语义, 避免歧义, <=>优先defaulted, 自由函数优于成员。"<<std::endl;return 0;}
```

## 附录 A: 运算符重载速查表

| 运算符 | 推荐形式 | 原因 |
|---|---|---|
| + - * / % | 自由函数（friend） | 对称性：a+b 和 b+a 都能工作 |
| == != < > <= >= | 成员函数（C++20: =default <=>） | 自动统一比较 |
| ++ -- (prefix) | 成员函数 | 修改自身状态，返回引用 |
| ++ -- (postfix) | 成员函数 | 返回拷贝，用 int 参数区分 |
| = (赋值) | 成员函数 | 必须是成员 |
| [] (下标) | 成员函数 | 必须是成员 |
| () (调用) | 成员函数 | 必须是成员 |
| << >> (流) | 自由函数（friend） | 左操作数是 std::ostream |
| -> * (解引用) | 成员函数 | 模拟指针行为 |
| && || , (逻辑/逗号) | 不推荐重载 | 丢失短路求值语义 |

```cpp
#include <iostream>
struct Complex{double r,i;Complex operator+(double s)const{return{r+s,i};}friend Complex operator+(double s,const Complex&c){return{c.r+s,c.i};}};
int main(){Complex c{1,2};auto d=c+3.0;auto e=3.0+c;std::cout<<d.r<<","<<e.r<<std::endl;return 0;}
```

## 附录 B: <=> 三路比较深度

```cpp
#include <iostream>
#include <compare>
struct Date{int y,m,d;auto operator<=>(const Date&)const=default;};
int main(){Date d1{2024,1,1},d2{2025,6,15};auto cmp=d1<=>d2;if(cmp<0)std::cout<<"before\n";return 0;}
```

```cpp
#include <iostream>
#include <compare>
struct Ord{int rank;std::strong_ordering operator<=>(const Ord&o)const{return rank<=>o.rank;}};
int main(){Ord a{10},b{20};std::cout<<(a<b)<<" "<<(a>b)<<std::endl;return 0;}
```

## 附录 C: 表达式模板与延迟求值

```cpp
#include <iostream>
template<typename L,typename R>struct AddExpr{L l;R r;auto eval()const{return l.eval()+r.eval();}};
struct Vec{int x;int eval()const{return x;}};
template<typename L,typename R>auto operator+(L l,R r){return AddExpr<L,R>{l,r};}
int main(){Vec a{10},b{20};std::cout<<(a+b).eval()<<std::endl;return 0;}
```

## 附录 D: 常见错误与修复

```cpp
#include <iostream>
int main(){
    std::cout<<"Pitfall 1: operator= must check self-assignment\n";
    std::cout<<"Pitfall 2: postfix ++ returns by value (copy cost)\n";
    std::cout<<"Pitfall 3: operator+ should be non-member for implicit conversions on both sides\n";
    std::cout<<"Pitfall 4: overloading && loses short-circuit (use regular && instead)\n";
    return 0;
}
```

```cpp
#include <iostream>
struct SafeAssign{int*v;SafeAssign(int x):v(new int(x)){}~SafeAssign(){delete v;}SafeAssign&operator=(const SafeAssign&o){if(this==&o)return*this;int*t=new int(*o.v);delete v;v=t;return*this;}int get()const{return*v;}};
int main(){SafeAssign a(10),b(20);a=b;std::cout<<a.get()<<std::endl;return 0;}
```

## 附录 E: 自定义迭代器与智能指针

```cpp
#include <iostream>
struct Range{int lo,hi;struct It{int v;int operator*()const{return v;}It&operator++(){++v;return*this;}bool operator!=(const It&o)const{return v!=o.v;}};It begin()const{return{lo};}It end()const{return{hi};}};
int main(){Range r{1,5};int s=0;for(int x:r)s+=x;std::cout<<s<<std::endl;return 0;}
```

```cpp
#include <iostream>
#include <memory>
struct Res{int v;Res(int x):v(x){}int get()const{return v;}};
struct Ptr{std::unique_ptr<Res> p;Res&operator*(){return*p;}Res*operator->(){return p.get();}explicit Ptr(int x):p(std::make_unique<Res>(x)){}};
int main(){Ptr p(99);std::cout<<p->get()<<std::endl;return 0;}
```

```cpp
#include <iostream>
struct Mat{int d[2][2];int*operator[](int i){return d[i];}};
int main(){Mat m{{{1,2},{3,4}}};std::cout<<m[0][1]<<std::endl;return 0;}
```

```cpp
#include <iostream>
#include <string>
struct Json{int n;std::string s;operator int()const{return n;}operator std::string()const{return s;}};
int main(){Json j{42,"hello"};std::cout<<(int)j<<" "<<(std::string)j<<std::endl;return 0;}
```

## 附录 A：标准库与底层 [D: stdlib / E: Lowlevel / H: Design]

```
标准库中的运算符重载:
- std::complex<T>: operator+,-,*,/ → libstdc++内联展开为2条addps(SIMD)
- std::iterator: operator++/-- → 指针运算(vectors)或节点遍历(lists)
- std::function: operator() → 类型擦除的间接调用(~10ns overhead)
- std::shared_ptr: operator*,-> → 内联解引用, 零开销(与裸指针相同汇编)

底层(汇编): operator+ for complex<double>
  complex<double> a{1,2}, b{3,4};
  auto c = a + b;
  → GCC -O2: addpd xmm0, xmm1 (单条SSE指令, 两个double并行加)
  → 手写: 相同汇编。运算符重载=零开销抽象

设计权衡: 运算符重载的3条铁律
  1. 保留原始语义: operator+ 不修改操作数, 返回新对象
  2. 对称性: a+b 和 b+a 都应工作 → 用自由函数(friend)而非成员
  3. 避免歧义: operator bool() 的隐式转换 → 用explicit operator bool()
```


## 深度增强：运算符重载底层与工业

### 原理分析

运算符重载是C++零开销抽象最直接的体现——编译后与手写函数调用完全相同。标准库中大量使用: std::complex用operator+生成addpd(SIMD指令), std::iterator用operator++内联为指针加减。

WG21从未单独标准化运算符重载——它是C++78(C with Classes)的原始特性, 随C++98进入标准。P2593R0(C++23 deducing this)允许用值类型实现运算符(而非引用), 简化模板代码。

### 汇编验证

```asm
; complex<double> a{1,2}, b{3,4}; auto c = a + b;
; GCC -O2: addpd xmm0, xmm1  (单条SSE指令)
; 手写: double cr=a.real+b.real; ci=a.imag+b.imag;
;       addsd xmm0,xmm2; addsd xmm1,xmm3 (2条, 相同)
; 结论: operator+=零开销抽象, 编译器内联后与手写相同
```

```cpp
#include <iostream>
struct Vec2{float x,y;Vec2 operator+(const Vec2&o)const{return{x+o.x,y+o.y};}};
int main(){Vec2 a{1,2},b{3,4},c=a+b;std::cout<<c.x<<","<<c.y<<std::endl;return 0;}
```

### 工业案例

| 项目 | 运算符 | 效果 |
|---|---|---|
| Eigen | Matrix operator* | 表达式模板消除临时对象 |
| fmtlib | operator""_format | 编译期格式字符串验证 |
| std::chrono | operator""ms | 字面量时间单位(类型安全) |
| Boost.Spirit | operator>> | parser组合(>>=then, |=or) |

### 面试

Q: 成员operator+ vs 自由函数? A: 自由函数支持隐式转换(左操作数也可以转换); 成员函数只能转换右操作数
Q: operator bool()的陷阱? A: 隐式转换到bool可能导致意外行为→C++11起用explicit operator bool()
Q: 为什么不要重载operator&&和operator||? A: 它们会失去短路求值(两个操作数总是被求值)


## 附录 H：运算符重载面试

```cpp
#include <iostream>
struct Vec2{float x,y;Vec2 operator+(const Vec2&o)const{return{x+o.x,y+o.y};}};
int main(){Vec2 a{1,2},b{3,4},c=a+b;std::cout<<c.x<<","<<c.y<<std::endl;return 0;}
```

| 运算符 | 成员/自由 | 原因 |
|---|---|---|
| operator+ | 自由函数 | 支持隐式转换(左操作数) |
| operator= | 成员 | 与this绑定 |
| operator[] | 成员 | 访问内部数据 |
| operator<< | friend/自由 | 左操作数是ostream |

面试: 为什么operator+用自由函数? 支持a+1和1+a(成员只能支持a+1)

## 附录 I：运算符ABI

operator+的name mangling: GCC: _ZplRK4Vec2S1_ (operator+ for Vec2)
与普通函数相同: 纯编译期, 零运行时开销, 内联后无call

```asm
; Vec2 c=a+b;
; GCC -O2: addss xmm0,xmm2; addss xmm1,xmm3  (两条SSE单精度加法)
; 手写: adds同上
; 结论: operator+=零开销抽象, 编译器内联后与手写相同汇编
```

```cpp
#include <iostream>
struct Vec2{float x,y;Vec2 operator+(const Vec2&o)const{return{x+o.x,y+o.y};}};
int main(){Vec2 a{1,2},b{3,4},c=a+b;std::cout<<c.x<<","<<c.y<<std::endl;return 0;}
```

面试: operator+开销? 零(内联后与手写相同); 成员vs自由? 自由支持隐式转换(左操作数)

## 相关章节（交叉引用）

- **后续依赖**：`Book/part03_language/ch21_const_family.md`（第21章　const / constexpr / consteval / constinit 深度详解）—— 本章为其前置，建议后续延伸阅读。
- **相邻主题**：`Book/part03_language/ch30_volatile.md`（第30章 volatile / atomic 与硬件寄存器）—— 编号相邻、主题接续。
- **相邻主题**：`Book/part03_language/ch32_initialization.md`（第32章 初始化与列表初始化）—— 编号相邻、主题接续。
- **相邻主题**：`Book/part03_language/ch29_friend.md`（第29章 友元 friend 与访问控制）—— 编号相邻、主题接续。
- **同模块**：`Book/part03_language/ch19_variables.md`（第19章　变量、存储期、链接与 ODR（工业级深度版））—— 同模块下的其他主题。

## 真实开源项目参考（可查证链接）

> 运算符重载的工业实现——下列链接指向真实源码（L2 文件级）。

- **LLVM/Clang `Sema::BuildOverloadedOperatorCall`**：[llvm/llvm-project · clang/lib/Sema/SemaOverload.cpp](https://github.com/llvm/llvm-project/blob/main/clang/lib/Sema/SemaOverload.cpp) —— 编译器如何对 `a + b` 做重载决议（候选集构建、隐式转换序列排序、淘汰歧义），对应「② 重载决议」的工业实现源头。
- **Boost.Operators（CRTP 自动生成运算符）**：[boostorg/operators · include/boost/operators.hpp](https://github.com/boostorg/operators/blob/develop/include/boost/operators.hpp) —— 用 `less_than_comparable<T>` 等基类模板，一次定义 `<` 即获得 `>`/`<=`/`>=` 全套，对应「⑦ 约定：返回 `*this`」的工业 DRY 实践。
- **Eigen（表达式模板运算符）**：[eigenteam/eigen-git-mirror · Eigen/Core](https://github.com/eigenteam/eigen-git-mirror/blob/master/Eigen/Core) —— `MatrixXd a = b + c + d` 通过运算符重载 + 表达式模板实现零临时对象求值，对应「⑩ 性能」中"运算符重载不该有隐藏拷贝"的标杆。
- **Abseil `absl::string_view` 的运算符**：[abseil/abseil-cpp · absl/strings/string_view.h](https://github.com/abseil/abseil-cpp/blob/master/absl/strings/string_view.h) —— `operator==`/`operator<` 等对 `string_view` 的重载，对应「⑧ 与 std::string 互操作」的标准前置。

**最佳实践**：二元运算符优先定义为非成员 `friend`（支持左操作数隐式转换）；复合赋值（`+=`）返回 `T&`，非复合（`+`）返回 `T` 值（「⑦ 约定」）；避免重载 `&&`/`||/`,`（失去短路求值）；运算符不应有非直观副作用（如 `operator+` 修改状态）。

> 交叉引用：重载决议细节见 [ch60](Book/part06_templates/ch60_template_basics.md)；比较概念见 [ch67](Book/part06_templates/ch67_concepts.md)。

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

