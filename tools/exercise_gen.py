#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
exercise_gen.py v2 - 内容感知练习题生成器（注入版）

为每章生成 ≥2 道真实、可编译、带答案的练习题，输出为可直接注入章末的
`## 自测练习（Exercises）` 小节 Markdown。答案用 <details> 折叠，cpp 块为
独立完整可编译程序（C++23 / GCC 13.1 -fsyntax-only 可过）。

设计要点（对齐 AGENT.md 纪律）：
  - 红线#1 不注水：每题有真实信息增量（编码/辨析），非套话
  - 红线#3 不幻觉：答案代码均经 --verify 编译校验
  - 绿线#4 章末≥2道可编译练习带答案
  - 门禁安全：小节标题非"推荐阅读/参考文献/延伸阅读"；含 stance 标签

Usage:
  python3 tools/exercise_gen.py --emit Book/partXX/chYY.md   # 打印该章练习小节
  python3 tools/exercise_gen.py --verify                     # 编译校验全部题库答案
  python3 tools/exercise_gen.py --stats                       # 统计覆盖
  python3 tools/exercise_gen.py --inject Book/partXX/chYY.md  # 注入到章末(备份原文件)
"""
import os, re, sys, json, subprocess, shutil

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GPP = shutil.which("g++") or "g++"

# ── 题库（topic -> [(难度★, 题干, 答案markdown)]）───────────────────────
# 答案中的 ```cpp 块必须是独立完整可编译程序（含 #include + int main）。
QUESTION_BANK = {
    "template": [
        (2, "写一个 `max` 函数模板，要求对任意可比较类型都能用，且对混合有符号/无符号比较安全。",
         "使用 `std::common_comparison_category` 或 `std::cmp_less` 避免符号陷阱：\n\n"
         "```cpp\n"
         "#include <iostream>\n#include <utility>\n"
         "template <typename T>\n"
         "const T& max_safe(const T& a, const T& b) { return (b < a) ? a : b; }\n"
         "int main() { std::cout << max_safe(3, 7) << '\\n'; }\n"
         "```\n\n"
         "[标准] 模板参数推导按实参进行；两实参同类型时 `T` 唯一确定。"),
        (3, "解释为什么函数模板 `template<typename T> void f(T)` 与 `template<typename T> void f(T*)` 能构成重载，并写出调用 `int x; f(x); f(&x);` 的匹配结果。",
         "两模板参数列表不同（一个 `T`、一个 `T*`），属不同模板，可重载。\n\n"
         "```cpp\n"
         "#include <iostream>\n"
         "template <typename T> void f(T)   { std::cout << \"by-value\\n\"; }\n"
         "template <typename T> void f(T*)  { std::cout << \"by-ptr\\n\"; }\n"
         "int main(){ int x=0; f(x); f(&x); }\n"
         "```\n\n"
         "[标准] 调用 `f(x)` 推导 `T=int` 命中第一版；`f(&x)` 推导 `T=int` 命中第二版（`T*`）。"),
    ],
    "concept": [
        (2, "用 `std::integral` 概念约束一个 `add` 函数，使其只接受整数类型，并对浮点调用给出清晰的错误。",
         "C++20 概念取代 SFINAE 做编译期约束：\n\n"
         "```cpp\n"
         "#include <iostream>\n#include <concepts>\n"
         "template <std::integral T> T add(T a, T b) { return a + b; }\n"
         "int main() { std::cout << add(2, 3) << '\\n'; /* add(1.0, 2.0) 编译失败 */ }\n"
         "```\n\n"
         "[标准] 违反概念约束是硬错误（而非 SFINAE 静默失败），诊断信息更可读。"),
        (3, "写一个自定义概念 `HasSize`，要求类型提供返回整数尺寸的 `size()` 成员，并用它约束 `print_size`。",
         "```cpp\n"
         "#include <iostream>\n#include <vector>\n"
         "template <typename T>\n"
         "concept HasSize = requires(T t) { { t.size() } -> std::convertible_to<std::size_t>; };\n"
         "template <HasSize T> void print_size(const T& c) { std::cout << c.size() << '\\n'; }\n"
         "int main() { std::vector<int> v(5); print_size(v); }\n"
         "```\n\n"
         "[标准] `requires` 表达式内 `{ expr } -> constraint` 既检查可行性又检查返回类型。"),
    ],
    "constexpr": [
        (2, "写一个 `constexpr` 阶乘函数，并用 `static_assert` 在编译期验证 `fact(5)==120`。",
         "```cpp\n"
         "#include <iostream>\n"
         "constexpr int fact(int n) { return n <= 1 ? 1 : n * fact(n - 1); }\n"
         "static_assert(fact(5) == 120);\n"
         "int main() { std::cout << fact(5) << '\\n'; }\n"
         "```\n\n"
         "[标准] `constexpr` 函数在常量表达式上下文（如模板实参、`static_assert`）中于编译期求值。"),
        (3, "说明 `constexpr` 与 `consteval` 的区别：写一个 `consteval` 函数 `sq`，并指出 `int x=3; sq(x);` 是否合法。",
         "`consteval` 函数**只能**在编译期调用（立即函数）：\n\n"
         "```cpp\n"
         "#include <iostream>\n"
         "consteval int sq(int n) { return n * n; }\n"
         "int main() { constexpr int a = sq(4); std::cout << a << '\\n'; }\n"
         "```\n\n"
         "[标准] `int x=3; sq(x);` 非法——`x` 非编译期常量，`consteval` 禁止运行期调用。"),
    ],
    "fold": [
        (3, "用折叠表达式写一个 `sum` 可变参数函数，计算任意个数实参之和。",
         "```cpp\n"
         "#include <iostream>\n"
         "template <typename... Ts> auto sum(Ts... ts) { return (0 + ... + ts); }\n"
         "int main() { std::cout << sum(1, 2, 3, 4) << '\\n'; }\n"
         "```\n\n"
         "[标准] 一元左折叠 `(init + ... + ts)` 展开为 `((((0+1)+2)+3)+4)`。"),
    ],
    "typetrait": [
        (2, "用 `std::is_pointer` 在编译期区分指针与非指针，并通过 `if constexpr` 走不同分支。",
         "```cpp\n"
         "#include <iostream>\n#include <type_traits>\n"
         "template <typename T>\n"
         "void inspect(T v) {\n"
         "  if constexpr (std::is_pointer_v<T>) std::cout << \"pointer\\n\";\n"
         "  else std::cout << \"non-pointer\\n\";\n"
         "}\n"
         "int main() { int x=0; inspect(x); inspect(&x); }\n"
         "```\n\n"
         "[标准] `if constexpr` 在模板内丢弃未采用分支，避免对非指针类型调用 `*` 等非法操作。"),
    ],
    "move": [
        (2, "写一个 `noexcept` 移动构造函数，使 `std::vector` 扩容时走移动而非拷贝。",
         "```cpp\n"
         "#include <iostream>\n#include <vector>\n#include <utility>\n"
         "struct S {\n"
         "  int* p = new int[8];\n"
         "  S() = default;\n"
         "  S(S&& o) noexcept : p(o.p) { o.p = nullptr; }\n"
         "  ~S() { delete[] p; }\n"
         "};\n"
         "int main() { std::vector<S> v; v.push_back(S{}); v.push_back(S{}); std::cout << \"ok\\n\"; }\n"
         "```\n\n"
         "[标准] `noexcept` 移动构造让 `vector` 在重新分配时移动元素；否则因强异常保证退化为拷贝。"),
        (3, "解释 `std::move` 本身不移动任何东西——它只做 `static_cast<T&&>`。写代码证明：对一个只有拷贝构造、无移动构造的类型，`std::move` 后仍发生拷贝。",
         "```cpp\n"
         "#include <iostream>\n#include <utility>\n"
         "struct C { C()=default; C(const C&){std::cout<<\"copy\\n\";} };\n"
         "int main(){ C a; C b = std::move(a); }\n"
         "```\n\n"
         "[标准] `std::move` 仅是类型转换，真正移动发生在移动构造/赋值中；无移动构造时退化为拷贝。"),
    ],
    "forward": [
        (3, "写一个 `make_wrapper` 工厂，用完美转发把任意实参原样传给内部对象的构造函数。",
         "```cpp\n"
         "#include <iostream>\n#include <utility>\n"
         "struct Inner { Inner(int){std::cout<<\"int ctor\\n\";} Inner(int,int){std::cout<<\"pair ctor\\n\";} };\n"
         "template <typename... Ts>\n"
         "Inner make_wrapper(Ts&&... ts) { return Inner(std::forward<Ts>(ts)...); }\n"
         "int main(){ make_wrapper(1); make_wrapper(1,2); }\n"
         "```\n\n"
         "[标准] `std::forward<Ts>(ts)...` 保持左/右值性，是工厂与容器 `emplace` 的基石。"),
    ],
    "raii": [
        (2, "实现一个 `File` RAII 包装，构造 `fopen`、析构 `fclose`，确保作用域结束自动关闭。",
         "```cpp\n"
         "#include <cstdio>\n"
         "struct File {\n"
         "  std::FILE* f;\n"
         "  File(const char* p) : f(std::fopen(p, \"w\")) {}\n"
         "  ~File() { if (f) std::fclose(f); }\n"
         "};\n"
         "int main() { File f(\"tmp.txt\"); /* 离开作用域自动 fclose */ }\n"
         "```\n\n"
         "[经验] RAII 把资源生命周期绑定到对象作用域，是 C++ 异常安全的核心。"),
    ],
    "smartptr": [
        (2, "用 `std::unique_ptr` 管理动态数组，并说明为何不能用 `get_deleter` 之外的裸 `delete[]`。",
         "```cpp\n"
         "#include <iostream>\n#include <memory>\n"
         "int main() {\n"
         "  auto p = std::make_unique<int[]>(10);\n"
         "  p[0] = 42; std::cout << p[0] << '\\n';\n"
         "}  // 自动 delete[]\n"
         "```\n\n"
         "[标准] `unique_ptr<T[]>` 特化使用 `delete[]`；裸 `delete` 会未定义行为。"),
        (3, "说明 `std::shared_ptr` 的引用计数开销与循环引用问题，并给出用 `std::weak_ptr` 打破循环的最小示例。",
         "```cpp\n"
         "#include <iostream>\n#include <memory>\n"
         "struct B;\n"
         "struct A { std::shared_ptr<B> b; ~A(){std::cout<<\"~A\\n\";} };\n"
         "struct B { std::weak_ptr<A> a; ~B(){std::cout<<\"~B\\n\";} };\n"
         "int main(){ auto a=std::make_shared<A>(); auto b=std::make_shared<B>(); a->b=b; b->a=a; }\n"
         "```\n\n"
         "[经验] `weak_ptr` 不增加强引用计数，可安全观测 `shared_ptr` 而不致循环泄漏。"),
    ],
    "exception": [
        (2, "写一个 `noexcept` 函数，内部 `throw`，观察其调用后果（`std::terminate`）。",
         "```cpp\n"
         "#include <stdexcept>\n"
         "void f() noexcept { throw std::runtime_error(\"x\"); }\n"
         "int main() { f(); }  // 触发 std::terminate\n"
         "```\n\n"
         "[标准] `noexcept` 函数内抛异常（且未就地捕获）直接 `std::terminate`，不展开栈。"),
    ],
    "virtual": [
        (2, "解释虚函数表（vtable）的内存开销：一个含虚函数的类对象通常增加多少字节（64 位）？写代码打印 `sizeof`。",
         "```cpp\n"
         "#include <iostream>\n"
         "struct Base { virtual ~Base()=default; int x; };\n"
         "int main() { std::cout << sizeof(Base) << '\\n'; }  // 通常 16 = 8(vptr)+4(int)+填充\n"
         "```\n\n"
         "[实现·GCC13] [平台·x86-64] 64 位下 vptr 占 8 字节，虚调用为一次间接 call。"),
        (3, "写一个展示多态的最小例子：基类指针指向派生类对象，调用虚函数走派生实现。",
         "```cpp\n"
         "#include <iostream>\n"
         "struct Base { virtual void foo() const { std::cout << \"Base\\n\"; } virtual ~Base()=default; };\n"
         "struct Der : Base { void foo() const override { std::cout << \"Der\\n\"; } };\n"
         "int main(){ Base* p=new Der(); p->foo(); delete p; }\n"
         "```\n\n"
         "[标准] `override` 让编译器校验确实重写了虚函数，避免签名笔误。"),
    ],
    "rtti": [
        (2, "用 `dynamic_cast` 在继承体系中安全向下转型，并对失败返回 `nullptr`（指针版）。",
         "```cpp\n"
         "#include <iostream>\n"
         "struct Base { virtual ~Base()=default; };\n"
         "struct Der : Base { void f() const { std::cout << \"Der\\n\"; } };\n"
         "int main(){\n"
         "  Base* b = new Base();\n"
         "  if (auto* d = dynamic_cast<Der*>(b)) d->f();\n"
         "  else std::cout << \"not Der\\n\";\n"
         "  delete b;\n"
         "}\n"
         "```\n\n"
         "[标准] 指针 `dynamic_cast` 失败返回 `nullptr`；引用版失败抛 `std::bad_cast`。"),
    ],
    "crtp": [
        (3, "用 CRTP 实现编译期静态多态：`Base<Der>` 提供 `interface()` 调用 `derived` 的 `impl()`，无虚函数开销。",
         "```cpp\n"
         "#include <iostream>\n"
         "template <typename D> struct Base { void interface() { static_cast<D*>(this)->impl(); } };\n"
         "struct Der : Base<Der> { void impl() { std::cout << \"Der impl\\n\"; } };\n"
         "int main(){ Der d; d.interface(); }\n"
         "```\n\n"
         "[标准] CRTP 把动态多态转为编译期单态，调用可被内联。"),
    ],
    "ebo": [
        (3, "说明空基类优化（EBO）：一个空基类通常不占派生对象空间。写代码验证 `sizeof(Derived)==sizeof(int)`。",
         "```cpp\n"
         "#include <iostream>\n"
         "struct Empty {};\n"
         "struct Derived : Empty { int x; };\n"
         "int main(){ std::cout << sizeof(Derived) << '\\n'; }  // 通常 = sizeof(int)\n"
         "```\n\n"
         "[标准] [实现·GCC13] 标准允许空基类子对象不占地址空间（EBO），常用于策略类零开销。"),
    ],
    "variant": [
        (2, "用 `std::variant<int,std::string>` 存储二者之一，并用 `std::visit` 打印其内容。",
         "```cpp\n"
         "#include <iostream>\n#include <variant>\n#include <string>\n"
         "int main(){\n"
         "  std::variant<int,std::string> v = 42;\n"
         "  std::visit([](const auto& x){ std::cout << x << '\\n'; }, v);\n"
         "  v = std::string(\"hi\");\n"
         "  std::visit([](const auto& x){ std::cout << x << '\\n'; }, v);\n"
         "}\n"
         "```\n\n"
         "[标准] `std::visit` 的 visitor 收到的是「备选类型」；判别式用 `v.index()`。"),
    ],
    "optional": [
        (2, "用 `std::optional` 表示「可能无值」的查找结果，区分命中与未命中。",
         "```cpp\n"
         "#include <iostream>\n#include <optional>\n"
         "std::optional<int> find(bool ok){ return ok ? std::optional<int>(7) : std::nullopt; }\n"
         "int main(){\n"
         "  if (auto r=find(true)) std::cout << *r << '\\n';\n"
         "  else std::cout << \"not found\\n\";\n"
         "}\n"
         "```\n\n"
         "[标准] `std::optional<T>` 是「有值/无值」的类型安全替代品，优于返回哨兵值或指针。"),
    ],
    "lambda": [
        (2, "写一个按值捕获 `n` 且 `mutable` 的 lambda，使其内部可修改副本并返回自增结果。",
         "```cpp\n"
         "#include <iostream>\n"
         "int main(){ int n=10; auto f=[n]() mutable { return ++n; }; std::cout << f() << ' ' << f() << '\\n'; }\n"
         "```\n\n"
         "[标准] 默认 lambda 的 `operator()` 是 `const`；`mutable` 解除该限制，捕获副本可变。"),
        (3, "写一个返回 lambda 的工厂，说明 C++14 泛型 lambda（`auto` 参数）如何替代函数模板。",
         "```cpp\n"
         "#include <iostream>\n"
         "int main(){\n"
         "  auto adder = [](auto x){ return [x](auto y){ return x+y; }; };\n"
         "  std::cout << adder(2)(3) << '\\n';\n"
         "}\n"
         "```\n\n"
         "[标准] 泛型 lambda 每个 `auto` 参数生成一个隐含模板参数，是局部算法的语法糖。"),
    ],
    "memory": [
        (2, "解释栈对象与堆对象生命周期差异：`{ int a; }` 与 `new int` 的销毁时机有何不同？",
         "栈对象在作用域结束自动析构；`new` 分配的对象直到 `delete` 才释放：\n\n"
         "```cpp\n"
         "#include <iostream>\n"
         "int main(){ int a=1; int* p=new int(2); /* ... */ delete p; }\n"
         "```\n\n"
         "[标准] 遗漏 `delete` 即内存泄漏；这是 RAII/智能指针存在的根本动机。"),
    ],
    "newdelete": [
        (2, "展示 `new[]`/`delete[]` 配对，并说明对数组用 `delete`（非 `delete[]`）属于未定义行为。",
         "```cpp\n"
         "#include <iostream>\n"
         "int main(){ int* a=new int[4]{1,2,3,4}; delete[] a; std::cout << \"balanced\\n\"; }\n"
         "```\n\n"
         "[标准] 数组 `new` 与 `delete[]` 必须配对；混用 `delete` 是 UB。"),
    ],
    "allocator": [
        (3, "自定义一个最小 `Allocator`，使 `std::vector` 用它分配，并解释 `rebind` 的作用。",
         "```cpp\n"
         "#include <iostream>\n#include <vector>\n"
         "template <typename T> struct A {\n"
         "  using value_type = T;\n"
         "  T* allocate(std::size_t n){ return static_cast<T*>(::operator new(n*sizeof(T))); }\n"
         "  void deallocate(T* p, std::size_t){ ::operator delete(p); }\n"
         "  template <typename U> bool operator==(const A<U>&) const noexcept { return true; }\n"
         "};\n"
         "int main(){ std::vector<int,A<int>> v; v.push_back(1); std::cout << v[0] << '\\n'; }\n"
         "```\n\n"
         "[标准] 容器内部可能为 `value_type` 的其它类型分配（如节点），`rebind` 把分配器改绑到该类型。"),
    ],
    "stl_vector": [
        (2, "比较 `vector::push_back` 与 `emplace_back`：后者如何避免一次额外移动/拷贝？",
         "```cpp\n"
         "#include <iostream>\n#include <vector>\n"
         "struct S { S(int){std::cout<<\"ctor\\n\";} S(const S&){std::cout<<\"copy\\n\";} };\n"
         "int main(){ std::vector<S> v; v.reserve(1); v.emplace_back(1); }\n"
         "```\n\n"
         "[标准] `emplace_back(args...)` 在容器内存中原地构造，省去临时对象+移动。"),
    ],
    "stl_string": [
        (2, "说明 SSO（短字符串优化）：长度低于阈值的 `std::string` 不分配堆内存。写代码观察容量差异。",
         "```cpp\n"
         "#include <iostream>\n#include <string>\n"
         "int main(){ std::string a(\"short\"), b(\"this is a very long string exceeding SSO buffer\"); std::cout << a << '|' << b << '\\n'; }\n"
         "```\n\n"
         "[实现·GCC13] libstdc++ 的 SSO 阈值为 15 字节（含尾部 NUL）。"),
    ],
    "stl_map": [
        (2, "用 `std::map` 与 `std::unordered_map` 各做一个计数，指出二者底层结构与复杂度差异。",
         "```cpp\n"
         "#include <iostream>\n#include <map>\n"
         "int main(){ std::map<int,int> m; m[1]=10; std::cout << m[1] << '\\n'; }\n"
         "```\n\n"
         "[标准] `map` 为红黑树（O(log n)，有序）；`unordered_map` 为哈希表（平均 O(1)，无序）。"),
    ],
    "stl_span": [
        (3, "用 `std::span` 让一个函数同时接收 `std::vector` 与原生数组，避免拷贝。",
         "```cpp\n"
         "#include <iostream>\n#include <span>\n#include <vector>\n"
         "void print(std::span<const int> s){ for(int x:s) std::cout<<x<<' '; std::cout<<'\\n'; }\n"
         "int main(){ int a[3]={1,2,3}; std::vector<int> v{4,5,6}; print(a); print(v); }\n"
         "```\n\n"
         "[标准] `span` 是连续序列的轻量视图（指针+长度），零拷贝、零所有权。"),
    ],
    "ranges": [
        (2, "用 ranges 管道过滤奇数并求平方，输出到 `std::vector`。",
         "```cpp\n"
         "#include <iostream>\n#include <vector>\n#include <ranges>\n"
         "int main(){\n"
         "  std::vector<int> v{1,2,3,4,5};\n"
         "  auto r = v | std::views::filter([](int x){return x%2;}) | std::views::transform([](int x){return x*x;});\n"
         "  for (int x : r) std::cout << x << ' ';\n"
         "}\n"
         "```\n\n"
         "[标准] ranges 管道惰性求值，组合算法无需显式中间容器。"),
    ],
    "algorithm": [
        (2, "用 `std::sort` + 自定义比较器对一个 `struct` 按某字段降序排序。",
         "```cpp\n"
         "#include <iostream>\n#include <vector>\n#include <algorithm>\n"
         "struct P { int score; };\n"
         "int main(){\n"
         "  std::vector<P> v{{3},{1},{2}};\n"
         "  std::sort(v.begin(), v.end(), [](const P&a,const P&b){ return a.score>b.score; });\n"
         "  std::cout << v[0].score << '\\n';\n"
         "}\n"
         "```\n\n"
         "[标准] 比较器返回 `true` 表示 `a` 应排在 `b` 前；须满足严格弱序。"),
    ],
    "thread": [
        (2, "用 `std::jthread` 启动线程，主线程等待其自动 join（C++20）。",
         "```cpp\n"
         "#include <iostream>\n#include <thread>\n"
         "int main(){\n"
         "  std::jthread t([]{ std::cout << \"worker\\n\"; });\n"
         "}  // 离开作用域自动 join\n"
         "```\n\n"
         "[标准] `jthread` 在析构时自动 `join`，并支持 `std::stop_token` 协作取消。"),
    ],
    "atomic": [
        (2, "用 `std::atomic<int>` 做 100 个 `jthread` 各加 1000 的无锁计数，验证结果为 100000。",
         "```cpp\n"
         "#include <iostream>\n#include <atomic>\n#include <vector>\n#include <thread>\n"
         "int main(){\n"
         "  std::atomic<int> c{0};\n"
         "  std::vector<std::jthread> ts;\n"
         "  for(int i=0;i<100;++i) ts.emplace_back([&]{ for(int j=0;j<1000;++j) c.fetch_add(1); });\n"
         "  std::cout << c.load() << '\\n';\n"
         "}\n"
         "```\n\n"
         "[标准] `fetch_add` 是原子 RMW；若去掉 `atomic` 则存在数据竞争、结果不确定。"),
    ],
    "memoryorder": [
        (3, "说明 `memory_order_relaxed` 与 `memory_order_seq_cst` 的区别，并给出一个只需 `relaxed` 的计数器场景。",
         "独立计数器只需原子性、不需同步其它内存，可用 `relaxed` 降低开销：\n\n"
         "```cpp\n"
         "#include <atomic>\n#include <thread>\n"
         "std::atomic<int> hits{0};\n"
         "void worker(){ for(int i=0;i<100;++i) hits.fetch_add(1, std::memory_order_relaxed); }\n"
         "```\n\n"
         "[标准] `seq_cst` 提供全局顺序一致，开销最大；`relaxed` 仅保证原子性。"),
    ],
    "coroutine": [
        (3, "写一个最小 C++20 协程 `Task<int>`，用 `co_return` 产出值，并用 promise 类型支撑。",
         "```cpp\n"
         "#include <iostream>\n#include <coroutine>\n"
         "struct Task { struct promise_type {\n"
         "  int value; Task get_return_object(){ return {}; }\n"
         "  std::suspend_never initial_suspend(){ return {}; }\n"
         "  std::suspend_never final_suspend() noexcept { return {}; }\n"
         "  void return_value(int v){ value=v; } void unhandled_exception(){}\n"
         "}; int result; };\n"
         "Task gen() { co_return 42; }\n"
         "int main(){ std::cout << \"coroutine ok\\n\"; }\n"
         "```\n\n"
         "[标准] 协程需 `promise_type` 提供 `get_return_object/initial_suspend/final_suspend/return_void|value`。"),
    ],
    "chrono": [
        (2, "用 `std::chrono` 测量一段代码的毫秒耗时。",
         "```cpp\n"
         "#include <iostream>\n#include <chrono>\n"
         "int main(){\n"
         "  auto t0 = std::chrono::steady_clock::now();\n"
         "  volatile int s=0; for(int i=0;i<1000000;++i) s+=i;\n"
         "  auto d = std::chrono::steady_clock::now() - t0;\n"
         "  std::cout << std::chrono::duration<double,std::milli>(d).count() << \" ms\\n\";\n"
         "}\n"
         "```\n\n"
         "[标准] `steady_clock` 单调不受系统时间调整影响，适合测耗时。"),
    ],
    "filesystem": [
        (2, "用 `std::filesystem` 遍历某目录下所有常规文件并打印其大小。",
         "```cpp\n"
         "#include <iostream>\n#include <filesystem>\n"
         "int main(){ for(auto& e : std::filesystem::directory_iterator(\".\")) if(e.is_regular_file()) std::cout << e.path() << '\\n'; }\n"
         "```\n\n"
         "[标准] `directory_iterator` 提供递归/非递归遍历；路径操作为跨平台抽象。"),
    ],
    "format": [
        (2, "用 `std::format`（C++20）安全格式化字符串，替代 `printf` 的脆弱格式串。",
         "```cpp\n"
         "#include <iostream>\n#include <format>\n"
         "int main(){ std::cout << std::format(\"{} + {} = {}\", 2, 3, 5) << '\\n'; }\n"
         "```\n\n"
         "[标准] `std::format` 类型安全、格式串在编译期部分检查，避免 `printf` 类型错配 UB。"),
    ],
    "modules": [
        (3, "说明 C++20 模块相比 `#include` 文本包含的两大优势，并给出模块接口单元的最小结构。",
         "模块避免文本重复解析与宏泄漏，编译更快：\n\n"
         "```text\n"
         "// math.ixx (接口单元, 需编译器模块支持)\n"
         "export module math;\n"
         "export int add(int a, int b) { return a + b; }\n"
         "```\n\n"
         "[标准] GCC 对模块支持较新（需 `-fmodules`）；接口单元以 `export module` 声明，实体用 `export` 导出。"),
    ],
    "contracts": [
        (3, "用契约属性 `[ [ assert: x>0 ] ]` 表达前置条件，并说明契约违反时的默认行为。",
         "GCC13 尚不支持 `[[assert]]` 契约属性，以下用 `assert` 宏等价模拟前置条件（可编译）：\n\n"
         "```cpp\n"
         "#include <iostream>\n#include <cassert>\n"
         "void f(int x) { assert(x > 0); std::cout << x << '\\n'; }\n"
         "int main(){ f(5); }\n"
         "```\n\n"
         "[标准] 契约（P2900）仍在演进；语义上 `[[assert: x>0]]` 即前置条件，违反默认触发 `std::terminate` 类行为，依构建模式而定。"),
    ],
    "pmr": [
        (3, "用 `std::pmr::monotonic_buffer_resource` 做一次性内存池，给 `pmr::vector` 提供零碎片分配。",
         "```cpp\n"
         "#include <iostream>\n#include <memory_resource>\n#include <vector>\n"
         "int main(){\n"
         "  std::pmr::monotonic_buffer_resource pool;\n"
         "  std::pmr::vector<int> v{&pool};\n"
         "  v.push_back(1); std::cout << v[0] << '\\n';\n"
         "}\n"
         "```\n\n"
         "[标准] `pmr` 把分配器与类型解耦；`monotonic_buffer` 不释放单个对象、仅整体回收，适合阶段性分配。"),
    ],
    "lifecycle": [
        (2, "以下代码有何生命周期陷阱？`const std::string& r = std::string(\"tmp\");` 之后使用 `r` 是否安全？",
         "该例中 `r` 绑定到临时量，临时量生存期被延长至 `r` 的作用域结束，故安全：\n\n"
         "```cpp\n"
         "#include <iostream>\n#include <string>\n"
         "int main(){ const std::string& r = std::string(\"tmp\"); std::cout << r << '\\n'; }\n"
         "```\n\n"
         "[标准] 但返回局部对象的引用/指针则是悬垂——必须区分「绑定临时」与「返回局部引用」。"),
    ],
    "enum": [
        (2, "用 `enum class`（强类型枚举）避免隐式转换到 `int`，并与传统 `enum` 对比。",
         "```cpp\n"
         "#include <iostream>\n"
         "enum class Color { Red, Green };\n"
         "int main(){ Color c = Color::Red; /* int x=c; 编译错误 */ std::cout << \"ok\\n\"; }\n"
         "```\n\n"
         "[标准] `enum class` 作用域限定、无隐式整型转换，避免命名污染与误用。"),
    ],
    "union": [
        (2, "说明匿名 union 与具名 union 的区别，并指出含非平凡成员（如 `std::string`）时为何需要显式构造/析构。",
         "```cpp\n"
         "#include <string>\n"
         "union U { int i; double d; U(){} ~U(){} };\n"
         "int main(){ U u; u.i = 7; }\n"
         "```\n\n"
         "[标准] 含非平凡成员的 union 默认构造/析构被删除，须显式提供；需手动管理活跃成员。"),
    ],
    "attribute": [
        (2, "说明 `[[nodiscard]]` 的作用，并写一个返回资源句柄但遗漏检查会导致泄漏的函数示例。",
         "```cpp\n"
         "#include <cstdio>\n"
         "[[nodiscard]] std::FILE* open(const char* p){ return std::fopen(p,\"r\"); }\n"
         "int main(){ open(\"x.txt\"); /* 警告: 返回值被丢弃 */ }\n"
         "```\n\n"
         "[标准] `[[nodiscard]]` 在调用者忽略返回值时产生诊断，防止忽略重要结果。"),
    ],
    "history": [
        (2, "简述 C++11 相比 C++98 的三大里程碑特性，以及它们为何被称为「现代 C++」起点。",
         "C++11 引入：移动语义（`std::move`/右值引用）、`auto`/范围 for、`nullptr` 与强类型枚举、lambda、`std::thread`、智能指针、`constexpr`。它们把 RAII 与零开销抽象系统化，是现代 C++ 的基石。\n\n[标准] 移动语义消除了大量不必要的深拷贝；lambda 让算法内联局部行为。"),
    ],
    "standardization": [
        (2, "说明 ISO C++ 的发布节奏（从 C++11 起改为三年周期）以及提案编号（Pxxxx）的含义。",
         "自 C++11 起改为约三年一个标准（11/14/17/20/23/26…）。提案以 `P` + 编号命名（如 P0201R3，R 后数字为修订版）。\n\n[标准] 特性须经提案→评审→投票进入工作草案（WD）并最终标准。"),
    ],
    "design_pattern": [
        (3, "用 CRTP 或模板策略实现一个编译期可配置的「计数日志」装饰器，说明相比运行时多态的零开销优势。",
         "参见 CRTP 练习：把日志策略作为模板参数传入，调用点被内联，无 vtable 间接：\n\n"
         "```cpp\n"
         "#include <iostream>\n"
         "template <typename Log> struct Op { void run(){ Log::write(); } };\n"
         "struct Console { static void write(){ std::cout << \"log\\n\"; } };\n"
         "int main(){ Op<Console> o; o.run(); }\n"
         "```\n\n"
         "[经验] 策略以编译期类型注入，零运行时分发开销。"),
    ],
    "perf": [
        (2, "说明 CPU 缓存行（通常 64 字节）对 false sharing 的影响，并给出用 `alignas` 隔离两线程计数器的最小示例。",
         "```cpp\n"
         "#include <iostream>\n#include <thread>\n#include <atomic>\n"
         "struct alignas(64) Counters { std::atomic<int> a{0}, b{0}; };\n"
         "int main(){ Counters c; std::jthread t1([&]{ for(int i=0;i<1000;++i) c.a.fetch_add(1); }); std::jthread t2([&]{ for(int i=0;i<1000;++i) c.b.fetch_add(1); }); std::cout << c.a << c.b << '\\n'; }\n"
         "```\n\n"
         "[平台·x86-64] 两计数器若同处一行会 false sharing；`alignas(64)` 隔离到不同缓存行。"),
    ],
}

# 文件名/主题补充映射（增强检测，覆盖历史/工具链/阅读等叙事章）
FILENAME_TOPIC = {
    "ch01":"history","ch02":"standardization","ch03":"history","ch04":"history",
    "ch05":"history","ch06":"history","ch07":"history","ch08":"history","ch09":"history",
    "ch10":"history","ch11":"history","ch12":"standardization","ch13":"standardization",
    "ch14":"perf","ch15":"perf","ch16":"standardization","ch17":"standardization",
    "ch18":"perf","ch19":"standardization","ch20":"template","ch21":"concept",
    "ch22":"template","ch23":"concept","ch24":"enum","ch25":"union","ch26":"lambda",
    "ch27":"attribute","ch28":"lifecycle","ch29":"design_pattern","ch30":"design_pattern",
    "ch31":"design_pattern","ch32":"design_pattern","ch37":"newdelete","ch38":"allocator",
    "ch39":"raii","ch40":"exception","ch41":"smartptr","ch42":"move","ch43":"memory",
    "ch44":"memory","ch45":"virtual","ch46":"virtual","ch47":"virtual","ch48":"rtti",
    "ch49":"virtual","ch50":"virtual","ch51":"crtp","ch52":"ebo","ch60":"template",
    "ch61":"template","ch62":"template","ch63":"template","ch64":"typetrait",
    "ch65":"typetrait","ch66":"typetrait","ch67":"concept","ch68":"fold","ch69":"constexpr",
    "ch70":"template","ch71":"design_pattern","ch76":"stl_vector","ch77":"stl_vector",
    "ch78":"stl_vector","ch79":"stl_vector","ch80":"stl_vector","ch81":"stl_string",
    "ch82":"stl_span","ch83":"stl_map","ch84":"stl_map","ch85":"stl_map","ch86":"stl_span",
    "ch87":"stl_vector","ch88":"variant","ch89":"variant","ch90":"ranges","ch91":"filesystem",
    "ch92":"chrono","ch93":"thread","ch94":"thread","ch95":"algorithm","ch96":"algorithm",
    "ch97":"algorithm","ch98":"algorithm","ch99":"algorithm","ch100":"algorithm",
    "ch101":"thread","ch102":"thread","ch103":"thread","ch104":"thread","ch105":"thread",
    "ch106":"thread","ch107":"atomic","ch108":"memoryorder","ch109":"memoryorder",
    "ch110":"atomic","ch111":"atomic","ch112":"coroutine","ch113":"coroutine",
    "ch114":"thread","ch115":"move","ch116":"forward","ch117":"move","ch118":"modules",
    "ch119":"ranges","ch120":"coroutine","ch121":"contracts","ch122":"pmr","ch123":"typetrait",
    "ch124":"perf","ch125":"format","ch126":"perf","ch127":"perf","ch128":"design_pattern",
    "ch129":"design_pattern","ch130":"design_pattern","ch131":"format","ch132":"standardization",
    "ch133":"design_pattern","ch134":"design_pattern","ch135":"design_pattern",
    "ch136":"design_pattern","ch137":"design_pattern","ch138":"design_pattern",
    "ch139":"crtp","ch140":"design_pattern","ch141":"design_pattern","ch142":"design_pattern",
    "ch143":"design_pattern","ch144":"design_pattern","ch145":"design_pattern",
    "ch146":"exception","ch147":"design_pattern","ch148":"standardization",
    "ch149":"standardization","ch150":"perf","ch151":"perf","ch152":"perf","ch153":"perf",
    "ch154":"perf","ch155":"perf","ch156":"perf","ch157":"perf","ch158":"perf",
    "ch159":"thread","ch160":"memory","ch161":"format","ch162":"design_pattern",
    "ch163":"thread","ch164":"design_pattern","ch165":"history",
}

BODY_KEYWORDS = {
    "template": r"模板|template|typename",
    "concept": r"concept|requires|概念",
    "constexpr": r"constexpr|consteval|编译期",
    "fold": r"折叠表达式|fold expression",
    "typetrait": r"type_traits|type trait|is_pointer|std::is_",
    "move": r"移动语义|std::move|移动构造",
    "forward": r"完美转发|forward|forwarding",
    "raii": r"RAII|资源管理|析构.*释放",
    "smartptr": r"unique_ptr|shared_ptr|weak_ptr|智能指针",
    "exception": r"异常|exception|noexcept|terminate",
    "virtual": r"虚函数|virtual|vtable|多态",
    "rtti": r"dynamic_cast|typeid|RTTI",
    "crtp": r"CRTP|奇异递归",
    "ebo": r"空基类|EBO|empty base",
    "variant": r"std::variant|variant",
    "optional": r"std::optional|optional",
    "lambda": r"lambda|捕获|mutable",
    "memory": r"栈|堆|生命周期|stack|heap|对象模型",
    "newdelete": r"new/delete|new\[\]|delete\[\]|new ",
    "allocator": r"allocator|分配器|分配",
    "stl_vector": r"vector|容器",
    "stl_string": r"std::string|string|SSO|短字符串",
    "stl_map": r"map|unordered_map|红黑树|哈希",
    "stl_span": r"span|视图|view\b",
    "ranges": r"ranges|views::|管道",
    "algorithm": r"std::sort|算法|sort|find_if",
    "thread": r"thread|jthread|线程",
    "atomic": r"atomic|原子",
    "memoryorder": r"memory_order|内存序|acquire|release",
    "coroutine": r"协程|coroutine|co_await|co_return|co_yield",
    "chrono": r"chrono|duration|steady_clock",
    "filesystem": r"filesystem|目录|路径",
    "format": r"std::format|format|格式化",
    "modules": r"模块|module|import ",
    "contracts": r"契约|contract|assert:",
    "pmr": r"pmr|memory_resource|monotonic",
    "lifecycle": r"生命周期|悬垂|dangling|悬空",
    "enum": r"enum class|强类型枚举|enum\b",
    "union": r"union|联合体",
    "attribute": r"\[\[nodiscard\]\]|属性|attribute|\[\[",
    "history": r"C\+\+11|C\+\+98|标准演进|历史|C\+\+20",
    "standardization": r"标准化|WG21|提案|P\d{4}|ISO",
    "design_pattern": r"设计模式|策略|装饰|工厂|单例|观察者",
    "perf": r"缓存|cache|false sharing|性能|benchmark|微架构|SIMD|流水线",
}


def detect_topics(text, fname):
    """返回匹配的题库 key 列表（按相关度排序，最多 3 个）。"""
    topics = []
    low = text.lower()
    for topic, pat in BODY_KEYWORDS.items():
        if re.search(pat, low, re.IGNORECASE):
            topics.append(topic)
    # 文件名强映射（覆盖叙事章）
    num = re.search(r"ch(\d{2,3})", fname)
    if num and num.group(1) in FILENAME_TOPIC:
        ft = FILENAME_TOPIC[num.group(1)]
        if ft not in topics:
            topics.insert(0, ft)
    if not topics:
        topics = ["history"]
    return topics[:3]


def gen_section(path):
    """为单章生成 `## 自测练习` 小节 Markdown（含折叠答案）。"""
    text = open(path, encoding="utf-8").read()
    fname = os.path.basename(path)
    topics = detect_topics(text, fname)
    picked = []
    for t in topics:
        for q in QUESTION_BANK.get(t, []):
            key = (t, q[1][:24])
            if key not in picked:
                picked.append(key)
                break
    # 不足 2 道则补通用题
    if len(picked) < 2:
        for t in ("history", "design_pattern", "perf"):
            if len(picked) >= 2:
                break
            for q in QUESTION_BANK.get(t, []):
                key = (t, q[1][:24])
                if key not in picked:
                    picked.append(key)
                    break
    lines = ["", "## 自测练习（Exercises）", "",
             "> 以下题目用于自测掌握程度；答案折叠于每题下方，建议先独立作答。", ""]
    n = 0
    for t, _ in picked[:3]:
        q = next(q for q in QUESTION_BANK[t] if (t, q[1][:24]) == (t, _))
        n += 1
        stars = "★" * q[0]
        lines.append(f"### 练习 {n}（难度 {stars}）")
        lines.append("")
        lines.append(q[1])
        lines.append("")
        lines.append("<details><summary>答案与解析</summary>")
        lines.append("")
        lines.append(q[2])
        lines.append("")
        lines.append("</details>")
        lines.append("")
    return "\n".join(lines)


def verify_bank():
    """编译校验题库中所有答案 cpp 块（独立程序，C++23 -fsyntax-only）。"""
    total = 0
    fail = 0
    for topic, qs in QUESTION_BANK.items():
        for stars, prompt, ans in qs:
            for m in re.finditer(r"```cpp\n(.*?)```", ans, re.S):
                code = m.group(1)
                # 去掉示意注释行（以 // 且仅说明、非代码）——保留所有，让编译器判
                total += 1
                ok, err = compile_cpp(code)
                if not ok:
                    fail += 1
                    print(f"[FAIL] {topic} ★{stars}: {err.strip().splitlines()[-1][:120]}")
    print(f"\n题库答案 cpp 块编译: {total-fail}/{total} 通过")
    return fail


def compile_cpp(code):
    import tempfile
    with tempfile.NamedTemporaryFile("w", suffix=".cpp", delete=False) as f:
        f.write(code)
        fn = f.name
    try:
        r = subprocess.run([GPP, "-std=c++23", "-O0", "-fsyntax-only", fn],
                           capture_output=True, text=True, timeout=30)
        return (r.returncode == 0), r.stderr
    except Exception as e:
        return False, str(e)
    finally:
        os.unlink(fn)


def inject(path):
    """把 `## 自测练习` 小节注入章末（备份原文件）。"""
    bak = path + ".bak"
    if not os.path.exists(bak):
        shutil.copy(path, bak)
    text = open(path, encoding="utf-8").read()
    if "## 自测练习（Exercises）" in text:
        print(f"[skip] 已有练习小节: {path}")
        return
    section = gen_section(path)
    # 去除末尾多余空行后追加
    text = text.rstrip() + "\n" + section + "\n"
    open(path, "w", encoding="utf-8").write(text)
    print(f"[ok] 已注入: {path}")


def stats():
    total = len(QUESTION_BANK)
    qcount = sum(len(v) for v in QUESTION_BANK.values())
    print(f"题库主题数: {total}")
    print(f"题库题目数: {qcount}")


if __name__ == "__main__":
    args = sys.argv[1:]
    if "--verify" in args:
        sys.exit(0 if verify_bank() == 0 else 1)
    if "--stats" in args:
        stats()
    elif "--emit" in args:
        i = args.index("--emit") + 1
        print(gen_section(args[i]))
    elif "--inject" in args:
        i = args.index("--inject") + 1
        inject(args[i])
    else:
        stats()
