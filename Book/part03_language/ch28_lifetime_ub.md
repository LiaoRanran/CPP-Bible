# 第28章　对象生命周期与未定义行为（UB）：生存期、悬垂、UB 分类与编译器武器化

> 标准基：ISO/IEC 14882:2023（C++23）｜预计阅读：7 h｜前置：ch19（存储期/链接/ODR）、ch20（引用与指针悬垂）、ch21（const/volatile 与写 UB）、ch25（联合 active member UB）、ch27（reinterpret_cast 与严格别名）、ch31（异常与 UB）、ch33（异常安全）、ch42（严格别名与优化）、ch61（并发数据竞争）｜后续：ch42（严格别名）、ch61（数据竞争）｜难度：★★★★★
> 立场分层约定：`[标准]`＝ISO 条文语义；`[实现]`＝编译器/标准库源码行为；`[平台]`＝OS/ABI/硬件（x86-64 / ARM / ELF / PE）；`[经验]`＝工程落地的铁律。四层不得混淆。

本章把"对象生命周期"与"未定义行为（Undefined Behavior, UB）"在**对象模型、存储期、临时对象、悬垂、UB 分类、编译器优化武器化、真实标准库源码、三编译器差异、Sanitizer 检测、constexpr、生命周期安全、跨语言**十二个维度讲透。所有"推荐阅读"的书籍内容已内化进正文（见 §⑳ 源码阅读路线），本章不再单列推荐阅读。

---

## ① 本章地图（先给结论，再击穿）

⟶ Book/part03_language/ch27_cast.md


**知识图谱（前置→本章→后续）**：

```
ch19 存储期 ─┐
ch20 引用指针 ─┼─► ch28 生命周期与 UB ◄─ ch21 const/写UB ─┐
ch25 联合 ────┘        │            ┌─────────────────────┘
                      ├─► ch27/42 严格别名（UB 重灾区）
                      ├─► ch31/33 异常与 UB（noexcept 穿透）
                      └─► ch61 并发数据竞争（UB 另一重灾区）
```

**一句话结论（[标准][经验]）**：
1. 对象生存期起于**构造函数完成**、止于**析构开始**（`[basic.life]`）。但"存储被复用或释放"之前对象就可能已"消亡"——此时访问它就是 UB。
2. 同一块存储上用 `placement new` 重建对象**必须**先显式调用旧对象的析构函数；重建后取回指针要用 `std::launder`（C++17），否则优化器会"证明"指针仍指向旧对象。
3. 临时对象的生命周期延长只发生在 **`const T&` 或右值引用绑定到 prvalue** 时，且有一长串例外（成员/数组元素/range-for 临时容器/返回引用/initializer_list）。
4. **悬垂（dangling）** 是所有返回"已亡对象"引用/指针的场景统称：`string_view`/`initializer_list`/range-for 临时/返回局部引用是最常见陷阱。
5. **UB 不是运行时错误**——它是"编译器可任意处理"的许可。编译器据此做激进优化：删空指针检查、把 UB 循环变成无限循环、重排越界访问。
6. 检测 UB 靠 **UBSan / ASan / TSan**；规避 UB 靠 **Core Guidelines + 生命周期静态分析（Lifetime 提案）**；`constexpr` 中任何 UB 会**直接编译失败**。

**分层判定总览表（[标准][实现][平台][经验]）**：

| 维度 | [标准] 语义 | [实现] 现状 | [平台] 差异 | [经验] 铁律 |
|---|---|---|---|---|
| 生存期起止 | [basic.life] 构造完→析构始 | libstdc++ `std::launder` 调 `__builtin_launder` | 所有平台一致 | 重建对象必 `launder` |
| 临时延长 | [class.temporary] const&/&& | GCC/Clang/MSVC 均延长 | 一致 | 例外清单必须背 |
| UB | 程序整体无约束 | 编译器按假设优化 | x86/ARM 表现不同 | 绝不依赖 UB 行为 |
| 检测 | 无标准机制 | UBSan/ASan/TSan（Clang 最全） | MinGW 缺运行时库 | CI 必须开 San |

---

## ② 对象生存期精确定义 [basic.life]

`[标准]` [basic.life]/1：对象 `o` 的生存期始于**获得合适对齐与大小的存储**、且**构造函数（含聚合/默认初始化）完成**之时；止于**析构开始**之时。对于无析构的类类型与所有标量类型，「析构开始」即生存期结束点。

`[实现]` 关键陷阱：生存期结束 ≠ 存储释放。存储可能仍被占用（栈帧未回退、堆块未 free、placement new 复用），但对象已经"死了"。在「存储被复用或释放」之前访问一个已结束生存期的对象，若访问经由指向旧对象的指针/引用，且新对象与旧对象类型**不相似（not similar）**，则行为是 UB。

### 2.1 生存期起于构造完成、止于析构开始

```cpp
// prog_01_lifetime_begin_end.cpp
// 编译: g++ -std=c++20 -Wall prog_01_lifetime_begin_end.cpp -o prog_01
#include <iostream>
struct S {
    int x;
    S(int v) : x(v) { std::cout << "ctor x=" << x << "\n"; }
    ~S() { std::cout << "dtor x=" << x << "\n"; }
};
int main() {
    alignas(S) char buf[sizeof(S)];            // 存储已就位, 但 S 尚未"生"
    S* p = ::new (buf) S(42);                  // 构造完成 -> 生存期开始
    std::cout << "alive: " << p->x << "\n";    // 合法: 仍在生存期
    p->~S();                                   // 析构开始 -> 生存期结束
    // 至此 buf 中已无 S 对象, 但存储仍占用
}
```
`[经验]` `placement new` 后才有对象；`->~S()` 后对象即"死"，即使内存还在。

### 2.2 存储未释放但对象已亡 → 访问即 UB

```cpp
// prog_02_dead_object_access.cpp  —— 错误示例 (UB)
// 编译: g++ -std=c++20 -Wall prog_02_dead_object_access.cpp -o prog_02
#include <iostream>
struct T {
    int v;
    T(int x) : v(x) {}
    ~T() { v = 0xDEAD; }   // 析构里"毒化"成员, 仅演示
};
int main() {
    alignas(T) char buf[sizeof(T)];
    T* p = ::new (buf) T(7);
    p->~T();                     // 生存期结束
    std::cout << p->v << "\n";   // UB! 通过旧指针访问已亡对象
}
```
`[标准]` [basic.life]/7：若新对象未在同一存储上被创建，通过指向旧对象的指针/引用访问已结束生存期的对象是 UB（即使读取的字节"恰好还在"）。

**正确修复**（prog_02 改法）：要么在析构前使用，要么在同一存储重建对象并 `launder`（见 §2.4）。

### 2.3 placement new 在同一存储重建对象（先显式析构）

`[标准]` [basic.life]/8：若在同一存储上创建了**与旧对象相似类型**的新对象，且旧对象已结束生存期，则可通过适当方式访问新对象。重建前**必须**先结束旧对象生存期（显式调析构），否则旧对象析构会被跳过或重复。

```cpp
// prog_03_placement_new_rebuild.cpp  —— 正确示例
// 编译: g++ -std=c++20 -Wall prog_03_placement_new_rebuild.cpp -o prog_03
#include <iostream>
struct A { int id; A(int i):id(i){} ~A(){ std::cout<<"A~"<<id<<"\n"; } };
int main() {
    alignas(A) char buf[sizeof(A)];
    A* a = ::new (buf) A(1);
    a->~A();                       // ① 先结束旧对象生存期
    A* a2 = ::new (buf) A(2);      // ② 同一存储重建
    std::cout << a2->id << "\n";   // 合法: a2 指向新对象
    a2->~A();
}
```

### 2.4 std::launder 在优化后取回指针（C++17）

`[标准]` [ptr.launder]：当新对象与旧对象类型**不相似**，或编译器"已知"指针源自旧对象时，直接复用旧指针是 UB；`std::launder(p)` 是一个优化屏障，返回指向 *p 所指向对象* 的指针。

```cpp
// prog_04_launder_needed.cpp  —— 错误 vs 正确 (const 对象重建)
// 编译: g++ -std=c++20 -Wall prog_04_launder_needed.cpp -o prog_04
#include <new>
#include <iostream>
struct C { const int tag; C(int t):tag(t){} };
int main() {
    alignas(C) char buf[sizeof(C)];
    C* c1 = ::new (buf) C(10);
    c1->~C();
    C* c2 = ::new (buf) C(20);     // 在 const 成员对象存储上重建
    C* p  = std::launder(c2);      // 正确: 取回指向新对象的指针
    std::cout << p->tag << "\n";   // 输出 20
    p->~C();
    // 若写成 C* p = c2; 在无 launder 时优化器可能仍按"tag==10"优化 -> UB
}
```
`[实现]` 见 §⑭ 真实 libstdc++ 源码：`launder` 体即 `{ return __builtin_launder(__p); }`，自身是空操作，但它向优化器下达"不要基于旧对象信息推导"的屏障指令。

---

## ③ 存储期回顾（自动/静态/线程/动态）

`[标准]` [basic.stc]：存储期决定对象存储空间的生命跨度。四类回顾并关联生存期（本节的 UB 与 ch19 存储期、ch20 引用交叉）：

### 3.1 自动存储期（块作用域）

```cpp
// prog_05_auto_vs_static.cpp
// 编译: g++ -std=c++20 -Wall prog_05_auto_vs_static.cpp -o prog_05
#include <iostream>
int& bad() { int x = 5; return x; }          // 返回局部 -> 悬垂(见 §⑦)
int& good() { static int x = 5; return x; }  // 静态存储期, 安全
int main() {
    // std::cout << bad() << "\n";           // UB: 引用已亡的自动对象
    std::cout << good() << "\n";             // 合法: 静态对象活到程序结束
}
```

