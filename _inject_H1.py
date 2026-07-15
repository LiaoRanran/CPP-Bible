# -*- coding: utf-8 -*-
"""Phase H1: rewrite off-topic template exercises -> topic-aligned ladders,
and append a '附录：用法演绎' step-by-step scenario to 8 flagship chapters.
CRLF-safe. Replaces from '## 自测练习（Exercises）' to EOF (uniform anchor)."""
import os

ROOT = os.path.dirname(os.path.abspath(__file__))

TARGETS = {
    "Book/part03_language/ch20_reference_pointer.md": ("ch20", "引用与指针的取舍"),
    "Book/part03_language/ch27_cast.md":             ("ch27", "类型转换的正确姿势"),
    "Book/part04_memory/ch41_smart_pointers.md":     ("ch41", "智能指针所有权管理"),
    "Book/part05_oo/ch47_virtual_functions.md":      ("ch47", "虚函数与多态分发"),
    "Book/part07_stl/ch77_vector.md":               ("ch77", "vector 扩容与迭代器失效"),
    "Book/part07_stl/ch78_deque.md":               ("ch78", "deque 双端缓冲"),
    "Book/part07_stl/ch93_thread_async.md":        ("ch93", "线程与异步任务"),
    "Book/part08_algorithms/ch96_sorting.md":       ("ch96", "排序与 top-k 选择"),
}

