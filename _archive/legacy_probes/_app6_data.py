# -*- coding: utf-8 -*-
# APP6 注入数据：part04_memory 5 章(ch35/36/37/38/40) 习题重写 + 用法演绎附录
# 约定与 APP5 一致：每章值为「从 ### 练习 1 起的全部注入尾」，按
# "## 附录：用法演绎（从选型到落地）" 切分为 EX(习题) / APX(附录) 两部分。
# C++ 字符串内的换行写成 \\n（Python 解析后成为 C++ 的 \n）。

APP6 = {
"ch35": r"""### 练习 1（难度 ★★）

写一个小程序，分别打印全局变量、静态变量、局部变量、堆对象的地址，并据此说明 C++ 进程虚拟地址空间各段（.text / .data / .bss / heap / stack）的相对高低关系。

<details><summary>答案与解析</summary>

地址数值受 ASLR 随机化影响，但各存储期的相对区间稳定：代码与只读常量在最底；已初始化全局/静态在 .data、零初始化在 .bss；堆从低向高增长；栈从高向低增长，因此栈地址通常高于堆。

```cpp
#include <iostream>
int g = 1;          // .data
int gb;             // .bss
int main() {
    int l = 2;      // 栈
    int* h = new int(3);   // 堆
    static int s = 4;      // .data(已初始化静态)
    std::cout << "global .data : " << &g << "\n";
    std::cout << "global .bss  : " << &gb << "\n";
    std::cout << "static .data : " << &s << "\n";
    std::cout << "local  stack : " << &l << "\n";
    std::cout << "heap         : " << h << "\n";
    delete h;
}
```

[标准] 不同存储期的对象落在不同地址区间；栈向低地址、堆向高地址增长，二者相向扩张。

</details>

### 练习 2（难度 ★★★）

用 `offsetof` 打印一个含 `char/int/double` 成员的结构体各成员偏移，解释为何 `sizeof` 大于各成员字节之和。

<details><summary>答案与解析</summary>

对齐要求（alignment）使编译器在成员间插入填充（padding），保证每个成员按其对齐边界存放；`sizeof` 还需是整体对齐的倍数。

```cpp
#include <iostream>
#include <cstddef>
struct A { char c; int i; double d; };
int main() {
    std::cout << "sizeof(A) = " << sizeof(A) << "\n";
    std::cout << "offset c = " << offsetof(A, c) << "\n";
    std::cout << "offset i = " << offsetof(A, i) << "\n";
    std::cout << "offset d = " << offsetof(A, d) << "\n";
}
```

[标准] 成员大小之和 1+4+8=13，但 `int` 需 4 字节对齐、`double` 需 8 字节对齐，常见布局 `sizeof(A)=16` 或 `24`（含尾部填充）。

</details>

### 练习 3（难度 ★★★★）

写程序连续声明两个局部变量、连续 `new` 两个堆对象，分别打印其地址，验证"栈向低地址、堆向高地址"的增长方向。

<details><summary>答案与解析</summary>

局部变量 `b` 的地址通常低于 `a`（栈向下增长）；`new` 得到的 `p2` 通常高于 `p1`（堆向上增长）。

```cpp
#include <iostream>
int main() {
    int a = 0, b = 0;
    int* p1 = new int(0);
    int* p2 = new int(0);
    std::cout << "stack: &a=" << &a << " &b=" << &b << " (b 通常低于 a)\n";
    std::cout << "heap : p1=" << p1 << " p2=" << p2 << " (p2 通常高于 p1)\n";
    delete p1; delete p2;
}
```

[标准] 栈与堆相向扩张；一旦二者相遇即栈溢出/堆耗尽，这就是为什么大对象不应放在栈上。

</details>

## 附录：用法演绎（从选型到落地）

### 演绎 1：嵌入式固件如何规划 RAM（.bss vs 栈）

**场景**：你在写 STM32 固件的接收任务，需要一个 4KB 缓冲。若随手声明为局部数组，它会被放进栈——而 Cortex-M 默认栈仅 1~8KB，嵌套中断一来就溢出。

**常见错误**（朴素写法）：
```text
void rx_task() {
    uint8_t buf[4096];   // 4KB 落在栈上, 中断嵌套即 HardFault
    // ...
}
```

**修复**：把大缓冲提升为全局或静态，使其进入 .bss（启动即分配、不占栈）；或放进链接脚本指定的特定 RAM 区。

```cpp
#include <iostream>
#include <cstddef>
#include <cstdint>
// 错误: void rx_task(){ uint8_t buf[4096]; }
static uint8_t g_rx_buf[4096];   // 进 .bss, 启动即分配, 不占栈
int main() {
    std::cout << "g_rx_buf size = " << sizeof(g_rx_buf)
              << " (位于 .bss, 不占栈)\n";
}
```

**结论**：嵌入式固件中"大缓冲/长生命周期"对象应进 .bss/.data（全局或 static）；只有小块、短生命周期的临时变量才放栈。栈溢出在 MCU 上表现为随机 HardFault，极难复现。

### 演绎 2：栈溢出的检测与规避

**场景**：递归过深或局部大数组导致栈溢出，症状是随机崩溃，且只有在特定调用深度才触发。

**常见错误**（朴素写法）：
```text
char buf[1 << 20];          // 1MB 局部数组, 远超栈容量
void deep(int n){ deep(n+1); }  // 无终止递归, 必然溢出
```

**修复**：大对象改放堆（`std::vector`/智能指针，堆上只存 24B 句柄）；递归确保有终止条件；开 `-fstack-protector-strong` 让栈金丝雀在返回前检测破坏。

```cpp
#include <iostream>
#include <vector>
// 栈版本危险: char buf[1<<20];
int main() {
    std::vector<char> buf(1 << 20);   // 1MB 在堆, 栈仅 24B 句柄
    std::cout << "heap buffer size = " << buf.size() << "\n";
}
```

**结论**：栈容量有限且不可动态扩展；任何"大小可能较大或运行时确定"的对象都应落堆。链接脚本里划出 `.stack` 段并保留保护区，是定位栈溢出的最后一道防线。

""",

"ch36": r"""### 练习 1（难度 ★★）

写程序对比栈对象与堆对象的生命周期：在函数中创建栈对象与堆对象，观察函数返回后二者是否仍可访问、是否需要手动释放。

<details><summary>答案与解析</summary>

栈对象在离开作用域时自动析构；堆对象脱离创建它的作用域后依然存在，必须 `delete` 或交给智能指针管理，否则泄漏。

```cpp
#include <iostream>
struct T { ~T() { std::cout << "T destroyed\n"; } };
T* leak() { T* p = new T(); return p; }   // 堆对象: 返回后仍存在
void scope() { T s; }                      // 栈对象: 离开 scope() 自动析构
int main() {
    scope();
    T* p = leak();
    delete p;
}
```

[标准] 栈对象生命周期由作用域绑定；堆对象生命周期由 `delete` 显式控制，二者本质不同。

</details>

### 练习 2（难度 ★★★）

用 RAII 包装一段需要释放的资源（如堆对象），保证无论正常返回还是中途抛异常都不会泄漏。

<details><summary>答案与解析</summary>

`std::unique_ptr` 在析构时自动释放，异常栈展开时也会调用析构，从而提供异常安全的资源回收。

```cpp
#include <iostream>
#include <memory>
struct T { ~T() { std::cout << "released\n"; } };
void use() {
    auto p = std::make_unique<T>();   // 离开 use() 自动释放
    // 即使中间抛异常, unique_ptr 析构仍释放
}
int main() { use(); }
```

[标准] RAII 把"资源获取"绑定到对象生命周期，是 C++ 异常安全的基础 idiom。

</details>

### 练习 3（难度 ★★★★）

写程序粗略计时：一百万次"仅栈"的小操作 vs 一百万次"每次在堆上分配/释放一个小 vector"，说明堆分配的开销来源。

<details><summary>答案与解析</summary>

栈分配只是指针/栈槽移动（O(1) 指令）；堆分配要进入分配器、搜索空闲链表、可能系统调用，开销高 1~2 个数量级。

```cpp
#include <iostream>
#include <vector>
#include <chrono>
int main() {
    const int N = 1000000;
    auto t0 = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < N; ++i) { int x = i; (void)x; }
    auto t1 = std::chrono::high_resolution_clock::now();
    for (int i = 0; i < N; ++i) { std::vector<int> v(8); (void)v; }
    auto t2 = std::chrono::high_resolution_clock::now();
    auto d1 = std::chrono::duration_cast<std::chrono::microseconds>(t1 - t0).count();
    auto d2 = std::chrono::duration_cast<std::chrono::microseconds>(t2 - t1).count();
    std::cout << "stack-only : " << d1 << " us\n";
    std::cout << "heap-alloc : " << d2 << " us (远高于栈)\n";
}
```

[标准] 高频小对象分配应优先考虑栈、对象池或 `std::pmr`，避免反复进入通用分配器。

</details>

---

> **UB 实证库**：堆内存（释放后使用 / 双重释放）与栈内存（栈对象越界使用）的**真实 UB 代码 + GCC 警告 + 修复**，见 [附录 UB 反例库](../../Appendix/ub/README.md)（UB-01/02/03）。

## 附录：用法演绎（从选型到落地）

### 演绎 1：返回局部变量引用/指针 → 悬垂

**场景**：你写一个返回计算结果的函数，图省事返回局部变量的引用，调用方拿到后程序偶发读到垃圾值。

**常见错误**（朴素写法）：
```text
const int& bad() {
    int x = 42;
    return x;        // x 已销毁, 返回悬垂引用 -> UB
}
```

**修复**：需要传值就按值返回（拷贝/移动）；需要跨作用域生命周期才用智能指针管理堆对象。

```cpp
#include <iostream>
#include <memory>
// 错误: const int& bad(){ int x=42; return x; }
int good_val() { int x = 42; return x; }               // 按值返回
std::unique_ptr<int> good_ptr() { return std::make_unique<int>(42); }
int main() {
    std::cout << good_val() << "\n";
    std::cout << *good_ptr() << "\n";
}
```

**结论**：永远不要返回局部变量的引用或指针。返回值让编译器选择拷贝或移动；需要堆生命周期才用智能指针。

### 演绎 2：大小在运行时才确定的缓冲 → 选堆

**场景**：你要读入用户指定长度 N 的数据，无法用编译期常量声明数组。

**常见错误**（朴素写法）：
```text
int n = read_input();
char buf[n];              // VLA, 非标准且易栈溢出
```

**修复**：大小运行时确定就用 `std::vector`（或 `std::unique_ptr<T[]>`），在堆上按需分配。

```cpp
#include <iostream>
#include <vector>
int main() {
    int n = 1024;                       // 运行时确定的大小(此处以常量示意)
    std::vector<int> v(n);              // 堆上分配, 自动管理生命周期
    std::cout << "heap buffer = " << v.size() << " ints\n";
}
```

**结论**：栈只适合大小已知且较小、生命周期随作用域的对象；其余交给堆与容器/智能指针。

""",

"ch37": r"""### 练习 1（难度 ★★）

为某个类重载类域 `operator new` / `operator delete`，统计该类被分配的次数与字节数。

<details><summary>答案与解析</summary>

类域 `operator new` 优先于全局版本；在其中调用 `std::malloc` 并累计计数，即可观测该类全部分配。

```cpp
#include <iostream>
#include <cstdlib>
#include <new>
struct Counter {
    static long allocs, bytes;
    static void* operator new(std::size_t n) {
        allocs++; bytes += (long)n;
        return std::malloc(n);
    }
    static void operator delete(void* p, std::size_t) { std::free(p); }
};
long Counter::allocs = 0;
long Counter::bytes = 0;
int main() {
    auto* c = new Counter();
    delete c;
    std::cout << "allocs=" << Counter::allocs
              << " bytes=" << Counter::bytes << "\n";
}
```

[标准] 重载类域 `operator new/delete` 不影响 `sizeof`，仅改变该类的内存来源；`new`/`delete` 必须配对。

</details>

### 练习 2（难度 ★★★）

使用 placement new 在一段预分配的缓冲区上构造对象，并手动调用析构。

<details><summary>答案与解析</summary>

placement new 的 `new(p) T(args)` 形式在已存在的内存 `p` 上构造对象，不分配；因此必须手动调用析构函数，且缓冲区需满足对齐与大小。

```cpp
#include <iostream>
#include <new>
#include <cstddef>
struct Point { int x, y; Point(int a, int b) : x(a), y(b) {} };
int main() {
    alignas(Point) static char pool[sizeof(Point) * 4];  // 预分配内存池
    Point* p = new (pool) Point(1, 2);     // placement new: 在 pool 上构造
    std::cout << p->x << "," << p->y << "\n";
    p->~Point();                           // 必须手动析构(placement new 不自动)
}
```

[标准] placement new 把"内存分配"与"对象构造"解耦，是内存池/定制分配器的核心机制。

</details>

### 练习 3（难度 ★★★★）

为某个小对象实现简易空闲链表对象池：复用已释放的对象，避免反复进入系统分配器。

<details><summary>答案与解析</summary>

在类域 `operator new` 中优先从空闲链表取块，不足才 `malloc`；`operator delete` 把块挂回空闲链表。这样高频 new/delete 仅在首次触及系统分配器。

```cpp
#include <iostream>
#include <cstdlib>
#include <new>
struct Node {
    int v;
    Node* next;
    static Node* free_head;
    void* operator new(std::size_t) {
        if (free_head) { Node* p = free_head; free_head = free_head->next; return p; }
        return std::malloc(sizeof(Node));
    }
    void operator delete(void* p) {
        Node* n = static_cast<Node*>(p);
        n->next = free_head; free_head = n;
    }
};
Node* Node::free_head = nullptr;
int main() {
    Node* a = new Node{1, nullptr};
    Node* b = new Node{2, nullptr};
    delete a; delete b;        // 回收进空闲链表
    Node* c = new Node{3, nullptr};   // 复用 b 的块
    std::cout << "reused node v=" << c->v << "\n";
}
```

[标准] 固定大小对象池把分配器开销摊还到首次，并消除碎片；代价是需手动保证对象析构（或池统一回收）。

</details>

## 附录：用法演绎（从选型到落地）

### 演绎 1：new / delete 必须配对，数组用 delete[]

**场景**：你用 `new[]` 分配了一个数组，释放时手滑写成 `delete`（少写方括号），程序偶发堆损坏。

**常见错误**（朴素写法）：
```text
int* p = new int[10];
delete p;          // 错误: 应 delete[] p; 否则 UB(仅释放首元素或破坏簿记)
```

**修复**：严格配对 `new`/`delete` 与 `new[]`/`delete[]`；更彻底的方案是根本不写裸 `new`，改用容器或智能指针。

```cpp
#include <iostream>
#include <memory>
#include <vector>
int main() {
    int* a = new int[10]; delete[] a;          // 配对
    auto b = std::make_unique<int[]>(10);       // 智能指针, 自动 delete[]
    std::vector<int> v(10);                      // 容器, 自动管理
    std::cout << "ok: 配对 new[]+delete[] 或 vector\n";
}
```

**结论**：裸数组 `new[]` 极易配错；`std::vector` / `std::unique_ptr<T[]>` 把数组生命周期交给 RAII，从根上消除配对错误。

### 演绎 2：高频小对象 → 对象池 / placement new 降碎片

**场景**：网络包处理对每个包都 `new`/`delete` 一个 Pkt 结构，运行一段时间后堆碎片上升、延迟抖动。

**常见错误**（朴素写法）：
```text
void on_packet() {
    Pkt* p = new Pkt{...};   // 每包进通用分配器, 碎片+系统调用
    // ... use p ...
    delete p;
}
```

**修复**：用空闲链表对象池复用 Pkt 块，或 placement new 落预分配缓冲；分配次数从"每包一次"降到"池耗尽才一次"。

```cpp
#include <iostream>
#include <cstdlib>
#include <new>
struct Pkt {
    int len;
    Pkt* next;
    static Pkt* free_head;
    void* operator new(std::size_t) {
        if (free_head) { Pkt* p = free_head; free_head = p->next; return p; }
        return std::malloc(sizeof(Pkt));
    }
    void operator delete(void* p) { Pkt* n = static_cast<Pkt*>(p); n->next = free_head; free_head = n; }
};
Pkt* Pkt::free_head = nullptr;
int main() {
    for (int i = 0; i < 3; ++i) delete new Pkt{i, nullptr};  // 分配即回收, 复用
    Pkt* p = new Pkt{99, nullptr};
    std::cout << "pooled pkt len=" << p->len << " (零系统调用)\n";
}
```

**结论**：高频定长小对象是内存池/placement new 的典型受益者；复用把分配器开销与碎片降到最低。

""",

"ch38": r"""### 练习 1（难度 ★★）

用 `std::pmr::monotonic_buffer_resource` 配合 `std::pmr::vector`，让一个 vector 的全部分配都落在栈上的固定缓冲区内，做到零堆分配。

<details><summary>答案与解析</summary>

`monotonic_buffer_resource` 在给定缓冲上单调分配（只增不减，销毁时整体回收）；把它的指针交给 pmr 容器的分配器，容器就在该缓冲上取内存。

```cpp
#include <iostream>
#include <memory_resource>
#include <vector>
int main() {
    char buf[1024];
    std::pmr::monotonic_buffer_resource res(buf, sizeof(buf));
    std::pmr::polymorphic_allocator<int> pa(&res);
    std::pmr::vector<int> v(pa);     // 在 buf 上分配, 零堆
    for (int i = 0; i < 10; ++i) v.push_back(i);
    std::cout << "pmr vector size=" << v.size()
              << " (栈缓冲, 零堆分配)\n";
}
```

[标准] `std::pmr` 把"分配策略"与"容器"解耦；`monotonic_buffer_resource` 适合请求内临时分配，请求结束一次性回收。

</details>

### 练习 2（难度 ★★★）

自定义一个 `std::pmr::memory_resource`，在委托上游资源分配的同时累计分配字节数，从而观测某次操作的总分配量。

<details><summary>答案与解析</summary>

继承 `std::pmr::memory_resource` 并重写 `do_allocate` / `do_deallocate` / `do_is_equal` 三个虚函数；在 `do_allocate` 里累加后委托上游。

```cpp
#include <iostream>
#include <memory_resource>
#include <vector>
struct CountingResource : std::pmr::memory_resource {
    std::pmr::memory_resource* upstream = std::pmr::get_default_resource();
    long total = 0;
    void* do_allocate(std::size_t bytes, std::size_t align) override {
        total += (long)bytes;
        return upstream->allocate(bytes, align);
    }
    void do_deallocate(void* p, std::size_t bytes, std::size_t align) override {
        upstream->deallocate(p, bytes, align);
    }
    bool do_is_equal(const std::pmr::memory_resource& o) const noexcept override {
        return this == &o;
    }
};
int main() {
    CountingResource cr;
    std::pmr::polymorphic_allocator<int> pa(&cr);
    std::pmr::vector<int> v(pa);
    for (int i = 0; i < 5; ++i) v.push_back(i);
    std::cout << "allocated bytes via pmr = " << cr.total << "\n";
}
```

[标准] pmr 资源可任意组合（计数、池化、对齐、调试）；所有 pmr 容器都通过 `polymorphic_allocator` 间接使用资源。

</details>

### 练习 3（难度 ★★★★）

用自定义计数资源对比"不 reserve"与"预先 reserve"时 `std::pmr::vector` 的分配次数，说明扩容代价。

<details><summary>答案与解析</summary>

vector 容量不足时扩容会重新分配并搬运元素；`reserve` 一次到位则只分配一次。用计数资源可把这一点量化出来。

```cpp
#include <iostream>
#include <memory_resource>
#include <vector>
struct CountRes : std::pmr::memory_resource {
    std::pmr::memory_resource* up = std::pmr::get_default_resource();
    long calls = 0;
    void* do_allocate(std::size_t b, std::size_t a) override { ++calls; return up->allocate(b, a); }
    void do_deallocate(void* p, std::size_t b, std::size_t a) override { up->deallocate(p, b, a); }
    bool do_is_equal(const std::pmr::memory_resource& o) const noexcept override { return this == &o; }
};
int main() {
    CountRes cr;
    std::pmr::polymorphic_allocator<int> pa(&cr);
    std::pmr::vector<int> v(pa);
    for (int i = 0; i < 1000; ++i) v.push_back(i);
    std::cout << "pmr vector allocations = " << cr.calls << "\n";
    CountRes cr2;
    std::pmr::polymorphic_allocator<int> pa2(&cr2);
    std::pmr::vector<int> w(pa2); w.reserve(1000);
    for (int i = 0; i < 1000; ++i) w.push_back(i);
    std::cout << "pmr vector (reserve) allocations = " << cr2.calls << "\n";
}
```

[标准] `reserve` 把分配次数从 O(log n) 降到 1；在已知规模的热点路径上应预先 reserve。

</details>

## 附录：用法演绎（从选型到落地）

### 演绎 1：高频临时容器 → pmr 池化降延迟

**场景**：每个网络请求内都要构造若干临时 `std::vector` 做解析，默认分配器每处都走堆，带来延迟尖刺与碎片。

**常见错误**（朴素写法）：
```text
void on_request() {
    std::vector<int> tmp;        // 每次走堆分配
    // ... 解析 ...
}                                // 离开作用域逐个释放
```

**修复**：为请求准备一块 `monotonic_buffer_resource`，请求内所有临时 pmr 容器都从这块缓冲取内存；请求结束资源析构，一次性整体回收，零逐对象释放。

```cpp
#include <iostream>
#include <memory_resource>
#include <vector>
void handle_request(char* buf, std::size_t n) {
    std::pmr::monotonic_buffer_resource res(buf, n);
    std::pmr::polymorphic_allocator<int> pa(&res);
    std::pmr::vector<int> tmp(pa);
    for (int i = 0; i < 4; ++i) tmp.push_back(i);
    std::cout << "request used " << tmp.size() << " elems (零堆分配)\n";
}
int main() {
    char buf[512];
    handle_request(buf, sizeof(buf));
}
```

**结论**：`monotonic_buffer_resource` 是"请求/帧作用域内临时分配"的理想选择——分配极快、回收一次性；代价是该资源上的内存不能单独释放（只增不减）。

### 演绎 2：pmr 资源的生命周期陷阱

**场景**：你把 `monotonic_buffer_resource` 声明为局部变量，却把依赖它的 pmr 容器存进了更长寿的对象（如 `shared_ptr`），资源先析构，容器再访问即悬垂。

**常见错误**（朴素写法）：
```text
auto res = std::make_shared<std::pmr::monotonic_buffer_resource>(buf, n);
auto vec = std::make_shared<std::pmr::vector<int>>(&*res);
// ... res 先于 vec 销毁, vec 指向已失效资源 -> UB
```

**修复**：资源生命周期必须 ≥ 所有使用它的 pmr 容器；把资源与容器放在同一作用域，或把资源作为容器的成员/拥有者。

```cpp
#include <iostream>
#include <memory_resource>
#include <vector>
int main() {
    char buf[256];
    std::pmr::monotonic_buffer_resource res(buf, sizeof(buf));  // 先建资源
    std::pmr::polymorphic_allocator<int> pa(&res);              // 先命名 allocator 变量
    std::pmr::vector<int> v(pa);                                // 同作用域: pa 为变量 -> 构造而非函数声明
    v.push_back(7);
    std::cout << "ok: 资源与 vector 同生命周期, v[0]=" << v[0] << "\n";
}
```

**结论**：pmr 容器只持有资源的指针，不拥有它；"资源活得比容器久"是硬约束，违反即悬垂。

""",

"ch40": r"""### 练习 1（难度 ★★）

用 copy-and-swap 惯用法为某个持有资源的类实现强异常安全保证的赋值运算符。

<details><summary>答案与解析</summary>

赋值运算符按值接收参数（发生拷贝），再与当前对象 `swap`；若拷贝阶段抛异常，当前对象原封不动（强保证）；`swap` 本身标 `noexcept`。

```cpp
#include <iostream>
#include <utility>
#include <vector>
struct Buf {
    std::vector<int> d;
    Buf(std::size_t n) : d(n) {}
    void swap(Buf& o) noexcept { d.swap(o.d); }
    Buf& operator=(Buf o) noexcept { d.swap(o.d); return *this; }  // 传值=拷贝, swap 提交
};
int main() {
    Buf a(3), b(5);
    a = b;
    std::cout << "a size=" << a.d.size() << "\n";
}
```

[标准] 传值参数在调用处完成拷贝，异常发生在 swap 之前，从而天然满足强异常保证。

</details>

### 练习 2（难度 ★★★）

演示：即使函数因异常提前返回，栈上的 RAII 对象仍会被析构（资源正确释放）。

<details><summary>答案与解析</summary>

异常沿调用栈展开时会逐个析构已构造的栈对象（栈展开）；RAII 正是利用这一点保证资源释放。

```cpp
#include <iostream>
#include <stdexcept>
struct Guard { ~Guard() { std::cout << "cleanup\n"; } };
void f() {
    Guard g;                          // 无论 f 如何返回, g 都析构
    throw std::runtime_error("boom");
}
int main() {
    try { f(); }
    catch (const std::exception& e) { std::cout << "caught: " << e.what() << "\n"; }
}
```

[标准] 栈展开对每一个已构造的自动对象调用析构函数；这就是 C++ 异常安全的核心机制。

</details>

### 练习 3（难度 ★★★★）

实现一个事务式提交：把修改先放进暂存区，提交时以"拷贝旧状态→合并→原子 swap"的方式保证强异常安全（提交失败原状态不变）。

<details><summary>答案与解析</summary>

先复制已提交状态到局部副本，在副本上合并暂存区；只有合并成功才与 `committed` 交换。若合并过程抛异常，`committed` 完全不受影响。

```cpp
#include <iostream>
#include <vector>
struct Db {
    std::vector<int> committed;
    std::vector<int> stage;
    void begin() { stage.clear(); }
    void add(int x) { stage.push_back(x); }
    void commit() {
        auto next = committed;                          // 拷贝旧状态
        next.insert(next.end(), stage.begin(), stage.end());
        committed.swap(next);                           // 原子提交(强保证)
    }
};
int main() {
    Db db; db.begin(); db.add(1); db.add(2); db.commit();
    std::cout << "committed=" << db.committed.size() << "\n";
}
```

[标准] "先做再提交"把不可逆的破坏限定在 swap 之前，是强异常保证的经典实现。

</details>

## 附录：用法演绎（从选型到落地）

### 演绎 1：析构函数抛异常 → std::terminate

**场景**：你在某个类的析构函数里做清理，清理失败时顺手 `throw`，结果程序在异常栈展开期间直接终止，还以为是别处 bug。

**常见错误**（朴素写法）：
```text
~T() {
    if (!cleanup()) throw std::runtime_error("cleanup failed");  // 栈展开期 -> terminate
}
```

**修复**：析构函数默认就是 `noexcept`；清理失败应吞掉异常（或仅记日志），绝不能向外传播。需要时把"可能失败"的清理做成显式、可抛的 `close()` 成员，由调用者决定如何处理。

```cpp
#include <iostream>
#include <stdexcept>
struct T {
    ~T() noexcept {                  // 析构不向外抛
        try { /* 可能失败的清理 */ }
        catch (...) { /* 吞掉, 记日志, 绝不抛 */ }
    }
};
int main() { T t; std::cout << "dtor safe (no terminate)\n"; }
```

**结论**：两个异常同时存在（正在传播一个、析构又抛一个）会立即 `std::terminate`；析构函数必须是异常安全的终点。

### 演绎 2：关键路径用 noexcept 承诺不抛，换取性能

**场景**：你为某个资源管理类写了移动构造，却没标 `noexcept`；`std::vector` 扩容时发现移动可能抛，为保全强异常保证退化为拷贝，性能骤降。

**常见错误**（朴素写法）：
```text
S(S&& o) : p(o.p) { o.p = nullptr; }   // 未标 noexcept -> vector 扩容退化为拷贝
```

**修复**：当底层资源的移动确实不抛时，显式把移动操作标 `noexcept`；容器据此选择移动而非拷贝。

```cpp
#include <iostream>
#include <vector>
#include <utility>
struct S {
    int* p = new int[8];
    S() = default;
    S(S&& o) noexcept : p(o.p) { o.p = nullptr; }   // noexcept: 承诺不抛
    ~S() { delete[] p; }
};
int main() {
    std::vector<S> v; v.reserve(4);
    for (int i = 0; i < 4; ++i) v.push_back(S{});     // 扩容走移动(S 移动 noexcept)
    std::cout << "vector grew via move (noexcept)\n";
}
```

**结论**：`noexcept` 既是性能开关也是契约——它告诉标准库"此操作绝不抛"，从而启用移动、启用更快的算法路径。

""",
}