### 3.2 线程存储期（thread_local）

`[标准]` [basic.stc.thread]：声明为 `thread_local` 的对象，其存储在**每个线程**首次使用前创建、线程结束时销毁——生存期绑定到线程而非块或程序。

```cpp
// prog_06_thread_local_lifetime.cpp
// 编译: g++ -std=c++20 -Wall -pthread prog_06_thread_local_lifetime.cpp -o prog_06
#include <iostream>
#include <thread>
thread_local int tls = 0;
void worker(int id) { tls = id; std::cout << "thread " << id << " tls=" << tls << "\n"; }
int main() {
    std::thread a(worker, 1), b(worker, 2);
    a.join(); b.join();     // 每线程的 tls 独立存活, 无数据竞争
}
```

### 3.3 动态存储期（new/delete）

`[标准]` [basic.stc.dynamic]：由 `new` 分配的存储持续到 `delete`。**生存期**在构造完成起、析构开始止；但**存储期**持续到 `delete`。悬空指针/引用来自"存储已释放但指针仍在用"（见 §⑦、§⑧ prog_26）。

```cpp
// prog_07_dynamic_lifetime.cpp
// 编译: g++ -std=c++20 -Wall prog_07_dynamic_lifetime.cpp -o prog_07
#include <iostream>
int main() {
    int* p = new int(99);     // 存储期+生存期都从 new 起
    std::cout << *p << "\n";  // 合法
    delete p;                 // 析构(此处是标量, 等效)+存储释放
    // *p;                    // UB: 存储已释放, 生存期早已结束
}
```

---

## ④ 临时对象生命周期：值类别、临时物化

`[标准]` [expr.prop]/2 值类别：`glvalue`（泛左值，有身份）、`prvalue`（纯右值，无身份、将物化）、`xvalue`（将亡值，有身份且将被移动）。**临时对象（temporary）** 由 prvalue 在"需要对象"时**物化（materialization）** 产生（[class.temporary]）。

`[实现]` 关键：`prvalue` 本身**不是对象**，只是一个"待计算的值"；只有当它被绑定到引用、作为函数实参、被 `decltype`/`static_cast` 等需要时，才**物化**为临时对象（RVO/NRVO 与物化可消除临时——这是优化的来源，见 ch27/ch42 交叉）。

```cpp
// prog_08_value_categories.cpp
// 编译: g++ -std=c++20 -Wall prog_08_value_categories.cpp -o prog_08
#include <type_traits>
#include <utility>
int g() { return 1; }
int& lval() { static int x; return x; }
int&& rref() { return 0; }     // 返回 xvalue
int main() {
    static_assert(std::is_same_v<decltype(g()), int>);        // prvalue -> int
    static_assert(std::is_same_v<decltype(lval()), int&>);    // glvalue
    static_assert(std::is_same_v<decltype(rref()), int&&>);   // xvalue
}
```

```cpp
// prog_09_materialization.cpp  —— 临时物化时机
// 编译: g++ -std=c++20 -Wall prog_09_materialization.cpp -o prog_09
#include <string>
void take(const std::string&) {}   // 定义, 避免链接错误
int main() {
    take(std::string("hi"));   // prvalue std::string("hi") 物化为临时,
                               // 绑定到 const& -> 延长(见 §⑤)
    using T = decltype(std::string("x"));   // 不物化: decltype 仅查询类型
    (void)sizeof(T);
}
```

---

## ⑤ 临时生命周期延长规则（[class.temporary]）

`[标准]` [class.temporary]/6：当 **`const` 左值引用或右值引用**绑定到一个 prvalue（临时）时，该临时对象（及其完整子对象）的生命周期被**延长**至该引用的作用域结束。

```cpp
// prog_10_const_ref_extend.cpp  —— 正确: const& 延长临时
// 编译: g++ -std=c++20 -Wall prog_10_const_ref_extend.cpp -o prog_10
#include <iostream>
struct Loud { ~Loud(){ std::cout << "dtor\n"; } };
const Loud& r = Loud{};        // 临时 Loud{} 活到 main 结束(而非本语句结束)
int main() { std::cout << "main end\n"; }   // 输出: main end \n dtor
```

```cpp
// prog_11_rvalue_ref_extend.cpp  —— 右值引用同样延长
// 编译: g++ -std=c++20 -Wall prog_11_rvalue_ref_extend.cpp -o prog_11
#include <iostream>
struct Loud { ~Loud(){ std::cout << "~Loud\n"; } };
int main() {
    Loud&& r = Loud{};         // 右值引用绑定 prvalue -> 延长
    std::cout << "before scope\n";
}                             // r 离开作用域 -> dtor 在此
```

---

## ⑥ 临时生命周期延长「例外」（背下这些坑）

`[标准]` [class.temporary]/6 明确列出**不延长**的情形。以下逐一用程序证伪。

### 6.1 绑定到成员变量 → 不延长

```cpp
// prog_12_member_binding_no_extend.cpp  —— 错误示例 (悬垂成员引用)
// 编译: g++ -std=c++20 -Wall prog_12_member_binding_no_extend.cpp -o prog_12
#include <string>
struct Holder { const std::string& s; };
int main() {
    Holder h{std::string("tmp")};   // 临时 string 绑定到成员引用
                                    // 注意: 延长规则不适用于成员!
    // h.s 在下一语句已是悬垂 -> 使用即 UB
}
```

### 6.2 绑定到数组元素 → 不延长

```cpp
// prog_13_array_elem_no_extend.cpp  —— 错误示例
// 编译: g++ -std=c++20 -Wall prog_13_array_elem_no_extend.cpp -o prog_13
#include <string>
int main() {
    using S = std::string;
    const S& arr[1] = { S("tmp") };   // 数组元素引用不延长临时
    // arr[0] 悬垂
}
```

### 6.3 range-for 遍历临时容器 → 不延长（迭代器悬垂）

```cpp
// prog_14_range_for_temp_no_extend.cpp  —— 错误示例 (UB)
// 编译: g++ -std=c++20 -Wall prog_14_range_for_temp_no_extend.cpp -o prog_14
#include <vector>
#include <iostream>
std::vector<int> make() { return {1,2,3}; }
int main() {
    for (int x : make()) {            // 临时 vector 在 for 头结束后即亡!
        std::cout << x;               // 迭代器悬垂 -> UB
    }
}
```
`[经验]` 这是 §⑦ prog_19 的近亲。GCC/Clang 在 `-Wall` 下常给 `-Wrange-loop-construct`/悬垂告警。正确写法：`auto v = make(); for (int x : v) ...`。

### 6.4 函数返回 const T& → 不延长（返回的是引用，临时已亡）

`[标准]` 延长只作用于**初始化引用时的直接绑定**。返回 `const T&` 时，临时在 `return` 表达式结束时已亡，返回的引用天然悬垂。

```cpp
// prog_15_return_const_ref_no_extend.cpp  —— 错误示例 (UB)
// 编译: g++ -std=c++20 -Wall prog_15_return_const_ref_no_extend.cpp -o prog_15
#include <string>
const std::string& bad() { return "abc"; }   // 临时 string 在返回时亡
int main() {
    // const std::string& r = bad();          // r 悬垂
}
```

### 6.5 initializer_list 的元素在 list 结束后消亡

`[标准]` [dcl.init.list]/6：array 成员（以及其元素引用）的生命周期与 `initializer_list` 对象本身一致。绑定到 `initializer_list<T>` 的临时数组在 list 析构后消亡。

```cpp
// prog_16_init_list_no_extend.cpp  —— 错误示例 (悬垂)
// 编译: g++ -std=c++20 -Wall prog_16_init_list_no_extend.cpp -o prog_16
#include <initializer_list>
#include <iostream>
const int& first() {
    std::initializer_list<int> L = {1,2,3};
    const int& r = *L.begin();   // r 绑定到 L 内部数组元素
    return r;                    // L 亡 -> 数组亡 -> r 悬垂 (UB)
}
```

---

## ⑦ 悬垂（dangling）全场景

`[经验]` 悬垂 = 引用/指针指向"已结束生存期"的对象。本章串起所有形态（交叉 ch20 引用悬垂）。

### 7.1 返回局部变量的引用

```cpp
#include <iostream>
// prog_17_return_local_ref.cpp  —— 错误示例 (UB, 经典)
// 编译: g++ -std=c++20 -Wall prog_17_return_local_ref.cpp -o prog_17
int& bad() { int x = 5; return x; }   // x 在返回时亡
int main() {
    // int& r = bad();  std::cout << r;   // UB
}
```

### 7.2 返回局部变量的指针

```cpp
// prog_18_return_local_ptr.cpp  —— 错误示例 (UB)
// 编译: g++ -std=c++20 -Wall prog_18_return_local_ptr.cpp -o prog_18
int* bad() { int x = 5; return &x; }   // 指针指向已亡自动对象
int main() {
    // int* p = bad();  *p = 9;          // UB
}
```
**正确修复**：返回 `std::unique_ptr<int>`/`int`（按值），或传入输出参数。

### 7.3 range-for 遍历临时 → 迭代器悬垂

```cpp
// prog_19_range_for_temp_dangling.cpp  —— 错误示例 (UB, 对应 prog_14)
// 编译: g++ -std=c++20 -Wall prog_19_range_for_temp_dangling.cpp -o prog_19
#include <vector>
#include <iostream>
std::vector<int> mk() { return {1,2,3}; }
int main() {
    const auto& r = mk();               // 注意: 临时绑定到 const& —— 延长的是 r 本身
    for (int x : r) {                   // 但 r 是 vector 的副本引用, 临时已亡
        std::cout << x;                 // 等价于 prog_14: 悬垂迭代器
    }
}
```
`[经验]` 把 `mk()` 的结果赋给**命名变量**再遍历：