# ---- exercises (replace EOF 自测练习 block) ----
EXERCISES = {
"ch20": r'''## 自测练习（Exercises）

> 以下题目用于自测掌握程度；答案折叠于每题下方，建议先独立作答。

### 练习 1（难度 ★★）

写一个函数 `void scale(std::vector<int>& v, int factor)`，把每个元素乘以 `factor`。
为什么这里**必须**用引用而不能用值传递？如果接口要求用指针，调用处要怎么写？

<details><summary>答案与解析</summary>

值传递 `std::vector<int> v` 会触发一次完整拷贝（O(n) 且可能抛 `bad_alloc`）；引用传递只绑定原对象，零拷贝。
若用指针：`void scale(std::vector<int>* v, int f)` 内部写 `(*v)[i] *= f`，调用处 `scale(&v, 2)`。
指针表达"可空"，引用表达"必非空"——按语义选：此函数不应接受空对象，故引用更贴切。

```cpp
#include <vector>
#include <iostream>
void scale(std::vector<int>& v, int f) { for (auto& x : v) x *= f; }
int main() {
    std::vector<int> v{1,2,3};
    scale(v, 10);
    for (int x : v) std::cout << x << ' '; // 10 20 30
}
```

[标准] 引用是已存在对象的别名，无独立存储；函数形参引用在调用处即绑定实参。

</details>

### 练习 2（难度 ★★★）

给定 `int x = 5; int& r = x; int* p = &x;`，依次执行 `r = 10; *p = 20;` 后 `x` 的值是多少？
用本书「批 L」的实证说明：引用在汇编层为何与被引用对象共享同一地址（零运行时开销）。

<details><summary>答案与解析</summary>

`x == 20`。`r` 和 `*p` 都直接寻址 `x` 的内存，没有任何"引用对象"被创建。
GCC 15.3.0 下 `r = 10` 编译为 `mov DWORD PTR [rbp-4], 10`，与直接写 `x` 的指令完全相同——引用在优化后**不占存储、无间接层**。

```cpp
int x = 5; int& r = x; int* p = &x;
r = 10;      // mov DWORD PTR [rbp-4], 10
*p = 20;     // mov DWORD PTR [rbp-4], 20
```

[标准] 标准不规定引用的实现，但要求其与对象行为等价；主流 ABI 直接用指针底层实现，优化后常完全消除。

</details>

### 练习 3（难度 ★★★★）

C++ **没有** `std::optional<T&>`（引用不能重绑定）。请基于裸指针实现一个 `optional_ref<T>`：
支持 `has_value()` / `value()` / `reset()`，构造时禁止空引用，并在一处故意误用触发未定义行为，指出问题。

<details><summary>答案与解析</summary>

```cpp
template <class T>
struct optional_ref {
    T* p;                              // 非空 invariant
    explicit optional_ref(T& r) : p(&r) {}
    bool has_value() const { return p != nullptr; }
    T& value() const { return *p; }    // 前置条件: has_value()
    void reset() { p = nullptr; }      // 破坏 invariant!
};
int main() {
    int x = 1;
    optional_ref<int> o(x);
    o.reset();                         // 误用: 此后 p==nullptr
    (void)o.value();                  // UB: 解引用空指针
}
```

陷阱：`reset()` 把 `p` 置空，但 `value()` 未检查——调用方越过 `has_value()` 直接 `value()` 即 UB。
工业写法应在 `value()` 内 `assert(p)` 或抛 `bad_optional_access`。

[标准] 引用必须在定义时绑定且不可重绑定；故 `optional<T&>` 被标准明确排除（用指针或 `std::reference_wrapper` 替代）。

</details>
''',

"ch27": r'''## 自测练习（Exercises）

> 以下题目用于自测掌握程度；答案折叠于每题下方，建议先独立作答。

### 练习 1（难度 ★★）

用 `static_cast` 完成 `double→int` 截断与 `int→double` 提升，指出哪一步会丢失信息、是否触发警告。

<details><summary>答案与解析</summary>

`int→double` 是拓宽，值保真（但大整数超过 2^53 会失精度，非本题范围）。
`double→int` 是收缩，**截断小数**且可能溢出——这是唯一的信息/UB 风险点，应开 `-Wfloat-conversion -Wconversion`。

```cpp
double d = 3.9;
int a = static_cast<int>(d);   // 3, 截断; -Wfloat-conversion 会警告
int b = 7;
double e = static_cast<double>(b); // 7.0, 保真
```

[标准] `static_cast` 执行良定义的数值转换；窄化转换在列表初始化 `{ }` 中被禁止，但在 `static_cast` 中允许（仅警告）。

</details>

### 练习 2（难度 ★★★）

何时**必须**用 `reinterpret_cast`？给出嵌入式内存映射 IO 读取一个 32 位状态寄存器的合理用例，
并指出它在严格别名规则下的未定义行为边界。

<details><summary>答案与解析</summary>

内存映射寄存器地址是硬件固定的整数，必须用 `reinterpret_cast` 把整数地址转为指针：

```cpp
volatile uint32_t* const STATUS = reinterpret_cast<volatile uint32_t*>(0x4002'1000);
uint32_t s = *STATUS;          // 读硬件寄存器
```

UB 边界：`reinterpret_cast` 得到的指针只有在"该地址确实存在一个同类型对象"时才合法访问。
把 `float*` 强转为 `int*` 去读位模式违反严格别名（见 ch42），应改用 `std::bit_cast` 或 `memcpy`。

[标准] `reinterpret_cast` 转换指针/整数；其结果的可解引用性受"对象模型 + 严格别名"约束，滥用即 UB。

</details>

### 练习 3（难度 ★★★★）

`dynamic_cast` 在虚继承下为何比普通单继承更慢（涉及 vtable thunk）？
写一个多重继承下 `dynamic_cast<Derived*>(base_ptr)` 返回 `nullptr` 的 case，并解释原因。

<details><summary>答案与解析</summary>

虚继承中派生类到虚基类的偏移**运行时才能确定**（取决于完整对象布局），`dynamic_cast`
需沿 vtable 的 RTTI 信息做路径查找并可能调用调整 thunk（见 ch49 实证）。
返回 `nullptr` 的典型情况：基类指针实际指向一个**不相关分支**的对象。

```cpp
struct B { virtual ~B() = default; };
struct D1 : B {};
struct D2 : B {};
struct Most : D1, D2 {};   // B 被继承两次(非虚)
B* p = new D2;             // p 指向 D2 那一支的 B 子对象
D1* q = dynamic_cast<D1*>(p); // nullptr: p 并不指向 D1 分支
```

[标准] `dynamic_cast` 对指针在失败时为 `nullptr`、对引用抛 `std::bad_cast`；跨虚继承布局需 RTTI 路径解析。

</details>
''',

"ch41": r'''## 自测练习（Exercises）

> 以下题目用于自测掌握程度；答案折叠于每题下方，建议先独立作答。

### 练习 1（难度 ★★）

`std::unique_ptr` 与 `std::shared_ptr` 的所有权语义有何本质区别？
写一个工厂 `make_node()` 返回 `unique_ptr<Node>`，调用方应如何"转移"而非"共享"所有权？

<details><summary>答案与解析</summary>

`unique_ptr` 独占所有权（不可拷贝、可移动，零控制块开销）；`shared_ptr` 共享所有权（引用计数，控制块分配）。
工厂返回 `unique_ptr`，调用方用 `std::move` 接收转移；若想共享则 `std::shared_ptr<std::unique_ptr 不可>`——直接返回 `shared_ptr` 或用 `std::move` 构造 `shared_ptr`。

```cpp
#include <memory>
struct Node { int v; };
std::unique_ptr<Node> make_node(int v) { return std::make_unique<Node>(Node{v}); }
int main() {
    auto a = make_node(1);          // 拥有
    auto b = std::move(a);          // 转移; a 现在为空
}
```

[标准] `unique_ptr`  movable-only；`make_unique`(C++14) 异常安全且避免裸 `new`。

</details>

### 练习 2（难度 ★★★）

为何 `shared_ptr` 的**循环引用**会导致内存泄漏？画一个 `A ↔ B` 双向 `shared_ptr` 结构，
并改成 `weak_ptr` 打破循环。

<details><summary>答案与解析</summary>

```cpp
struct A; struct B;
struct A { std::shared_ptr<B> b; ~A(){/*不会跑*/} };
struct B { std::shared_ptr<A> a; };
auto pa = std::make_shared<A>();   // use_count(A)=1
auto pb = std::make_shared<B>();   // use_count(B)=1
pa->b = pb; pb->a = pa;            // 互相 +1 -> 双方引用计数停在有环状态
// 离开作用域: pa/pb 析构各 -1, 但计数仍 >=1, 对象永不释放 -> 泄漏
```

修复：`struct B { std::weak_ptr<A> a; };` —— `weak_ptr` 不增加强引用计数，析构时 `B` 先释放，
其 `weak_ptr` 自动失效，`A` 随后释放。

[标准] `weak_ptr` 是 `shared_ptr` 的观察者，不拥有对象；`lock()` 原子尝试提升为 `shared_ptr`。

</details>

### 练习 3（难度 ★★★★）

`std::make_shared<T>` 相比 `std::shared_ptr<T>(new T)` 为何更快且更安全？
再写一个用**自定义 deleter** 管理 `std::FILE*` 的例子，并指出 `enable_shared_from_this` 的生命周期陷阱。

<details><summary>答案与解析</summary>

`make_shared` 把"控制块 + 对象"**一次性分配**（一次堆分配、更好缓存局部性），且不会因
`f(shared_ptr<T>(new T), g())` 的参数求值顺序导致泄漏；后者是两次分配。

```cpp
#include <memory>
#include <cstdio>
auto file = std::shared_ptr<FILE>(std::fopen("log.txt","w"),
                                  [](FILE* f){ if(f) std::fclose(f); }); // 自定义 deleter
// 即使异常离开作用域, fclose 也会被调用
```

陷阱：`enable_shared_from_this::shared_from_this()` 要求对象**已**被 `shared_ptr` 拥有；
在构造函数内或栈上对象调用会得到 `bad_weak_ptr` 或 UB。

[标准] `make_shared`(C++11) 单分配; `shared_ptr` deleter 保存在控制块中。

</details>
''',

"ch47": r'''## 自测练习（Exercises）

> 以下题目用于自测掌握程度；答案折叠于每题下方，建议先独立作答。

### 练习 1（难度 ★★）

写一个基类 `Shape` 含 `virtual double area()`，派生 `Circle` 与 `Rect`，用基类指针容器演示多态分发。
结合本书实证说明：一次虚调用在汇编层发生了什么（vtable 查找）。

<details><summary>答案与解析</summary>

```cpp
#include <iostream>
#include <vector>
#include <memory>
struct Shape { virtual double area() const = 0; virtual ~Shape()=default; };
struct Circle : Shape { double r; Circle(double r):r(r){} double area() const override { return 3.14159*r*r; } };
struct Rect   : Shape { double w,h; Rect(double w,double h):w(w),h(h){} double area() const override { return w*h; } };
int main(){
    std::vector<std::unique_ptr<Shape>> v;
    v.push_back(std::make_unique<Circle>(2));
    v.push_back(std::make_unique<Rect>(3,4));
    for (auto& s : v) std::cout << s->area() << '\n';
}
```

汇编层：调用 `s->area()` 编译为 `mov rax, [rsi]`（取 vtable 指针）→ `call [rax+offset]`（查虚函数槽）。
本书批 L/ASM 实证记录过 vtable 槽调用 `operator[]` 式的间接跳转。

[标准] 虚函数经 vtable 间接分发；override 必须签名一致（C++11 起建议显式 `override`）。

</details>

### 练习 2（难度 ★★★）

为何在**构造函数体内**调用虚函数不会触发动态绑定（不会调到派生类 override）？给出输出并解释。

<details><summary>答案与解析</summary>

```cpp
#include <iostream>
struct Base { Base(){ f(); } virtual void f(){ std::cout << "Base::f\n"; } };
struct Der : Base { Der():Base(){} void f() override { std::cout << "Der::f\n"; } };
int main(){ Der d; }   // 输出 "Base::f", 不是 "Der::f"
```

原因：对象在基类构造期间，其动态类型是 `Base`——vtable 指针此刻指向 `Base` 的 vtable，
派生类子对象尚未构造。标准明确规定构造/析构期间虚调用绑定到当前正在构造的类。

[标准] 在构造/析构函数中，虚函数调用绑定到当前构造/析构的类，不向下分发。

</details>

### 练习 3（难度 ★★★★）

CRTP 静态多态 vs 虚函数动态多态：各写一个 `add` 示例，指出前者零虚表开销但失去运行时异构，并说明何时选哪个。

<details><summary>答案与解析</summary>

```cpp
// 动态多态: 运行时异构, 有 vtable + 间接调用开销
struct Addable { virtual int add(int)=0; };
// 静态多态(CRTP): 编译期绑定, 无 vtable, 但容器必须同类型
template <class D> struct AddableCrtp { int add(int x){ return static_cast<D*>(this)->impl(x); } };
struct IntA : AddableCrtp<IntA> { int impl(int x){ return x+1; } };
```

选 CRTP：性能敏感、类型在编译期确定（如数值库 Eigen）；选虚函数：需要运行时多态、异构容器（如插件系统）。

[标准] CRTP 把虚调用转为静态分发（见 ch51 实证）；代价是失去运行时类型擦除能力。

</details>
''',

"ch77": r'''## 自测练习（Exercises）

> 以下题目用于自测掌握程度；答案折叠于每题下方，建议先独立作答。

### 练习 1（难度 ★★）

解释 `reserve(1000)` 后再 `push_back` 1000 次的复杂度；对比**不** reserve 时发生的扩容拷贝次数（假设 2× 扩容）。

<details><summary>答案与解析</summary>

`reserve(1000)` 一次分配够用，`push_back` 1000 次全部 O(1) 追加，总 **O(n)** 无重分配。
不 reserve（2× 扩容）：容量走 1→2→4→…→1024，元素被**整体拷贝** log2(1000)≈10 次，
总拷贝 ~1000+500+250+…≈2000 次移动，明显更慢且可能重复构造/析构。

```cpp
std::vector<int> a; a.reserve(1000);
for (int i=0;i<1000;++i) a.push_back(i);   // 0 次重分配
```

[标准] `reserve` 改变 `capacity` 不触发元素构造；扩容是"分配新缓冲 + 移动/拷贝 + 释放旧缓冲"。

</details>

### 练习 2（难度 ★★★）

写出在 `for` 循环中 `v.push_back` 导致**迭代器失效**的 bug，并给出两种修复（用索引 / 先 reserve）。

<details><summary>答案与解析</summary>

```cpp
// BUG: 扩容使 it 失效, 行为未定义
std::vector<int> v{1,2,3};
for (auto it = v.begin(); it != v.end(); ++it) v.push_back(*it);
// FIX 1: 用索引, end() 每次重算
for (size_t i = 0; i < v.size(); ++i) v.push_back(v[i]);
// FIX 2: 先 reserve 使 push_back 不扩容(迭代器仍可能因 size 变化需重算, 但地址稳定)
v.reserve(v.size()*2 + 4);
```

注：即使 reserve 后地址稳定，逻辑上 `end()` 也变了——索引法最稳妥。

[标准] `push_back` 触发扩容会使所有迭代器/引用/指针失效；未扩容时仅 `end()` 失效。

</details>

### 练习 3（难度 ★★★★）

实现 `erase_remove_if` 惯用法删除所有偶数；并解释 `vector<bool>` 的位压缩特化陷阱（proxy reference）。

<details><summary>答案与解析</summary>

```cpp
std::vector<int> v{1,2,3,4,5,6};
v.erase(std::remove_if(v.begin(), v.end(), [](int x){ return x%2==0; }), v.end());
// v == {1,3,5}
```

`vector<bool>` 把每个 bool 压成 1 bit，其 `operator[]` 返回**代理对象**而非 `bool&`：
不能 `auto& b = vb[0];`（编译失败），不能取地址，与"容器存 T 则 `T&` 可绑定"的直觉冲突。
需要真实 bool 语义时用 `std::vector<char>` 或 `std::bitset`/`dynamic_bitset`。

[标准] `vector<bool>` 是显性特化，元素非独立地址able 对象；属历史设计失误，工业代码慎用。

</details>
''',

"ch78": r'''## 自测练习（Exercises）

> 以下题目用于自测掌握程度；答案折叠于每题下方，建议先独立作答。

### 练习 1（难度 ★★）

对比 `deque` 与 `vector` 在**头部插入**的复杂度；用 `deque` 实现一个先进先出的队列。

<details><summary>答案与解析</summary>

`vector::insert(begin())` 要把全部元素后移 → **O(n)**；`deque::push_front` 只填当前头块、
必要时分配新块 → **摊还 O(1)**。`deque` 天然适合双端队列。

```cpp
#include <deque>
std::deque<int> q;
q.push_back(1); q.push_back(2);   // 入队尾
int head = q.front(); q.pop_front(); // 出队头 O(1)
```

[标准] `deque` 由分段连续缓冲区组成（见 ch78 批 L 实证），头/尾插入均摊 O(1)。

</details>

### 练习 2（难度 ★★★）

为何 `deque` 随机访问仍是 O(1) 但带"双间接"常数开销？结合批 L 实证中 `sar rdx, 0x7` 的分块映射解释。

<details><summary>答案与解析</summary>

`deque` 用"指针数组(map) + 定长块(512B)"两层结构。`operator[]` 先算块号 `i / 512`（`sar rdx, 0x7` 即 ÷128 元素的移位，取决于元素大小）去 map 查块指针，再算块内偏移 `i % 512`：
两次内存访问 vs `vector` 一次。故仍是 O(1)，但常数更大、缓存局部性弱于 `vector`。

```
block = map[ i >> 7 ];        // 第一跳: 取块基址
elem  = block[ i & 0x7f ];    // 第二跳: 块内索引
```

[标准] `deque` 随机访问摊还 O(1)，但比 `vector` 多一次间接；无 `data()` 连续视图。

</details>

### 练习 3（难度 ★★★★）

用 `deque` 实现**单调队列**（滑动窗口最大值），分析窗口滑动的均摊复杂度；并对比用 `vector` 的代价。

<details><summary>答案与解析</summary>

```cpp
// 维护双端队列存"候选最大值下标", 队首为当前窗口最大
std::deque<int> dq;
for (int i = 0; i < n; ++i) {
    while (!dq.empty() && a[dq.back()] <= a[i]) dq.pop_back(); // 淘汰更小者
    dq.push_back(i);
    if (dq.front() == i - k) dq.pop_front();                    // 移出窗口
    if (i >= k-1) out.push_back(a[dq.front()]);
}
```

每个元素最多入队、出队各一次 → 均摊 **O(1)/元素**，总 O(n)。
若用 `vector`：头部 `pop_front` 是 O(n) 拷贝，整体退化到 O(n·k)。

[标准] 单调队列是"双端 + 单调性"的经典技巧；`deque` 的 O(1) 双端弹出是关键。

</details>
''',

"ch93": r'''## 自测练习（Exercises）

> 以下题目用于自测掌握程度；答案折叠于每题下方，建议先独立作答。

### 练习 1（难度 ★★）

用 `std::thread` 并行求 `0..N` 的和；指出若改用 `detach()` 而非 `join()` 会有什么风险，
并说明 `std::jthread`(C++20) 如何自动避免它。

<details><summary>答案与解析</summary>

```cpp
#include <thread>
#include <vector>
long sum = 0;
void part(int lo, int hi){ long s=0; for(int i=lo;i<hi;++i) s+=i; sum += s; } // 注意: 这里有竞争!
int main(){
    std::thread t(part, 0, 1000);
    t.join();   // 等它结束再继续
    // t.detach(); // 危险: 线程可能访问已销毁的栈/全局, 或主线程先退出
}
```

`detach()` 后线程在后台独立运行，若主线程先退出或引用了局部变量 → 悬垂/UB。
`std::jthread` 析构时**自动 `request_stop()` + `join()`**，杜绝忘记 join 的泄漏。

[标准] `thread` 析构若仍 joinable 则 `std::terminate`；`jthread`(C++20) 自动 join。

</details>

### 练习 2（难度 ★★★）

`std::async` 返回的 `future` 在析构时为何会**阻塞**？写一个"忘记保存 future"导致意外同步的 bug。

<details><summary>答案与解析</summary>

```cpp
void fire_and_forget(){
    std::async(std::launch::async, [](){ heavy_work(); }); // future 是临时对象
} // 此处 future 析构 -> 阻塞等待 heavy_work 完成! 本想异步, 实际变同步
```

`std::async` 的 `future` 析构会等待共享状态就绪（标准规定），所以上面"即发即忘"反而同步了。
修复：真的想后台跑就用 `std::thread` 或显式 `std::packaged_task` + 长期持有 `future`。

[标准] `async` 返回的 `future` 析构行为：若共享状态未就绪则阻塞（阻塞析构语义）。

</details>

### 练习 3（难度 ★★★★）

两个线程对 `int counter` 各做 `++counter` 十万次，结果为何小于 20 万（丢失更新）？
用 `std::atomic<int>` 修复，并指出相比 `std::mutex` 的取舍（含 false sharing）。

<details><summary>答案与解析</summary>

```cpp
#include <atomic>
std::atomic<int> counter{0};                 // 原子 RMW, 无竞争
void worker(){ for(int i=0;i<100000;++i) ++counter; } // 正确累加到 200000
```

`++counter`（非原子）是"读-改-写"三步，线程交错导致写覆盖 → 丢失更新。
`atomic` 用 `lock xadd` 单指令完成；比 `mutex` 更轻，但若多个原子变量落在**同一缓存行**（false sharing），
会因缓存行在核间反复失效而变慢——此时应 padding 隔离（见 ch110/ch111 无锁章节）。

[标准] 数据竞争是 UB；`atomic` 提供无锁 RMW，`mutex` 提供临界区；false sharing 需缓存行对齐。

</details>
''',

"ch96": r'''## 自测练习（Exercises）

> 以下题目用于自测掌握程度；答案折叠于每题下方，建议先独立作答。

### 练习 1（难度 ★★）

`std::sort` 与 `std::stable_sort` 的稳定性有何差异？对一个 `(年龄, 姓名)` 的 pair 序列排序，
演示稳定性如何保留同年龄元素的原有相对顺序。

<details><summary>答案与解析</summary>

`sort` **不保证**相等元素顺序（可能重排）；`stable_sort` **保持**相等元素的原有相对顺序。
例：输入 `(20,"Bob"), (20,"Ann"), (18,"Zoe)`，按年龄排后 `stable_sort` 得
`(18,"Zoe"), (20,"Ann"), (20,"Bob)`（Ann 仍在 Bob 前）；`sort` 可能变成 `(20,"Bob"),(20,"Ann")`。

```cpp
std::vector<std::pair<int,std::string>> v{{20,"Bob"},{20,"Ann"},{18,"Zoe"}};
std::stable_sort(v.begin(), v.end(), [](auto&a,auto&b){ return a.first<b.first; });
```

[标准] `stable_sort` 复杂度上限 O(n·log²n)，内存不足时退化但仍稳定；`sort` 平均 O(n log n)。

</details>

### 练习 2（难度 ★★★）

introsort（introspective sort）为何混合 quick / heap / insertion？
解释它在什么条件下从 quick 切换到 heap（递归深度超限），这解决了快排的什么最坏情况？

<details><summary>答案与解析</summary>

快排平均 O(n log n) 但**已排序/几乎有序**输入会退化到 O(n²)。introsort 监控递归深度：
当深度超过 `2·log2(n)` 时，改调用 `std::partial_sort`（heap sort，严格 O(n log n)）收尾，
避免快排的最坏情况；小区间（如 ≤16）切到 insertion sort（小数据常数更小）。

```
if (depth_limit == 0)      heap_sort(range);   // 防 O(n^2)
else if (small(range))     insertion_sort(range);
else                       quick_sort_partition + recurse(depth_limit-1);
```

[标准] introsort = introspective sort；libstdc++ `std::sort` 即此实现（见 ch96 附录 A 工业源码）。

</details>

### 练习 3（难度 ★★★★）

求 top-k 与中位数时，全排序是浪费的。分别用 `std::partial_sort` 与 `std::nth_element` 实现"找中位数"，
对比复杂度，并说明 introselect 的 pivot 选择为何影响最坏情况。

<details><summary>答案与解析</summary>

```cpp
// 方法 A: partial_sort -> O(n log k), 这里 k=n/2
std::vector<int> a = /*...*/;
std::partial_sort(a.begin(), a.begin()+a.size()/2, a.end());
int medA = a[a.size()/2-1];

// 方法 B: nth_element -> O(n), 仅分区, 不排序
std::vector<int> b = a;
std::nth_element(b.begin(), b.begin()+b.size()/2, b.end());
int medB = b[b.size()/2];
```

`partial_sort` 把前 k 个排好（O(n log k)）；`nth_element` 只保证第 k 个就位、左右分区（O(n)）。
找中位数应用 `nth_element`。introselect 在快排式选择中同样用"深度超限转 heap select"防止 O(n²)。

[标准] `nth_element` 实现 introselect（median-of-medians 或 introspective pivot）；平均/最坏视实现而定。

</details>
''',
}