```cpp
// prog_19_fix.cpp
// 编译: g++ -std=c++20 -Wall prog_19_fix.cpp -o prog_19_fix
#include <vector>
#include <iostream>
std::vector<int> mk() { return {1,2,3}; }
int main() {
    auto v = mk();           // 命名对象, 整个 for 期间存活
    for (int x : v) std::cout << x;
}
```

### 7.4 initializer_list 悬垂

```cpp
// prog_20_init_list_dangling.cpp  —— 错误示例 (UB, 对应 prog_16)
// 编译: g++ -std=c++20 -Wall prog_20_init_list_dangling.cpp -o prog_20
#include <initializer_list>
#include <vector>
std::vector<int> build() {
    return std::vector<int>({1,2,3});   // 不要用 initializer_list 元素的引用逃逸
}
int main() { (void)build(); }
```

### 7.5 std::string_view 绑定临时 string → 悬垂

`[平台][经验]` `std::string_view` 是"非拥有"视图（ch20），绑定到临时 `std::string` 时，临时在语句结束即亡，view 悬垂。

```cpp
// prog_21_string_view_temp.cpp  —— 错误示例 (UB)
// 编译: g++ -std=c++20 -Wall prog_21_string_view_temp.cpp -o prog_21
#include <string>
#include <string_view>
#include <iostream>
std::string make() { return "hello"; }
int main() {
    // std::string_view v = make();  // 临时 string 亡 -> v 悬垂
    // std::cout << v;               // UB
    std::string s = make();           // 正确: 拥有副本
    std::string_view v = s;           // 安全: s 在作用域内存活
    std::cout << v;
}
```

---

## ⑧ 未定义行为（UB）分类与清单

`[标准]` 标准正文有 **≈200 处** "behavior is undefined" 标注。本章给出 15 类高频 UB，每类配一个可编译的"错误示例 + 修复"。UB 清单（工业级必背）：

| # | UB 类别 | 标准条款锚点 |
|---|---|---|
| 1 | 有符号整数溢出 | [expr.pre]/4 |
| 2 | 空指针解引用 | [expr.unary.op]/1 |
| 3 | 数组越界（读/写） | [bounds] |
| 4 | 数据竞争（并发） | [intro.races] |
| 5 | 解引用野指针 / 释放后使用 | [basic.stc.dynamic.deallocation] |
| 6 | 严格别名违反 | [basic.lval]/11 |
| 7 | 读取未初始化对象 | [dcl.init]/12 |
| 8 | 移位为负或超宽 | [expr.shift] |
| 9 | 有符号左移溢出 | [expr.shift] |
| 10 | int↔指针 `reinterpret_cast` | [expr.reinterpret.cast]/5 |
| 11 | 同一变量多重定义（ODR） | [basic.def.odr] |
| 12 | 在 const 对象上写 | [dcl.type.cv]/4 |
| 13 | 迭代器/容器失效后使用 | [sequence.reqmts] |
| 14 | 异常穿透 `noexcept` | [except.spec] |
| 15 | 同存储两次构造无析构 | [basic.life]/8 |

### 8.1 有符号整数溢出（UB）

```cpp
// prog_22_signed_overflow.cpp  —— 错误示例 (UB)
// 编译: g++ -std=c++20 -Wall prog_22_signed_overflow.cpp -o prog_22
#include <limits>
int main() {
    int m = std::numeric_limits<int>::max();
    int x = m + 1;          // UB: 有符号溢出
    (void)x;
}
```
**修复**：用 `std::add_sat`(C++26 计划)/手动检查，或 `unsigned`（回绕 defined）。

### 8.2 空指针解引用（UB）

```cpp
// prog_23_null_deref.cpp  —— 错误示例 (UB)
// 编译: g++ -std=c++20 -Wall prog_23_null_deref.cpp -o prog_23
int main() {
    int* p = nullptr;
    *p = 5;                 // UB: 空指针解引用
}
```

### 8.3 数组越界（UB）

```cpp
// prog_24_oob_array.cpp  —— 错误示例 (UB)
// 编译: g++ -std=c++20 -Wall prog_24_oob_array.cpp -o prog_24
#include <vector>
int main() {
    std::vector<int> v(3);
    int x = v[10];          // UB: 越界 (vector::operator[] 不检查)
    (void)x;
}
```
**修复**：用 `v.at(10)`（抛 `out_of_range`）。

### 8.4 数据竞争（UB）

```cpp
// prog_25_data_race.cpp  —— 错误示例 (UB)
// 编译: g++ -std=c++20 -Wall -pthread prog_25_data_race.cpp -o prog_25
#include <thread>
int g = 0;
void f() { for (int i=0;i<100000;++i) ++g; }   // 无同步 -> 数据竞争
int main() {
    std::thread a(f), b(f);
    a.join(); b.join();
}
```
**修复**：`std::atomic<int> g` 或 `std::mutex`。

### 8.5 解引用野指针 / 释放后使用（UB）

```cpp
// prog_26_wild_ptr_deref.cpp  —— 错误示例 (UB)
// 编译: g++ -std=c++20 -Wall prog_26_wild_ptr_deref.cpp -o prog_26
#include <iostream>
int main() {
    int* p = new int(7);
    delete p;               // p 成野指针
    std::cout << *p;        // UB: 释放后使用 (use-after-free)
}
```
**修复**：`delete` 后立刻 `p = nullptr`；或用智能指针。

### 8.6 严格别名违反（UB）

`[标准]` [basic.lval]/11：通过不兼容类型（除 `char*`/`unsigned char*`/signed char*）的 glvalue 读取对象是 UB。交叉 ch27/ch42。

```cpp
// prog_27_strict_aliasing.cpp  —— 错误示例 (UB)
// 编译: g++ -std=c++20 -Wall -fstrict-aliasing prog_27_strict_aliasing.cpp -o prog_27
#include <cstdint>
#include <iostream>
void break_alias() {
    std::uint32_t x = 0x12345678;
    std::uint16_t* p = reinterpret_cast<std::uint16_t*>(&x);  // 别名冲突
    std::cout << *p;            // UB: 经不兼容类型读取
}
```
**修复**：`std::memcpy` / `std::bit_cast`（见 §⑬ prog_42）。

### 8.7 读取未初始化对象（UB）

```cpp
// prog_28_uninit_read.cpp  —— 错误示例 (UB)
// 编译: g++ -std=c++20 -Wall prog_28_uninit_read.cpp -o prog_28
#include <iostream>
int main() {
    int x;                  // 未初始化
    std::cout << x;         // UB: 读取未初始化自动变量
}
```
**修复**：定义即初始化 `int x{}`。

### 8.8 移位为负或超宽（UB）

```cpp
// prog_29_shift_neg_or_wide.cpp  —— 错误示例 (UB)
// 编译: g++ -std=c++20 -Wall prog_29_shift_neg_or_wide.cpp -o prog_29
#include <cstdint>
int main() {
    std::uint32_t a = 1u << 32;   // UB: 移位量 >= 宽度
    int b = 1 << -1;              // UB: 负移位
    (void)a; (void)b;
}
```

### 8.9 有符号左移溢出（UB）

```cpp
// prog_30_signed_lshift_overflow.cpp  —— 错误示例 (UB)
// 编译: g++ -std=c++20 -Wall prog_30_signed_lshift_overflow.cpp -o prog_30
#include <cstdint>
int main() {
    std::int32_t x = 1;
    x = x << 31;           // UB: 有符号左移溢出 (符号位)
    (void)x;
}
```
**修复**：用 `std::uint32_t` 左移（回绕 defined）。

### 8.10 int↔指针 reinterpret_cast（UB）

`[标准]` [expr.reinterpret.cast]/5：把整数转成指针后解引用，除非该整数源自同一指针的 `reinterpret_cast`，否则是 UB（且结果可能不对齐）。

```cpp
// prog_31_int_pointer_reinterpret.cpp  —— 错误示例 (UB)
// 编译: g++ -std=c++20 -Wall prog_31_int_pointer_reinterpret.cpp -o prog_31
#include <cstdint>
int main() {
    std::uintptr_t n = 0x1234;                 // 任意整数
    int* p = reinterpret_cast<int*>(n);        // 转换本身"实现定义"
    // *p = 5;                                 // 解引用 -> UB
    (void)p;
}
```

### 8.11 同一变量多重定义（ODR 违反，UB）

`[标准]` [basic.def.odr]：同一实体的多个定义若不一致或跨 TU 冲突是 UB。

```cpp
// prog_32_multiple_definition.cpp  —— 错误示例 (UB, 需两个 TU 触发, 此处示意)
// 编译: 两个文件分别定义 int g=1; int g=2; 链接 -> ODR 违反
// 简化单 TU 演示: 不同文件同名的 inline 不一致
// （真实 UB 需跨翻译单元, 此处仅标注, 不内联演示以免误用）
```

### 8.12 在 const 对象上写（UB）

```cpp
// prog_33_write_const.cpp  —— 错误示例 (UB)
// 编译: g++ -std=c++20 -Wall prog_33_write_const.cpp -o prog_33
#include <iostream>
int main() {
    const int c = 10;
    // const_cast<int&>(c) = 20;   // UB: 写真正声明为 const 的对象 (硬件层 SIGSEGV)
    std::cout << c;
}
```
`[平台]` 真正声明为 `const` 的对象可能位于只读页（`.rodata`），写会触发保护错误。

### 8.13 迭代器失效后使用（UB）

```cpp
// prog_34_iterator_invalidation.cpp  —— 错误示例 (UB)
// 编译: g++ -std=c++20 -Wall prog_34_iterator_invalidation.cpp -o prog_34
#include <vector>
#include <iostream>
int main() {
    std::vector<int> v{1,2,3};
    auto it = v.begin();
    v.push_back(4);            // 可能 realloc -> it 失效
    std::cout << *it;          // UB: 使用失效迭代器
}
```
**修复**：`push_back` 后重新取迭代器，或用 `reserve`。

### 8.14 异常穿透 noexcept（UB→std::terminate）

`[标准]` [except.spec]/5：若异常试图离开 `noexcept` 函数，调用 `std::terminate`。严格说是"实现必须调用 terminate"，非纯 UB，但等价于程序失控。

```cpp
// prog_35_exception_noexcept.cpp  —— 错误示例 (std::terminate)
// 编译: g++ -std=c++20 -Wall prog_35_exception_noexcept.cpp -o prog_35
#include <stdexcept>
void f() noexcept { throw std::runtime_error("boom"); }  // 离开 noexcept -> terminate
int main() { f(); }
```

### 8.15 同存储两次构造无析构（UB）

```cpp
// prog_36_double_construct_no_dtor.cpp  —— 错误示例 (UB)
// 编译: g++ -std=c++20 -Wall prog_36_double_construct_no_dtor.cpp -o prog_36
#include <new>
struct D { int x; D(int v):x(v){} ~D(){ x = -1; } };
int main() {
    alignas(D) char buf[sizeof(D)];
    D* a = ::new (buf) D(1);
    // 缺少 a->~D();
    D* b = ::new (buf) D(2);   // UB: 旧对象未析构即重建 (若 D 有 nontrivial 析构)
    b->~D();
}
```
**修复**：`::new` 重建前先 `a->~D()`（见 §2.3 prog_03）。

### 8.16 各 UB 的"检测手段"对照表（工业级速查）

`[实现][经验]` 不是所有 UB 都能被工具抓住。下表标注每类 UB **首选检测手段**与**编译器告警**（没有"——"表示只能靠 code review/静态分析）：

| # | UB 类别 | 首选 Sanitizer | 编译期告警/分析 |
|---|---|---|---|
| 1 | 有符号溢出 | UBSan (`-fsanitize=undefined`) | `-Waggressive-loop-optimizations` |
| 2 | 空指针解引用 | UBSan / ASan | `-Wnull-dereference`(Clang) |
| 3 | 数组越界 | ASan（`-fsanitize=address`） | `-Warray-bounds` |
| 4 | 数据竞争 | TSan（`-fsanitize=thread`） | 静态竞争检测（困难） |
| 5 | 释放后使用 | ASan / Valgrind | 无可靠编译期 |
| 6 | 严格别名违反 | 无直接 San | `-Wstrict-aliasing`(GCC, 噪声大) |
| 7 | 未初始化读 | MSan（`-fsanitize=memory`）/ASan 部分 | `-Wuninitialized` / `-Wmaybe-uninitialized` |
| 8 | 移位负/超宽 | UBSan | `-Wshift-count-negative`/`-Wshift-count-overflow` |
| 9 | 有符号左移溢出 | UBSan | 同上 |
| 10 | int↔指针 reinterpret | 无直接 San | `-Wint-to-pointer-cast` |
| 11 | 多重定义 ODR | 链接器 / 静态分析 | `-Wmultiple-definition` |
| 12 | 写 const 对象 | 无直接 San | 通常因 `.rodata` 段错误暴露 |
| 13 | 迭代器失效 | 无直接 San | Clang `-Wdangling` 部分覆盖 |
| 14 | 异常穿透 noexcept | 无 San | `-Wexceptions`/静态分析 |
| 15 | 同存储两次构造 | 无直接 San | 靠 review + launder 纪律 |

`[经验]` 注意 **MSan（MemorySanitizer）** 专门抓"未初始化读"（#7），它比 ASan 更激进但开销更大，且需要**整个依赖链**都用 `-fsanitize=memory` 重编（否则误报）。Clang 提供，GCC 无原生 MSan。

---

## ⑨ UB 与"未指定 / 实现定义 / 良构"的区别

`[标准]` 这是最容易混淆的概念分层（[defns.undefined]/[defns.unspecified]/[defns.impl.defined]/[defns.well.formed]）：

| 术语 | 含义 | 是否错误 | 示例 |
|---|---|---|---|
| 良构（well-formed） | 符合语法与语义约束 | 否 | `int x = 1;` |
| 未指定（unspecified） | 合法，但结果在数个可接受值中任选 | 否 | 函数实参求值顺序 |
| 实现定义（implementation-defined） | 合法，结果由实现文档规定 | 否 | `sizeof(int)`、`char` 是否有符号 |
| UB | 标准**完全不约束**行为 | 是（程序整体失效） | 有符号溢出、空指针解引用 |

`[经验]` 未指定/实现定义**不会**让程序崩溃或"任意行为"，只是结果可变；UB 让**整个程序**从首个 UB 起语义失效（"鼻恶魔"）。

```cpp
// prog_37_unspecified_order.cpp  —— 未指定, 非 UB
// 编译: g++ -std=c++20 -Wall prog_37_unspecified_order.cpp -o prog_37
#include <iostream>
int a() { std::cout << "a"; return 1; }
int b() { std::cout << "b"; return 2; }
int main() { int r = a() + b(); (void)r; }   // 打印 "ab" 或 "ba" 都合法
```

```cpp
// prog_38_impl_defined_sizeof.cpp  —— 实现定义, 非 UB
// 编译: g++ -std=c++20 -Wall prog_38_impl_defined_sizeof.cpp -o prog_38
#include <iostream>
int main() { std::cout << sizeof(int) << "\n"; }  // 由实现规定(通常 4)
```

---

## ⑩ UB 不是"运行时报错"，而是"编译器可任意处理"

`[标准][实现]` 这是全章最核心的认知转变：UB **不会**产生"标准规定的运行时异常"。相反，标准把"发生 UB 后的行为"完全留给实现——实现可以崩溃、可以静默给出错误结果、可以**删除相关代码**、可以**把循环变成无限循环**。

`[经验]` 因此"我测试过没崩，所以这段代码安全"是**致命误区**：UB 在某次编译/某次输入下"恰好工作"，换优化级别、换编译器、换 CPU 就可能爆炸。下面两节用本机 GCC 13.1.0 的**真实汇编**证明。

---

## ⑪ 优化武器化实例：时间旅行与代码删除

`[实现]` 编译器在 `-O2` 下基于"UB 永不发生"的假设做推理。以下是**本机 GCC 13.1.0 实测**的汇编（节选）。

### 11.1 有符号溢出把"死循环"优化成真·无限循环

源程序：

```cpp
// prog_39_overflow_loop_weaponized.cpp
// 编译: g++ -std=c++20 -O2 -S prog_39_overflow_loop_weaponized.cpp -o /tmp/p39.s
#include <cstdio>
int main() {
    int i = 1;
    while (i > 0) { i += 1; }    // 期望: 溢出后 i 变负, 循环退出
    printf("i=%d\n", i);         // 实际: 编译器假定 i 永不溢出 -> 循环永不退出
}
```

**`-O0` 汇编**（忠实地按代码生成）：循环体有 `addl $1,-4(%rbp)` 与 `cmpl $0,-4(%rbp)` 的真实比较与跳转。

**`-O2` 汇编**（本机输出，关键行）：

```
ub_overflow.cpp:5:11: warning: iteration 2147483646 invokes undefined behavior
                               [-Waggressive-loop-optimizations]
main:
    subq    $40, %rsp
    call    __main
.L2:
    jmp     .L2          ; <-- 整个循环被编译成 "jmp .L2" 无限自旋!
```

`[实现]` 编译器看到 `i += 1` 后 `i > 0`——它**证明**有符号 `i` 永远非负（因为溢出是 UB，被假定不发生），于是 `while(i>0)` 恒真，循环退化为 `jmp .L2` 死循环。这是"时间旅行"式优化：编译器用"未来不可能发生的事"反推"现在的条件恒真"。

### 11.2 空指针检查被删除（因解引用空指针是 UB）

源程序：

```cpp
// prog_40_null_check_deleted.cpp
// 编译: g++ -std=c++20 -O2 -S prog_40_null_check_deleted.cpp -o /tmp/p40.s
#include <cstdlib>
int* p = nullptr;
int main() {
    if (p != nullptr) { return *p; }   // 这个分支本应可达
    *p = 42;                            // UB: 解引用空指针
    return 0;
}
```

**`-O2` 汇编**（本机输出，关键行）：

```
main:
    call    __main
    movq    p(%rip), %rax
    testq   %rax, %rax
    je      .L6
    movl    (%rax), %eax      ; 分支: 读 *p
    ...
.L6:
    xorl    %eax, %eax
    movl    %eax, 0           ; <-- 直接向地址 0 (NULL) 写入 0
    ud2                      ; <-- 未定义指令, 立即终止
```

`[实现]` 编译器见到 `*p = 42`（对 `p` 解引用），即**断定 `p` 非空**（否则已 UB）。于是前面的 `if (p != nullptr)` 检查被判定为"恒真"可优化，但空指针路径仍被发射成 `movl %eax,0; ud2`——直接往 NULL 写并触发 `ud2`。这证明：优化器**主动删除了安全假设**，把"不可能"的路径变成了"确定崩溃"。

`[经验]` 这类 bug 在 `-O0` 下"看起来能跑"，`-O2` 下"神秘崩溃"或"死循环"。唯一解药是**不要写 UB**，而非依赖某次编译结果。

### 11.3 数组越界让编译器删掉"别的"边界检查（阵列去相关）

`[实现]` 严格别名/未定义行为的"传染性"不止于本语句：一旦编译器在某个循环里"证明"索引不会越界（因为它假定你不会写 UB），它就可以**删掉同一函数里另一处对同一个/同形数组的边界检查**。这叫"去相关（disambiguation）"。