# ---- usage demonstrations (append after exercises) ----
DEMOS = {
"ch20": r'''
## 附录：用法演绎 — 返回引用还是指针？

> 场景：设计一个配置读取 API，调用方要拿到一个"可能很大、且不应被拷贝"的对象。

**步骤 1：朴素值返回（错误起点）**

```cpp
Config load_config();              // 返回副本: 大对象拷贝 + 可能异常
Config c = load_config();          // 一次完整拷贝
```

问题：每次调用都拷贝整个 `Config`（可能有数百字段/嵌套容器），且若函数内部抛异常，半构造副本难处理。

**步骤 2：返回 `const` 引用（悬垂风险）**

```cpp
const Config& load_config();       // 若内部返回局部变量的引用 -> 悬垂!
const Config& c = load_config();   // c 指向已销毁对象 -> UB
```

陷阱：引用必须绑定到**调用方或更长生命周期**的对象。返回局部变量引用是经典 UB。

**步骤 3：返回指针表达"可空"**

```cpp
Config* load_config();             // nullptr 表示"未找到/失败"
Config* c = load_config();
if (c) use(*c);                    // 调用方必须判空
```

指针的语义是"可能没有"，调用方被迫判空——适合"查找可能失败"的场景。

**步骤 4：工业最终形态（所有权转移）**

```cpp
std::unique_ptr<Config> load_config();   // 转移所有权, 零拷贝, 无悬垂
auto c = load_config();                  // 拥有, 离开作用域自动释放
if (c) use(*c);
```

**结论**：返回值（拷贝，小对象）/ `const&`（借出长生命周期对象）/ 指针（可空查询）/ `unique_ptr`（转移所有权）。
选型的唯一依据是**生命周期与可空性**，而非习惯。

**工程含义**：引用≠指针的"语法糖"，而是"非空别名"的契约；在 API 边界滥用引用会埋下悬垂雷。
''',

"ch27": r'''
## 附录：用法演绎 — 类型双关（type punning）的正确与错误姿势

> 场景：网络/序列化中常需查看一个 `float` 的 32 位 IEEE-754 位模式（或反过来构造）。

**步骤 1：错误——通过 union 双关（UB）**

```cpp
union U { float f; uint32_t u; };
U x; x.f = 1.0f;
uint32_t bits = x.u;             // C++ 中读取非活跃成员是未定义行为
```

虽然很多编译器"恰好"支持（type-punning union 是 GCC 扩展），但它**不是标准行为**，换编译器/开启严格别名优化即崩。

**步骤 2：错误——`reinterpret_cast` 强转指针（违反严格别名）**

```cpp
float f = 1.0f;
uint32_t bits = *reinterpret_cast<uint32_t*>(&f);  // 违反严格别名 -> UB, -fstrict-aliasing 下可能被优化错
```

编译器假设 `float*` 与 `uint32_t*` 不会指向同一内存，可能重排/缓存，结果不可信。

**步骤 3：正确——`std::memcpy`（零开销且标准合法）**

```cpp
float f = 1.0f; uint32_t bits;
std::memcpy(&bits, &f, sizeof(bits));   // 标准明确允许, 编译器优化为单条 mov
```

`memcpy` 是唯一被标准许可的"重新解释对象表示"方式；现代编译器会把它优化成一条寄存器传送，**零运行时成本**。

**步骤 4：正确——`std::bit_cast`（C++20，最优雅）**

```cpp
uint32_t bits = std::bit_cast<uint32_t>(1.0f);   // 编译期可求值, 类型安全
```

**结论**：需要位模式互看时，优先 `std::bit_cast`(C++20) 或 `memcpy`；`reinterpret_cast`/`union` 双关仅在明确 UB 边界内、且确认编译器扩展支持时使用。

**工程含义**：严格别名规则（ch42）不是学术细节——它直接决定你的序列化/网络代码在 `-O2` 下是否正确。
''',

"ch41": r'''
## 附录：用法演绎 — 从裸指针迁移到 `unique_ptr`

> 场景：重构一段老代码，原接口返回裸 `T*`（调用方负责 `delete`），频繁出现泄漏与双重释放。

**步骤 1：原始代码（双重释放雷区）**

```cpp
Buffer* create_buffer(size_t n) { return new Buffer(n); }
// 调用方:
Buffer* b = create_buffer(1024);
use(b);
delete b;                 // 若 use() 内部也 delete -> 双重释放; 若抛异常 -> 泄漏
```

**步骤 2：用 `unique_ptr` + 自定义 deleter 包装**

```cpp
auto create_buffer(size_t n) {
    return std::unique_ptr<Buffer>(new Buffer(n));   // 或 make_unique
}
auto b = create_buffer(1024);   // 离开作用域自动释放, 异常安全
use(b.get());                   // .get() 仅借出裸指针, 不转移所有权
```

**步骤 3：工厂模式转移所有权**

```cpp
std::unique_ptr<Buffer> b = create_buffer(1024);  // 拥有
std::unique_ptr<Buffer> b2 = std::move(b);        // 显式转移; b 变空
// 不能 copy: auto b3 = b2; 编译失败 -> 编译期杜绝双重释放
```

**步骤 4：管理非内存资源（FILE*）**

```cpp
auto f = std::unique_ptr<FILE, decltype(&fclose)>(fopen("x","r"), fclose);
// 文件句柄随 f 析构自动 fclose, 异常安全
```

**结论**：`unique_ptr` 把"所有权"编码进类型系统——可移动不可拷贝，编译期阻止双重释放；
`.get()` 仅用于需要裸指针的旧 API，绝不从中转交生命周期管理。

**工程含义**：裸 `new/delete` 在 modern C++ 中基本只应出现在 `make_unique/make_shared` 内部；
所有权语义不清是 C++ 历史泄漏的头号来源。
''',

"ch47": r'''
## 附录：用法演绎 — 设计一个可扩展的插件系统

> 场景：主程序要在**运行时**按名字加载不同算法实现（图像处理滤镜、压缩器等），且易于第三方扩展。

**步骤 1：定义抽象接口（多态基类）**

```cpp
struct Filter {
    virtual ~Filter() = default;
    virtual Image apply(const Image&) const = 0;
    virtual const char* name() const = 0;
};
```

**步骤 2：派生具体滤镜（override 虚函数）**

```cpp
struct Grayscale : Filter {
    Image apply(const Image& i) const override { /* ... */ return gray; }
    const char* name() const override { return "grayscale"; }
};
```

**步骤 3：工厂注册 + 运行时按名创建（多态分发）**

```cpp
std::map<std::string, std::function<std::unique_ptr<Filter>()>> registry;
registry["grayscale"] = [] { return std::make_unique<Grayscale>(); };
// 运行时:
auto f = registry.at(user_choice)();   // 动态多态: 不知道具体类型也能调用
Image out = f->apply(src);              // 经 vtable 分发到正确实现
```

**步骤 4：对比 CRTP 静态策略（性能优先时）**

```cpp
template <class Impl> struct FilterCrtp {
    Image apply(const Image& i) const { return static_cast<const Impl*>(this)->impl(i); }
};
struct GrayscaleS : FilterCrtp<GrayscaleS> { Image impl(const Image&) const { /*...*/ } };
```

`FilterCrtp` 把 `apply` 编译期内联（无 vtable 间接、可被优化掉），但**容器必须同类型**——
无法把 `GrayscaleS` 和 `SepiaS` 放进同一个 `vector<FilterCrtp<??>>`。

**结论**：需要运行时异构插件 → 虚函数多态（灵活、有 vtable 开销）；
性能热点且类型编译期已知 → CRTP（零开销、失去异构）。两者不是替代关系，是按场景取用。

**工程含义**：多态不是"面向对象必用"，而是"异构 + 运行时分发"需求的答案；误用 CRTP 会锁死扩展性。
''',

"ch77": r'''
## 附录：用法演绎 — 百万元素构建的性能对决

> 场景：从外部数据源读入 1,000,000 条记录构建一个 `vector`，对比四种写法的耗时差距。

**步骤 1：无 reserve 逐步 `push_back`（最慢）**

```cpp
std::vector<Rec> v;
for (auto& r : source) v.push_back(r);   // 容量 1->2->4->...->1048576, 约 20 次重分配 + 整体搬迁
```

每次扩容都分配新缓冲并把旧元素**移动**过去；总搬移量 ≈ `n·log2(n)`，且反复申请/释放内存。

**步骤 2：先 `reserve` 再 `push_back`（快得多）**

```cpp
std::vector<Rec> v; v.reserve(source.size());   // 1 次分配到位
for (auto& r : source) v.push_back(r);          // 零重分配
```

**步骤 3：用 `emplace_back` 避免临时对象（更快）**

```cpp
v.reserve(source.size());
for (auto& r : source) v.emplace_back(r.id, r.name, r.val); // 原地构造, 跳过一次拷贝/移动
```

**步骤 4：容量收缩（若之后不再增长）**

```cpp
v.shrink_to_fit();   // 释放多余 capacity, 降低内存占用(可能触发一次搬迁)
```

**量化对照（示意，i7/`-O2`）**：

| 写法 | 重分配次数 | 相对耗时 |
|------|:--:|:--:|
| 无 reserve + push_back | ~20 | 1.00× (基线) |
| reserve + push_back | 0 | ~0.35× |
| reserve + emplace_back | 0 | ~0.30× |

结合 ch77 扩容策略：`vector` 默认约 **1.5×–2×** 几何增长，预 `reserve` 直接消灭扩容抖动。

**结论**：已知规模必 `reserve`；能用 `emplace_back` 就别 `push_back(临时对象)`；增长结束后 `shrink_to_fit` 回收。

**工程含义**：`vector` 的"慢"几乎总是"忘了 reserve"造成的，不是 `vector` 本身慢。
''',

"ch78": r'''
## 附录：用法演绎 — 生产者-消费者双端缓冲的选型

> 场景：一个日志/任务队列，头部被频繁 `pop`、尾部被频繁 `push`，元素生命周期短。

**步骤 1：若误用 `vector`（头部删除 O(n)）**

```cpp
std::vector<Task> q;
q.push_back(t);          // 尾插 O(1)
q.erase(q.begin());      // 头删 O(n): 后续所有元素前移
```

高吞吐下每次头删都搬动整个队列 → 性能随队列长度线性恶化。

**步骤 2：改用 `deque`（头尾均摊 O(1)）**

```cpp
std::deque<Task> q;
q.push_back(t);          // 尾 O(1)
q.pop_front();           // 头 O(1): 仅释放头块一个槽, 不搬移其余元素
```

deque 的块结构让头删只动"头块"，其余块原地不动——无全局搬迁抖动。

**步骤 3：何时 deque 反而**不如** vector？**

```cpp
// 随机访问密集 + 缓存敏感的数值计算:
for (size_t i=0;i<n;++i) sum += q[i];   // deque 每次访问 2 次间接(map查块+块内)
// vector 仅 1 次直接寻址, 且连续内存对预取友好 -> 更快
```

**结论**：双端频繁增删（队列、滑动窗口、撤销栈）→ `deque`；
尾部增删 + 随机访问密集 + 缓存敏感 → `vector`。不要因为"deque 也能随机访问"就无脑替换 vector。

**工程含义**：容器选型看**访问模式**而非功能列表；deque 以"双端 O(1) + 无 realloc 抖动"换"随机访问常数更大 + 缓存更差"。
''',

"ch93": r'''
## 附录：用法演绎 — 并行求和的数据竞争现场

> 场景：把 0..N 的求和拆到 4 个线程，最后合并。演示竞争如何产生、如何修。

**步骤 1：朴素共享计数器（数据竞争 → 错误结果）**

```cpp
long counter = 0;
auto worker = [&](){ for(int i=0;i<50000;++i) ++counter; }; // 读-改-写非原子
std::thread t1(worker), t2(worker), t3(worker), t4(worker);
t1.join(); t2.join(); t3.join(); t4.join();
// 期望 200000, 实际常 < 200000: 写覆盖导致丢失更新 (UB)
```

`++counter` 编译为 `mov+add+mov`，线程交错使一次写被另一次覆盖。

**步骤 2：加 `std::mutex`（正确但较重）**

```cpp
long counter = 0; std::mutex m;
auto worker = [&](){ for(int i=0;i<50000;++i){ std::lock_guard<std::mutex> lk(m); ++counter; } };
// 正确, 但每次 ++ 都加锁 -> 串行化, 并行收益被锁吃掉
```

**步骤 3：改 `std::atomic<int>`（无锁、正确）**

```cpp
std::atomic<long> counter{0};
auto worker = [&](){ for(int i=0;i<50000;++i) ++counter; }; // lock xadd 单指令 RMW
// 结果严格 200000, 且无锁竞争开销远低于 mutex
```

**步骤 4：更好——每个线程私有计数，最后合并（无共享 → 无竞争）**

```cpp
std::vector<long> local(4, 0);
std::vector<std::thread> ts;
for (int t=0;t<4;++t) ts.emplace_back([&,t]{ for(int i=t*25000;i<(t+1)*25000;++i) local[t]+=i; });
for (auto& th : ts) th.join();
long total = std::accumulate(local.begin(), local.end(), 0L); // 无锁合并
```

**结论**：能避免共享就不共享（步骤 4 最快）；必须共享用 `atomic`（轻）而非 `mutex`（重）；
注意 false sharing——把 `local[t]` 放同一缓存行会互相失效，需 padding 隔离（见 ch110/111）。

**工程含义**：并行化的第一原则不是"加锁"，而是"减少共享"；atomic 解决正确性，架构解决性能。
''',

"ch96": r'''
## 附录：用法演绎 — top-k 与中位数的正确打开方式

> 场景：从 1,000,000 个数里取最大的 100 个，或求中位数。全排序是浪费的。

**步骤 1：朴素全排序（O(n log n)，绝大多数工作白做）**

```cpp
std::vector<int> a = read_million();
std::sort(a.begin(), a.end());          // 全部排好, 但只想要前 100 / 中间 1 个
auto topk = std::vector<int>(a.begin()+a.size()-100, a.end());
int median = a[a.size()/2];
```

**步骤 2：`std::partial_sort`（只排前 k，O(n log k)）**

```cpp
std::partial_sort(a.begin(), a.begin()+100, a.end()); // 前 100 就位且有序, 其余无序
// 比全排序少排 n-100 个元素
```

**步骤 3：`std::nth_element`（只分区，O(n) — top-k 与中位数的最优解）**

```cpp
// 找中位数: 只保证第 n/2 个就位, 左边都 <= 它, 右边都 >= 它
std::nth_element(a.begin(), a.begin()+a.size()/2, a.end());
int median = a[a.size()/2];

// 取最大 100: 以第 n-100 个为支点分区, 再 sort 尾部 100
std::nth_element(a.begin(), a.begin()+a.size()-100, a.end());
std::sort(a.begin()+a.size()-100, a.end());
```

**步骤 4：理解 introsort / introselect 的 pivot 保护**

`std::sort`/`nth_element` 内部用 introsort/introselect：正常快排式分区，但当递归深度超限（防已排序输入退化 O(n²)）时转 heap sort / heap select 兜底——保证严格 O(n log n) / O(n)。

**量化对照（示意）**：

| 需求 | 算法 | 复杂度 |
|------|------|------|
| 全有序 | `sort` | O(n log n) |
| 前 k 有序 | `partial_sort` | O(n log k) |
| 第 k 个就位 | `nth_element` | O(n) |

**结论**：只取极值/分位数 → `nth_element`；只要前 k 有序 → `partial_sort`；全排序才用 `sort`。
盲目 `sort` 取 top-k 是把 O(n) 问题做成了 O(n log n)。

**工程含义**：算法选型先看"我到底需要什么不变量"——多数 top-k/中位数场景根本不需要完全有序。
''',
}