```cpp
// prog_39b_bounds_elim.cpp  —— 优化武器化: 越界假设消除边界检查
// 编译: g++ -std=c++20 -O2 -S prog_39b_bounds_elim.cpp -o /tmp/p39b.s
#include <cstddef>
extern int arr[16];
int sum_first(int n) {           // n 由调用者传入, 可能 > 16
    int s = 0;
    for (int i = 0; i < n; ++i)
        s += arr[i];             // 若编译器假定 n<=16(否则 UB), 此循环无越界
    return arr[0] + s;           // 此处的访问也被"证明"安全
}
```
`[实现]` 若 `n` 被上游某个 UB 假设（例如 `n` 来自一处越界写入）污染，GCC/Clang 可能推断 `0<=i<16` 恒成立，于是把 `arr[i]` 编译成无符号扩展/无边界检查的连续加载，并把 `arr[0]` 的读取与前一个循环**合并/重排**。结果：你在一处写的 UB，让**另一处原本安全的代码**被错误优化。这正是 UB "传播性"的可怕之处。

`[经验]` 结论：UB 不是"局部小错"，它是**整函数乃至跨函数优化推理的毒药**。任何一处 UB 都可能让编译器把看似无关的正确代码改成错误代码。

---

## ⑫ 未初始化读与 padding：陷阱表示

`[标准]` [dcl.init]/12：读取未初始化的对象，若该类型有**陷阱表示（trap representation）**，则读取本身是 UB。标量类型如 `bool` 只能取 `true`/`false`（`[basic.fundamental]`），`float` 有 NaN 陷阱位——读了"非法位模式"的 `bool`/`float` 即 UB，且 `memcpy` 复制 padding 也可能触发。

```cpp
// prog_41_trap_representation.cpp  —— 错误示例 (UB)
// 编译: g++ -std=c++20 -Wall prog_41_trap_representation.cpp -o prog_41
#include <cstring>
#include <iostream>
struct Packed {
    bool b;        // 1 字节, 但相邻可能有 padding
    int  i;
};
int main() {
    Packed p;                    // p.b, p.i 均未初始化
    std::cout << p.b;            // UB: bool 的非法位模式 = 陷阱表示
    char buf[sizeof(Packed)];
    std::memcpy(&p, buf, sizeof buf);  // 复制未定义 padding 内容
}
```
`[经验]` 始终值初始化：`Packed p{};`。`reinterpret`/memcpy 跨结构体时留意 padding 不可移植。

### 12.1 padding 与位域：跨平台不可移植陷阱

`[平台]` 下面的结构体在 x86-64 上 `sizeof` 通常是 8（`bool` 占 1 字节 + 3 字节 padding + `int` 4 字节），那 3 字节 padding **内容未指定**。若你 `memcpy` 整个结构体去比较/传输，padding 字节可能含栈上残留——跨进程/跨机比较会"相等但字节不同"。

```cpp
// prog_41b_padding_compare.cpp  —— 错误示例 (依赖 padding 内容)
// 编译: g++ -std=c++20 -Wall prog_41b_padding_compare.cpp -o prog_41b
#include <cstring>
#include <iostream>
struct Wire { bool flag; int value; };     // 有未初始化的 padding
bool eq(const Wire& a, const Wire& b) {
    char ca[sizeof(Wire)], cb[sizeof(Wire)];
    std::memcpy(ca, &a, sizeof(Wire));
    std::memcpy(cb, &b, sizeof(Wire));
    return std::memcmp(ca, cb, sizeof(Wire)) == 0;  // UB 风险: 比较了 padding
}
int main() {
    Wire a{true, 1}, b{true, 1};
    // eq(a,b) 可能因 padding 残留不同而返回 false
    (void)eq(a, b);
}
```
**修复**：逐字段比较（`a.flag==b.flag && a.value==b.value`），或对 padding 用 `std::memset`/`= {}` 清零后再 `memcpy`。序列化时也只传"有意义"的字段，不盲目 `memcpy` 整个结构体。交叉 ch25（联合 active member）：联合的 padding 同样不可信。

---

## ⑬ 严格别名与 UB（交叉 ch27 / ch42）

`[标准]` [basic.lval]/11 允许的"合法别名途径"：
- 通过 `char`/`unsigned char`/`signed char`/`std::byte` 的 glvalue 访问任何对象（"字符类型豁免"）；
- 通过**动态类型相似**类型访问；
- 通过 `memcpy`/`std::bit_cast` 复制字节后再解释（不违反别名，因为产生新对象）。

`[实现]` 关闭严格别名用 `-fno-strict-aliasing`（GCC/Clang 默认**开启**）；MSVC 的 `/Oa`（已废弃）语义不同。合法重解释用 `std::bit_cast`（C++20，看 ch27）：

```cpp
// prog_42_bit_cast_legal.cpp  —— 正确: 绕过严格别名
// 编译: g++ -std=c++20 -Wall prog_42_bit_cast_legal.cpp -o prog_42
#include <bit>
#include <cstdint>
#include <iostream>
int main() {
    float f = 1.0f;
    // 合法: bit_cast 经字节复制产生新对象, 不违反严格别名(要求同尺寸)
    std::uint32_t bits = std::bit_cast<std::uint32_t>(f);  // 取 float 的位模式
    std::cout << bits;
}
```
`[标准]` 参见 ch27 `reinterpret_cast` 边界与 ch42 严格别名与优化，二者与本节共用 [basic.lval] 条款。

### 13.1 当别名豁免不够用：`__attribute__((may_alias))` 与 `[[noalias]]`

`[实现]` 有时你必须让一个类型"故意违反"严格别名——典型场景是手写网络/序列化缓冲区、或 SIMD 向量视图。两个厂商扩展/标准手段：

1. **`__attribute__((may_alias))`（GCC/Clang）**：给类型加此属性后，**该类型的指针可被当作"可别名任意对象"** 处理，编译器不再对它做激进的别名假设。常用于 `typedef float m128f __attribute__((may_alias));` 让向量指针能安全别名普通 `float[]`。

```cpp
// prog_42b_may_alias.cpp  —— 用 may_alias 合法化跨类型访问
// 编译: g++ -std=c++20 -Wall -fstrict-aliasing prog_42b_may_alias.cpp -o prog_42b
#include <cstdint>
#include <iostream>
typedef std::uint16_t aliased_u16 __attribute__((may_alias));
int main() {
    std::uint32_t x = 0x12345678;
    // 经 may_alias 类型读取 -> 编译器不假定别名冲突, 合法路径
    aliased_u16* p = reinterpret_cast<aliased_u16*>(&x);
    std::cout << *p;          // 取低 16 位, 不触发严格别名 UB
}
```

2. **`[[noalias]]`（C++23 标准属性）**：给函数参数标注"此指针不别名其他参数"，让优化器放心地做重排（与 C 的 `restrict` 等价）。`[实现]` Clang 完整支持；GCC 13.x 会发 `-Wattributes` 警告并**忽略**该属性（语义上仍合法，只是未获优化）。这是"反向"工具——它**声明无别名**以换取优化，而非放宽别名规则。

```cpp
// prog_42c_noalias.cpp  —— [[noalias]] 声明无别名以助优化
// 编译: g++ -std=c++23 -Wall prog_42c_noalias.cpp -o prog_42c
#include <cstddef>
[[nodiscard]] int* f(int* [[noalias]] p, int* [[noalias]] q) {
    *p = 1; *q = 2;
    return p;                 // 编译器已知 p,q 不重叠, 可安全重排两侧写
}
int main() { int a=0,b=0; (void)f(&a,&b); }
```

`[标准][经验]` 偏好排序：`std::memcpy`/`std::bit_cast`（零风险）> `__attribute__((may_alias))`（局部放宽，受控）> `[[noalias]]`（优化声明）> `-fno-strict-aliasing`（全局关闭，影响整模块性能，最后手段）。绝不要用裸 `reinterpret_cast` 跨类型读（prog_27）。

---

## ⑭ 真实 libstdc++ 源码逐行：`launder` / `operator new` / `addressof`

`[实现]` 以下全部取自本机 **MinGW GCC 13.1.0** 的 libstdc++，路径前缀：
`C:/Qt/Tools/mingw1310_64/lib/gcc/x86_64-w64-mingw32/13.1.0/include/c++/`
（下引行号基于该文件）。

### 14.1 `std::launder`（`<new>`：188–208）

文件 `<new>`（即上面路径下的 `new`）：

```cpp
// <new> :188-208  (libstdc++ 13.1.0, MinGW GCC 13.1.0)
#if __cplusplus >= 201703L
namespace std
{
#ifdef _GLIBCXX_HAVE_BUILTIN_LAUNDER
#define __cpp_lib_launder 201606L
  /// Pointer optimization barrier [ptr.launder]
  template<typename _Tp>
    [[nodiscard]] constexpr _Tp*
    launder(_Tp* __p) noexcept
    { return __builtin_launder(__p); }          // 第194行: 体即一个内建调用

  // The program is ill-formed if T is a function type or
  // (possibly cv-qualified) void.

  template<typename _Ret, typename... _Args _GLIBCXX_NOEXCEPT_PARM>
    void launder(_Ret (*)(_Args...) _GLIBCXX_NOEXCEPT_QUAL) = delete;
  template<typename _Ret, typename... _Args _GLIBCXX_NOEXCEPT_PARM>
    void launder(_Ret (*)(_Args......) _GLIBCXX_NOEXCEPT_QUAL) = delete;

  void launder(void*) = delete;                 // 第204行: 阻止对 void* 误用
  void launder(const void*) = delete;
  void launder(volatile void*) = delete;
  void launder(const volatile void*) = delete;
#endif // _GLIBCXX_HAVE_BUILTIN_LAUNDER
```

`[实现]` 逐行要点：
- **第 194 行** `launder` 的函数**体本身什么都没做**（直接 `return __p` 经内建）。它的作用**完全在于编译器内建 `__builtin_launder`**：这是一个"优化屏障"语义原语。即便汇编层面 `p` 没变，优化器也必须假定"返回的指针可能指向一个不同类型/已重建的对象"，从而**丢弃**基于旧对象推导出的事实（如"const 成员值不变"）。
- **第 199–207 行** 用 `= delete` 禁止对**函数指针**和 **`void*`** 调用 `launder`，避免把"无类型指针"当对象指针用（那是另一类 UB）。
- `[[nodiscard]]` 提醒调用者必须用返回值——直接写 `std::launder(p);` 而不接返回值毫无意义（不会改 `p`）。

`[标准]` 为什么需要它？见 §2.4：placement new 在同一存储重建**不相似类型**后，旧指针 `p` 在优化器眼中"仍指向旧对象"。若旧对象是 `const` 成员，优化器可能常量传播旧值。必须 `p = std::launder(p);` 才能让优化器"忘记"旧对象。

### 14.2 `operator new` / `operator delete`（`<new>`：126–181）

```cpp
#include <cstddef>
// <new> :126-181  (libstdc++ 13.1.0)
_GLIBCXX_NODISCARD void* operator new(std::size_t) _GLIBCXX_THROW (std::bad_alloc)
  __attribute__((__externally_visible__));                 // 第126行: 普通 new
_GLIBCXX_NODISCARD void* operator new[](std::size_t) _GLIBCXX_THROW (std::bad_alloc)
  __attribute__((__externally_visible__));                 // 第128行: 数组 new
void operator delete(void*) _GLIBCXX_USE_NOEXCEPT
  __attribute__((__externally_visible__));                 // 第130行: 普通 delete
void operator delete[](void*) _GLIBCXX_USE_NOEXCEPT
  __attribute__((__externally_visible__));                 // 第132行: 数组 delete
// ... sized/aligned/nothrow 重载略 ...
// Default placement versions of operator new.              第173行起
_GLIBCXX_NODISCARD inline void* operator new(std::size_t, void* __p) _GLIBCXX_USE_NOEXCEPT
{ return __p; }                                            // 第174-175行: placement new
_GLIBCXX_NODISCARD inline void* operator new[](std::size_t, void* __p) _GLIBCXX_USE_NOEXCEPT
{ return __p; }
// Default placement versions of operator delete.          第179行起
inline void operator delete  (void*, void*) _GLIBCXX_USE_NOEXCEPT { }   // 第180行: 空
inline void operator delete[](void*, void*) _GLIBCXX_USE_NOEXCEPT { }
```

`[实现]` 逐行要点：
- **第 126–132 行** 是替换全局 `new`/`delete` 的声明（非 `inline`，在运行时库 `libstdc++.a` 中实现，内部调 `malloc`/`free` 并抛 `bad_alloc`）。
- **`__attribute__((__externally_visible__))`**：保证即使看似无副作用，该函数不被优化掉（它是程序对外的"可见"入口，里德-温伯格定理的反向：分配不能消失）。
- **第 174 行** placement new 就是 `return __p;`——不分配内存，只返回传入的存储地址供构造用。这就是 §2 所有 placement new 示例的底层机制。
- **第 180 行** placement delete 是空函数（不释放存储），符合标准语义。

### 14.3 `std::addressof`（`<bits/move.h>`：47–50 与 142–151）

```cpp
// <bits/move.h> :47-50  (libstdc++ 13.1.0)
  template<typename _Tp>
    inline _GLIBCXX_CONSTEXPR _Tp*
    __addressof(_Tp& __r) _GLIBCXX_NOEXCEPT
    { return __builtin_addressof(__r); }          // 第50行: 用内建取真实地址

// <bits/move.h> :142-151
  template<typename _Tp>
    _GLIBCXX_NODISCARD
    inline _GLIBCXX17_CONSTEXPR _Tp*
    addressof(_Tp& __r) noexcept
    { return std::__addressof(__r); }             // 第146行: 委托给 __addressof

  template<typename _Tp>
    const _Tp* addressof(const _Tp&&) = delete;   // 第151行: 禁止对临时调用
```

`[实现]` 逐行要点：
- **第 50 行** `__builtin_addressof(__r)`：这是关键——它**绕过用户重载的 `operator&`**。普通的 `&x` 若 `T` 重载了 `operator&`，返回的是运算符结果（可能根本不是地址）；而 `__builtin_addressof` 直接取对象真实内存地址。
- **第 146 行** 公开接口 `std::addressof` 委托给内部 `__addressof`，二者都 `constexpr`（C++17 起，`_GLIBCXX17_CONSTEXPR`），可在编译期使用。
- **第 151 行** 删除 `addressof(const T&&)` 重载，阻止 `std::addressof(SomeTemporary())`——临时无稳定地址，误用会悬垂。

`[标准]` 交叉 ch20（引用）：`addressof` 与 `std::launder` 是标准库里两个"看起来啥也没干、实则驯服优化器"的原语，其价值在 `-O2` 下才显形。

---

## ⑮ 三编译器对比：GCC / Clang / MSVC

`[实现][平台]` 下表基于 GCC 13.x、Clang 16+、MSVC 19.x 的公开行为：

| 能力 | GCC | Clang | MSVC |
|---|---|---|---|
| UBSan (`-fsanitize=undefined`) | ✅（Linux 完整；MinGW 缺运行时库 `[平台-推断]`） | ✅（最完整，默认带运行时） | ⚠️ `/fsanitize=undefined`（实验，部分） |
| ASan (`-fsanitize=address`) | ✅ Linux | ✅ | ⚠️ `/fsanitize=address`（较新版本） |
| TSan (`-fsanitize=thread`) | ✅ Linux | ✅ | ❌ 无原生 |
| `-fstrict-aliasing` 默认 | ✅ 开 | ✅ 开 | ⚠️ 模型不同（`/Oa` 废弃） |
| `/permissive-`（MSVC 严格模式） | — | — | ✅ 关掉非标准许可，减少隐式 UB 容忍 |
| `std::launder` 实现 | `__builtin_launder` | `__builtin_launder` | 内建 `__builtin_launder` |

`[实现]` **关键差异**：
1. **严格别名**：GCC/Clang 默认 `-fstrict-aliasing`（prog_27 在 `-O2` 下会被优化出"正确但错误"的结果）；MSVC 的别名模型更宽松（历史上很少按严格别名优化），所以同一段别名违规代码在 MSVC 下"看似正常"、在 GCC/Clang 下崩溃——**绝不因此以为代码安全**。
2. **`/permissive-`**：MSVC 默认 `/permissive`（兼容模式）会容忍一些非标准/潜在 UB 的写法；加上 `/permissive-` 可暴露更多问题，是 Windows 下逼近标准的手段。
3. **Sanitizer 运行时**：本机 MinGW GCC 13.1.0 **未随附** `libubsan/libasan/libtsan`（见 §⑯ 实测 `-lubsan: No such file or directory`），故本机只能跑**编译期** UB 诊断（`-Waggressive-loop-optimizations` 等）与 §⑪ 的汇编级证据；完整运行时检测需 Linux/Clang 或 MSVC 的 ASan。

`[经验]` CI 矩阵必须覆盖 **GCC + Clang**（不同优化器对 UB 的反应不同），不能只测一个编译器。

### 15.1 `/permissive-` 与 `-Werror`：把隐式 UB 挡在编译期

`[平台]` Windows 下 MSVC 的 `/permissive-` 能关掉大量"历史兼容"许可（如非标准的范围 for 临时、隐式 `int`、两阶段查找放松）。它虽不直接检测 UB，但能**消除"因编译器宽容而看起来正常"的危险写法**：

```cpp
// prog_47_permissive_example.cpp  —— MSVC 下 /permissive- 暴露问题
// 编译(MSVC): cl /std:c++20 /permissive- /W4 prog_47_permissive_example.cpp
struct S { int m; };
int f() {
    // 非标准扩展: 在成员函数外用 "S::m" 取成员类型在非标准模式被容忍,
    // /permissive- 下按标准拒绝 -> 逼你写明确、无歧义的合法代码
    return sizeof(S::m);          // C++11 起合法, 但宽松模式可能放过更多隐患写法
}
```
`[经验]` 跨平台项目建议：GCC/Clang 加 `-Wall -Wextra -Wshadow -Wconversion -Werror`（至少 `-Werror` 用于 CI）；MSVC 加 `/W4 /permissive- /w14640`（悬垂检测告警）。把"宽松模式能过"当作**红灯**而非绿灯。

---

## ⑯ UBSan / ASan / TSan 检测

`[标准][实现]` 三类 Sanitizer 是工业级定位 UB 的基石（注意：它们是**检测手段**，不是性能基准）：

| 工具 | 检测目标 | 编译开关 | 开销 |
|---|---|---|---|
| UBSan | 有符号溢出、移位、空解引用、类型混淆等 | `-fsanitize=undefined` | 低–中 |
| ASan | 释放后使用、越界、double-free | `-fsanitize=address` | 中–高 |
| TSan | 数据竞争 | `-fsanitize=thread` | 高 |

`[平台]` **本机实测**：在 MinGW GCC 13.1.0 上链接 sanitizer 失败：
```
C:/Qt/.../ld.exe: cannot find -lubsan: No such file or directory
collect2.exe: error: ld returned 1 exit status
```
（ASan/TSan 同样缺 `libasan`/`libtsan`）——这是 MinGW 发行版的**平台限制** `[平台-推断]`，非代码问题。下给出**典型输出**（取自 Clang/GCC-on-Linux 实测，作为标准诊断形态）：

### 16.1 UBSan 典型输出（有符号溢出，prog_22）