def detect_eol(text):
    return "\r\n" if "\r\n" in text else "\n"

def main():
    for path, (key, _title) in TARGETS.items():
        full = os.path.join(ROOT, path)
        raw = open(full, encoding="utf-8").read()
        eol = detect_eol(raw)
        lines = raw.split(eol)
        # find '## 自测练习（Exercises）'
        anchor = None
        for i, l in enumerate(lines):
            if l.startswith("## 自测练习（Exercises）"):
                anchor = i
                break
        if anchor is None:
            print(f"[SKIP] {path}: no 自测练习 anchor found")
            continue
        # new tail = exercises + demo (no leading blank needed; sections separated by blank line)
        new_tail = EXERCISES[key].rstrip("\n") + eol + eol + DEMOS[key].lstrip("\n").rstrip("\n")
        # preserve any trailing blank lines style: append a single eol at very end
        new_lines = lines[:anchor] + new_tail.split("\n")
        out = eol.join(new_lines).rstrip("\n") + eol
        # ensure file ends with exactly one eol
        with open(full, "w", encoding="utf-8", newline="") as f:
            f.write(out)
        print(f"[OK] {path}: replaced lines {anchor+1}..EOF with exercises+demo ({len(new_lines)} total lines)")

if __name__ == "__main__":
    main()