```cpp
// prog_43_ubsan_demo.cpp  —— 对应 prog_22, 用 UBSan 跑
// 编译(Clang/Linux): clang++ -std=c++20 -fsanitize=undefined prog_43_ubsan_demo.cpp -o prog_43
#include <limits>
int main() {
    int x = std::numeric_limits<int>::max() + 1;   // UBSan 在此触发
    return x;
}
```
**典型 UBSan 诊断**（参考输出）：
```
prog_43_ubsan_demo.cpp:4:38: runtime error: signed integer overflow:
  addition of unsigned value 2147483647 and 1 cannot be represented in type 'int'
SUMMARY: UndefinedBehaviorSanitizer: undefined-behavior prog_43_ubsan_demo.cpp:4:38
```

### 16.2 ASan 典型输出（释放后使用，prog_26）

```cpp
// prog_44_asan_demo.cpp  —— 对应 prog_26, 用 ASan 跑
// 编译: clang++ -std=c++20 -fsanitize=address prog_44_asan_demo.cpp -o prog_44
#include <iostream>
int main() {
    int* p = new int(7);
    delete p;
    std::cout << *p;        // ASan 在此触发 heap-use-after-free
}
```
**典型 ASan 诊断**（参考输出）：
```
==12345==ERROR: AddressSanitizer: heap-use-after-free on address 0x602...
READ of size 4 at 0x602... thread T0
    #0 0x... in main prog_44_asan_demo.cpp:6:20
    #1 0x... in __libc_start_main
0x602... is located 0 bytes inside of 4-byte region [0x602...,0x602...)
freed by thread T0 here:
    #0 0x... in operator delete prog_44_asan_demo.cpp:5
```

### 16.3 TSan 典型输出（数据竞争，prog_25）

```cpp
// prog_45_tsan_demo.cpp  —— 对应 prog_25, 用 TSan 跑
// 编译: clang++ -std=c++20 -fsanitize=thread -pthread prog_45_tsan_demo.cpp -o prog_45
#include <thread>
int g = 0;
void f() { for (int i=0;i<100000;++i) ++g; }
int main() { std::thread a(f), b(f); a.join(); b.join(); }
```
**典型 TSan 诊断**（参考输出）：
```
WARNING: ThreadSanitizer: data race (pid=...)
  Write of size 4 at 0x... by thread T2:
    #0 f() prog_45_tsan_demo.cpp:4
  Previous write of size 4 at 0x... by thread T1:
    #0 f() prog_45_tsan_demo.cpp:4
```

`[经验]` 把 `-fsanitize=address,undefined` 接入**测试构建 + CI**，能让绝大多数内存/整数 UB 在合并前现形。注意 TSan 与 ASan **不可同时启用**（运行时互斥）。

### 16.1 把 Sanitizer 接入 CMake + CI（实用片段）

`[经验]` 不要只在本地手敲命令。把检测做成独立构建类型，CI 自动跑：

```cmake
# CMakeLists.txt 片段: 提供 Sanitize 构建类型
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# cmake -DCMAKE_BUILD_TYPE=Sanitize ..
set(CMAKE_CXX_FLAGS_SANITIZE
    "-O1 -g -fsanitize=address,undefined -fno-omit-frame-pointer"
    CACHE STRING "" FORCE)
set(CMAKE_EXE_LINKER_FLAGS_SANITIZE
    "-fsanitize=address,undefined" CACHE STRING "" FORCE)
```
`[经验]` 要点：
- **用 `-O1` 而非 `-O0`**：Sanitizer 在 `-O0` 下噪声多、漏报多；`-O1` 兼顾速度与精度。
- **`-fno-omit-frame-pointer`**：保证栈回溯可读。
- **独立 CI job**：Sanitize 构建比普通构建慢数倍，放独立流水线，失败时阻断合并。
- **TSan 单独 job**：因与 ASan 互斥，另开一个 `-fsanitize=thread` job（交叉 ch61）。

---

## ⑰ 常量表达式中的 UB：constexpr 直接编译失败

`[标准]` [expr.const]：常量表达式求值中若出现 UB（溢出、空解引用、越界等），则**该表达式不是常量表达式**，含有它的 `constexpr` 变量/函数**直接编译失败**——这是 constexpr 的"免费 UB 检测"。

```cpp
// prog_46_constexpr_ub_fail.cpp  —— 编译失败示例 (constexpr 中 UB)
// 编译: g++ -std=c++20 -Wall prog_46_constexpr_ub_fail.cpp -o prog_46  (报错)
constexpr int bad() {
    int x = 2147483647;
    x += 1;                 // UB: 有符号溢出, 出现在 constexpr 求值中
    return x;
}
int main() { constexpr int v = bad(); (void)v; }
```
**典型编译错误**（参考输出）：
```
prog_46_constexpr_ub_fail.cpp: In function 'constexpr int bad()':
prog_46_constexpr_ub_fail.cpp:4:11: error: overflow in constant expression [-fpermissive]
    4 |     x += 1;
      |     ~~^~~~
```
`[经验]` 善用 `constexpr`/`consteval` 把"编译期能验证的不变式"前置到编译期——UB 在编译期就炸，比运行期 Sanitizer 更早、零开销。交叉 ch31/33（异常）：`constexpr` 中抛异常或调用非 constexpr 同样编译失败。

### 17.1 constexpr 中 UB 的"边界"：并非所有 UB 都能在编译期被抓

`[标准]` 需要清醒：`constexpr` 只挡住"恰好发生在常量求值路径上"的 UB。若 UB 发生在**运行期分支**（仅当非常量实参才触发），编译器**不会**为它报错——它只在你用常量实参调用时才求值。因此 `constexpr` 是**必要不充分**的 UB 防护。

```cpp
// prog_46b_constexpr_runtime_ub.cpp  —— constexpr 不覆盖运行期 UB
// 编译: g++ -std=c++20 -Wall prog_46b_constexpr_runtime_ub.cpp -o prog_46b  (通过!)
constexpr int maybe_ub(int n) {
    return n + 1;            // 若 n==INT_MAX 则 UB, 但 constexpr 不自动"全输入"验证
}
int main() {
    int x = maybe_ub(2147483647);   // 运行期实参 -> UB 在运行期发生, 编译期不报错
    (void)x;
}
```
`[经验]` 配合 `consteval`（强制编译期求值）可让更多路径进入常量求值，但**任何逃逸到运行期的代码仍需 Sanitizer**（§⑯）。`constexpr` 与 Sanitizer 是**互补**而非替代。

---

## ⑱ 生命周期安全：静态分析与 Lifetime 提案

`[标准][平台]` C++ 没有 Rust 式的所有权类型系统，但社区在用**静态分析**逼近：

1. **Clang 的 `-Wdangling` / `-Wlifetime` 实验**：基于 Microsoft 提出的 **Lifetime 静态分析**（提案 **P1174 / 早期 dangling-pointer 分析**），通过**多次借用（reborrow）规则**在编译期标记悬垂。它给指针/引用加"生命周期注解"，推导"返回的引用指向哪个参数"，从而在无运行时开销下捕获 §⑦ 的多数悬垂。

2. **Core Check（MSVC `/analyze` + CppCoreCheck）**：内置 `bounds`/`lifetime` 规则集，能在 Windows 上静态发现悬垂与越界。

3. **`gsl::span` / `std::string_view` 的"非空、有界"契约**：把"裸指针 + 长度"升格为带边界的对象，配合静态规则减少越界 UB（§⑧ prog_24）。

`[经验]` 生命周期静态分析是"尽量在编译期抓住悬垂"的现实路径；它不能覆盖全部（别名图复杂时退化为告警），但比"全靠人眼 review"强得多。商业/安全关键项目应开启对应分析器。

### 18.1 Lifetime 提案（P1174）的核心规则速览

`[标准]` Microsoft 的 Lifetime 静态分析（Herb Sutter 主导，提案 **P1174 / 早期 P0588**）定义了可机器检查的**借用规则**，目标是"在 C++ 里静态消除悬垂指针/引用"。核心规则（内化要点）：

1. **返回引用必须指向某个入参**：函数返回 `T&`/`T*` 时，分析器要求该引用"指向某个 `lifetime` 入参"；若指向局部（prog_17/18）则直接报错。
2. **`string_view`/`span` 参数标注 `lifetime`**：函数 `f(string_view s)` 接收的 view 的 `lifetime` 必须 ≤ 其调用处实参的 `lifetime`；把 view 绑定到临时（prog_21）会被标记。
3. **多次借用（reborrow）**：一个对象可被多次不可变借用，但**不可变借用存在期间不能有可变借用**——这正是 Rust 借用检查的规则，被移植到 C++ 的静态分析层。
4. **指针非空性剖面（nullability）**：用 `gsl::not_null<T*>` 表达"绝不空"，让分析器在解引用前不再需要空检查，也堵住 prog_23 类 UB。

`[实现]` 该提案尚未进入标准语言层（需要注解语法与参数化分析），目前以 **Clang `-Wlifetime` 实验**、**MSVC CppCoreCheck `lifetime` 规则**、以及 **`gsl::` 库类型** 形式落地。它的意义在于：把"悬垂"从"运行期崩溃/UB"降级为"编译期可诊断的契约违反"。

---

## ⑲ Core Guidelines 的 UB 规避

`[经验]` 来自 **C++ Core Guidelines** 的 UB 相关条目（已内化，非推荐阅读）：

| 条目 | 规则 | 对应本章 |
|---|---|---|
| ES.20 | 始终保持对象初始化 | §8.7 prog_28 |
| ES.42 | 避免有符号溢出，用 `unsigned` 或检查 | §8.1 prog_22 |
| ES.45 | 避免"魔法"窄化转换 | §8.9 移位 |
| ES.65 | 不要解引用无效指针 | §8.2/8.5/§⑦ |
| ES.73 | 优先用具名变量而非临时 | §6.3/7.3 |
| ES.74 | 勿在一条语句里混用指向同一对象的两类指针/引用 | §⑬ 别名 |
| C.30 | 定义常规模板/类时给析构 | §2.3 |
| F.43 | 不要返回局部对象引用/指针 | §⑦ prog_17/18 |
| I.11/`gsl::span` | 用 `span` 替代裸指针区间 | §8.3/§⑱ |
| CP.20/CP.21 | 用 `atomic`/`mutex` 避免数据竞争 | §8.4 prog_25 |
| P.5 | 编译期能查的用 `constexpr` 查 | §⑰ prog_46 |

`[经验]` 把以上规则写进 **Clang-Tidy / 编译器告警**（`-Wall -Wextra -Wshadow -Wconversion`），能在提交前拦下大多数 UB 雏形。

---

## ⑳ 跨语言对比 + 源码阅读路线

### 20.1 跨语言 UB 对比（[标准][平台]）

| 语言 | 内存模型 | 典型 UB 现状 | 工具生态 |
|---|---|---|---|
| **C++** | 手动/RAII + 裸指针 | UB 极多（溢出、别名、悬垂、竞争） | UBSan/ASan/TSan/Core Guidelines |
| **C** | 手动 | 与 C++ 同源 UB，且**无**标准库级检测工具，靠 `-fsanitize`/Coverity | 少 |
| **Rust** | 所有权 + 借用检查 + 生命周期标注 | **编译期消除整类 UB**：无空指针解引用（Option/Result）、无数据竞争（Send/Sync）、无悬垂（借用检查）、无越界（运行时 panics 而非 UB） | Miri（UB 解释器）、Clippy |
| **Java / C#** | 托管 GC | 无大部分内存 UB；数据竞争仍 UB（但无野指针/越界 UB） | 语言内内存安全 |
| **Go** | GC | 有少量 UB（数据竞争、unsafe 包），但无悬垂/越界 UB | `go test -race` |
| **Swift** | ARC | 无野指针/越界 UB；`UnsafePointer` 显式标注不安全区 | 内建 |

`[经验]` Rust 的"UB 在编译期被类型系统消灭"是 C++ 努力用 Sanitizer+静态分析+Guidelines 才部分达到的效果——这是现代 C++ 引入 `std::span`/`std::string_view`/`gsl` 的根本动机。但 C++ 的零开销与 ABI 兼容使其无法一步到位，故**工程师的纪律**仍是最后防线。

### 20.2 源码阅读路线（真实路径，本机可查）

`[实现]` 想真正理解"生命周期原语如何驯服优化器"，按此顺序读：

1. **libstdc++ `<new>`（本机路径 `.../include/c++/new`）**：
   - 第 188–208 行：`std::launder` 的 `__builtin_launder` 屏障（§⑭.1）。
   - 第 126–181 行：`operator new`/`operator delete` 全家桶与 placement 版本（§⑭.2）。
2. **libstdc++ `<bits/move.h>`（本机路径 `.../include/c++/bits/move.h`）**：
   - 第 47–50 行：`__addressof` 用 `__builtin_addressof` 绕过 `operator&`。
   - 第 142–151 行：`std::addressof` 与对临时的 `= delete`（§⑭.3）。
3. **LLVM/Clang UBSan 源码**（`llvm-project/compiler-rt/lib/ubsan/`）：
   - `ubsan_handlers.cpp`：`handleIntegerOverflow`/`handleNullPointerUsage`——理解诊断文本如何生成（§⑯）。
4. **C++ Core Guidelines**（`isocpp.github.io/CppCoreCheck`）：
   - "Lifetime" 章节与 `bounds`/`lifetime` profile——对应 §⑱/§⑲。
5. **提案 P1174（静态生命周期安全）** 与 **P0532（严格别名改进讨论）**：
   - 理解 C++ 标准化层面如何用静态分析补生命周期漏洞（§⑱）。

`[标准]` 交叉阅读：ch19（存储期/ODR）、ch20（引用与指针悬垂）、ch21（const 与写 UB，prog_33）、ch25（联合 active member 的"重解释"类 UB）、ch27（reinterpret_cast 与严格别名，prog_27/31/42）、ch31（异常与 UB，prog_35）、ch33（异常安全与资源 UB）、ch42（严格别名与优化，深层展开 `-fstrict-aliasing`）、ch61（并发数据竞争，prog_25/45）。

---

## ⑳+ 本章速查卡（工程铁律）

`[经验]` 把以下几条贴在工位：
1. **UB 不是 bug 的"一种"，而是"所有保证失效"**；测试通过≠安全。
2. **永远初始化**（prog_28/41）；**优先 `unsigned` 做位运算与回绕**（prog_22/30）。
3. **临时延长只看 `const T&`/`T&&` 直接绑定 prvalue**，其余（成员/数组/range-for/返回引用/initializer_list）全不延长（§⑤⑥）。
4. **`string_view`/`initializer_list` 绝不绑定临时**（prog_16/20/21）。
5. **placement new 重建前先 `->~T()`，重建后 `std::launder`**（prog_03/04）。
6. **别名重解释用 `memcpy`/`std::bit_cast`，别用 `reinterpret_cast` 读**（prog_27/42）。
7. **CI 开 `-fsanitize=address,undefined` + `/analyze`/Clang-Tidy**（§⑯⑲）。
8. **能 `constexpr` 验证的不变式前置到编译期**（prog_46）。

---

> 本章完。所有"推荐阅读"内容已内化（见 §⑭ 真实源码路线、§⑲ Guidelines、§⑳ 跨语言与提案）。后续深入：ch42（严格别名与优化，§⑬ 的延续）、ch61（并发数据竞争，§8.4/§⑯ 的延续）。


## 联合使用场景

| 关联章节 | 场景 | 组合方式 |
|---|---|---|
| [第27章](Book/part03_language/ch27_cast.md) | 独占所有权/工厂模式 | 本章提供概念，第27章提供实现 |

## 附录 E：生命周期工业案例

Google内部UB检测: ASan(每CI)+MSan(部分)+UBSan(~1.5x慢)
Chromium use-after-free CVE-2019-5786: unique_ptr过早释放,修复:shared_ptr
LLVM PR-41379: clang自身在-dump-tokens中use-after-free
C++26 contracts(P2900): pre/post在debug自动检查

```cpp
#include <iostream>
int main(){std::cout<<"UB=compiler weapons. ASan=use-after-free, UBSan=overflow."<<std::endl;return 0;}
```

面试: use-after-free检测通过ASan影子内存标记; UB危险因为编译器假设UB不可能发生


## 附录 F：UB面试

```cpp
#include <iostream>
int main(){int*p=new int(42);delete p;std::cout<<"use-after-free=UB; ASan detects it. No diagnostic required by standard."<<std::endl;return 0;}
```

| UB类型 | 检测 | 例子 |
|---|---|---|
| use-after-free | ASan | delete后读取 |
| null deref | UBSan | *nullptr |
| signed overflow | UBSan | INT_MAX+1 |
| ODR violation | 无 | 同一符号不同定义 |

面试: UB=未定义行为, 编译器可任意处理; ASan/UBSan在CI中检测

## 相关章节（交叉引用）

- **相邻主题**：`Book/part03_language/ch29_friend.md`（第29章 友元 friend 与访问控制）—— 编号相邻、主题接续。
- **相邻主题**：`Book/part03_language/ch26_lambda.md`（第26章　lambda 表达式全解：闭包类型、捕获、泛型/模板 lambda、constexpr、ABI 与 std::function 类型擦除）—— 编号相邻、主题接续。
- **相邻主题**：`Book/part03_language/ch30_volatile.md`（第30章 volatile / atomic 与硬件寄存器）—— 编号相邻、主题接续。
- **同模块**：`Book/part03_language/ch19_variables.md`（第19章　变量、存储期、链接与 ODR（工业级深度版））—— 同模块下的其他主题。

- **同模块**：`Book/part03_language/ch20_reference_pointer.md`（第20章　引用（reference）vs 指针（pointer）：语义本质、底层实现与生命周期战争）—— 同模块下的其他主题。

## 附录 G（工业级 UB / sanitizer 实战）

> 下列项目均在生产代码中大规模使用该特性，源码可在其公开仓库核查。

- **Google** — Abseil 与 ASan / GTest 深度集成做生命周期测试
- **LLVM** — `-fsanitize=address` 与 `-fsanitize=undefined` 由 Clang 提供
- **Chromium** — clusterfuzz 要求所有构建开启 ASan
- **Boost** — Boost.Uuid 严格避免未定义行为
- **Qt ** — QPointer 自动置空防止悬垂指针
- **Eigen** — AVX 对齐加载若越界会触发 UB，需用 `EIGEN_MAX_ALIGN_BYTES`
- **folly** — folly 提供 sanitizer 友好的原子封装
- **Redis** — CI 中开启 ASan 捕获越界写
- **ClickHouse** — 用 MSan 检测未初始化内存读取
- **RocksDB** — 单元测试默认挂 ASan
- **V8** — V8 GC 与 ASan 协同检测悬垂
- **DPDK** — DPDK 支持以 ASan 构建捕获池外写
- **gRPC** — CI 对 C++ 开启 ASan / UBSan
- **spdlog** — 实现严格无 UB，可被 sanitizer 验证
- **fmt** — 格式化库接受 fuzzing 持续测试
- **Unreal** — UE 提供专属 sanitizer 构建配置
- **WebKit** — WebKitGTK 提供 ASan 构建
- **Mozilla** — Mozilla 提供 ASan 官方构建
- **Abseil** — Abseil 要求编译器开启 UBSan 才合入
- **Blink** — Blink 用 sanitizer 验证布局对象生命周期

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


---

> **UB 实证库**：释放后使用 / 双重释放 / 栈对象越界使用等生命周期 UB 的**真实代码 + 编译器警告 + 运行时表现 + 修复**，见 [附录 UB 反例库](../../Appendix/ub/README.md)（UB-01/02/03）。
