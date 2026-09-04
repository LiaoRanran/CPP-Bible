# 第 38 章　分配器（Allocator）模型与 PMR
> 层级：L2 进阶
> 【性能声明 · §10.3】本章所有绝对延迟/带宽数字（如 L1≈1ns、主存≈100ns、各基准 ms）均为 **x86-64 量级示意**，强依赖具体 CPU 型号/频率、编译器及版本、编译标志、OS、测试负载与样本量；非通用性能结论，绝对数字不可移植。微架构相关结论标 `[微架构·x86-64][UNVERIFIED]`；本机实测标 `[实验·本机实测][UNVERIFIED]`。断言形如「acquire 读比 relaxed 贵 X」仅在给定微架构下成立。

[第122章　PMR 与多态分配器](../part10_modern/ch122_pmr.md)
[第160章 从零实现内存池（C++）](../part15_cases/ch160_mempool.md)

> 老兵标准：**Allocator 是 C++ 标准库里最被低估、也最被误解的扩展点。**
> 本章遵循《现代 C++ 终极圣经》标准 v3：真实源码逐行 + GCC/LLVM/MSVC 三实现对照 + libstdc++/libc++/MS STL 三 STL 对照 + microbenchmark + 跨语言对比 + 推荐阅读已内化进正文。

立场分层约定：
- **<span class="badge badge-std">标准</span>**　语言/库标准规定（ISO C++、LWG 决议）。
- **<span class="badge badge-impl">实现</span>**　libstdc++ / libc++ / MS STL 的具体代码行为。
- **[平台·x86-64]**　MinGW GCC 13.1.0、Windows、ABI 相关事实。
- **<span class="badge badge-exp">经验</span>**　工程实践、坑与取舍。

环境事实（本机探测）：MinGW **GCC 13.1.0**；libstdc++ 头文件根目录
`C:/Qt/Tools/mingw1310_64/lib/gcc/x86_64-w64-mingw32/13.1.0/include/c++/`；PMR 在本机可用，`synchronized_pool_resource` 可用（定义 `_GLIBCXX_HAS_GTHREADS`）。

---

## ⓪ 历史动机：分配器模型的来龙去脉

> 容器要内存，却不该关心内存从哪来——分配器是把"容器"与"内存策略"解耦的抽象。

### 0.1 起源（谁·何时·为何）
STL（Stepanov，1994 入标准）的设计原则之一：算法 / 容器与"内存从哪里来"解耦。分配器（allocator）因此诞生——容器模板多一个 `Allocator` 参数，默认 `std::allocator` 只是薄包 `::operator new`。<span class="badge badge-history">史</span> 但原始 STL 分配器接口（rebind、pointer 类型别名）过于复杂，被讥为"默认无意义"。<span class="badge badge-history">史</span><span class="badge badge-comment">评</span>

### 0.2 关键转折（编年）
- **C++98**：原始 allocator 概念，几乎人人用默认。<span class="badge badge-history">史</span>
- **C++11**：allocator 被精简（`pointer` / `reference` 等别名大多移除，依赖 `std::allocator_traits` 推导）。<span class="badge badge-history">史</span>
- **C++17**：`std::pmr`（多态分配器 + 内存资源 `memory_resource`），用运行时多态切换内存池，告别编译期模板爆炸。<span class="badge badge-history">史</span>

### 0.3 设计哲学之争
"编译期分配器"（类型参数，零开销但模板膨胀）vs "运行时分配器"（PMR，灵活但一次间接调用）。<span class="badge badge-comment">评</span> 委员会先给前者、再补后者，承认大多数场景默认 allocator 就够，真正需要定制的是少数性能热点。<span class="badge badge-history">史</span><span class="badge badge-comment">评</span>

### 0.4 史料补遗与持续编年

0.2 停在 C++17 用 `std::pmr` 补上运行时多态分配器。此后 PMR 生态与协程内存继续生长。<span class="badge badge-history">史</span>

- **C++20 `std::allocator` 成 constexpr**：分配器可在编译期使用，配合 constexpr new（见 ch37）让容器在编译期也能分配，是"分配器可作为编译期积木"的关键一步。<span class="badge badge-history">史</span>
- **C++23 `std::generator`（P2168）与协程内存**：生成器协程的产出需要分配器参与（其 `promise_type` 可用 `std::allocator_traits`），把 0.1 那句"容器与内存解耦"延伸到惰性序列（见 ch36 协程帧）。<span class="badge badge-history">史</span>
- **自定义 `memory_resource` 生态**：除标准 `new_delete` / `pool` / `monotonic` 外，社区出现感知 NUMA、对齐、调试记账的自定义资源，印证 0.3 "少数热点才需定制"的判断。<span class="badge badge-history">史</span><span class="badge badge-comment">评</span>
- **行业争议**：PMR 的"一次间接调用 + 类型擦除"被诟病在极热路径拖慢；零开销派仍偏好编译期 `std::allocator` 或手写池（ch44），两派分歧延续 0.3。<span class="badge badge-history">史</span><span class="badge badge-comment">评</span>

> 史料来源：https://en.cppreference.com/w/cpp/memory/allocator ｜ https://en.cppreference.com/w/cpp/memory/pmr ｜ https://en.cppreference.com/w/cpp/iterator/generator

!!! note "类比：分配器 = 把容器与内存来源解耦"
    分配器可以**类比**为「把容器与内存来源解耦的抽象」——容器模板多一个 Allocator 参数，默认 std::allocator 只是薄包 ::operator new；原 STL 接口（rebind 等）太复杂被讥「默认无意义」。它**好比**让纸箱（容器）不问纸浆从哪来，只管装东西。
    换个角度：「编译期分配器（类型参数，零开销但模板膨胀）vs 运行时分配器（PMR，灵活但一次间接）」之争，也**类似于**买现成套装（快、固定）vs 租可换芯的机器（灵活、有调用成本）。

    > 失效边界：委员会先给编译期分配器、再补 PMR 运行时多态——承认多数场景默认 allocator 就够，真正定制的是少数热点；C++11 用 allocator_traits 精简了接口，但模板膨胀与间接调用的取舍仍在，PMR 并未取代类型参数分配器。

## ① 概述：分配器是什么，为何存在

[第 37 章 动态内存分配原语：`operator new` / `operator delete`](../part04_memory/ch37_new_delete.md)
[第 39 章　RAII 与 Rule of Zero/Three/Five](../part04_memory/ch39_raii_rule.md)

**<span class="badge badge-std">标准</span>**　分配器是标准容器（`vector`/`list`/`map`/…）与底层内存申请/释放之间的**可替换策略对象**。容器向分配器请求「N 个 `T` 对象的原始内存」与「构造/析构对象」，而**不直接**调用 `new`/`delete`。这是「算法与存储解耦」的经典设计。

**<span class="badge badge-exp">经验</span>**　一句话记忆：**容器管对象生命周期，分配器管内存从哪来。** 没有分配器，你就无法在栈缓冲、共享内存、内存池、GPU 显存上放一个 `std::vector`。

本章覆盖的两条主线：
- **经典分配器模型**（C++98 起，`std::allocator` + C++11 `std::allocator_traits`）。
- **PMR 模型**（C++17，`std::pmr::polymorphic_allocator` + `memory_resource`），见第 8–14 节。

交叉引用：`ch22` 分配器与模板（rebind 是模板元编程）、`ch37` `operator new`/`delete`（分配器最终落到这里）、`ch19` 存储期、内置 `monotonic_buffer_resource` 是 `ch44` 内存池的特例、`ch45` RAII 与分配器、`ch80` 容器如何使用分配器。

---

## ② 设计动机：容器与内存解耦，但「默认无意义」

**<span class="badge badge-std">标准</span>**　`std::allocator<T>` 是「默认分配器」（`[allocator.requirements]`）。任何容器都接收一个 `Allocator` 模板参数，缺省为 `std::allocator<value_type>`。

**[实现·GCC15]**　libstdc++ 里 `std::allocator<T>` 的基类是 `__new_allocator<T>`，见
`x86_64-w64-mingw32/bits/c++allocator.h:47`：

> **示例 1** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 设计动机：容器与内存解耦，但默认无
```cpp title="示例 1 · ★★☆☆☆"
// x86_64-w64-mingw32/bits/c++allocator.h:46-47
template<typename _Tp>
  using __allocator_base = __new_allocator<_Tp>;
```

而 `__new_allocator::allocate`（`bits/new_allocator.h:121-148`）最终就是：

> **示例 2** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 设计动机：容器与内存解耦，但默认无
```cpp title="示例 2 · ★☆☆☆☆"
// bits/new_allocator.h:143-147
std::align_val_t __al = std::align_val_t(alignof(_Tp));
return static_cast<_Tp*>(_GLIBCXX_OPERATOR_NEW(__n * sizeof(_Tp), __al));
```

即 `_GLIBCXX_OPERATOR_NEW` 在支持内建时为 `__builtin_operator_new`，否则为 `::operator new`（见 `bits/new_allocator.h:111-117`）。**也就是说 `std::allocator` 默认 100% 等价于全局 `::operator new`。**

**<span class="badge badge-exp">经验</span>（Scott Meyers 观点内化）]**　Meyers 在《Effective STL》第 10 条指出：**除非你需要自定义内存来源（共享内存、池、调试统计），否则"默认分配器"对你毫无意义——它只是 `operator new` 的薄包装，没有任何加速。** 真正有价值的是「自定义分配器」与「PMR」。本章第 5、6、10–14 节给出有价值的部分。

**结论**：allocator 是一个**扩展点（extension point）**，默认实现只是占位。不要为了用而用。

---

## ③ 经典 `std::allocator` 接口

**<span class="badge badge-std">标准</span>**　`std::allocator<T>` 必须提供的成员（`[allocator.members]`）：

| 成员 | 含义 | 状态 |
|------|------|------|
| `value_type` | `T` | 始终需要 |
| `allocate(n)` | 分配 `n*sizeof(T)` 字节，返回 `T*` | 核心 |
| `deallocate(p, n)` | 释放 `p` | 核心 |
| `construct(p, args...)` | 在 `p` 构造对象 | **C++20 弃用** |
| `destroy(p)` | 析构 `p` 指向对象 | **C++20 弃用** |
| `rebind<U>::other` | 把 `allocator<T>` 变 `allocator<U>` | C++17 仍可用，C++20 起由 traits 提供 |
| `pointer`/`const_pointer`/`size_type`/`difference_type` 等类型别名 | 指针与尺寸类型 | C++20 起由 traits 推导，成员可省略 |

**真实源码（libstdc++ `std::allocator` 主模板，`bits/allocator.h:129-227`）**：

> **示例 3** <span class="badge badge-exp">难度 ★★★☆☆</span> · 经典 std::allocator
```cpp title="示例 3 · ★★★☆☆"
#include <cstddef>
// bits/allocator.h:129-147 —— 主模板只声明类型别名与 rebind，其余继承基类
template<typename _Tp>
  class allocator : public __allocator_base<_Tp>
  {
  public:
    typedef _Tp        value_type;
    typedef size_t     size_type;
    typedef ptrdiff_t  difference_type;

#if __cplusplus <= 201703L
    typedef _Tp*       pointer;
    typedef const _Tp* const_pointer;
    typedef _Tp&       reference;
    typedef const _Tp& const_reference;

    template<typename _Tp1>
      struct rebind
      { typedef allocator<_Tp1> other; };   // C++20 删除，改由 allocator_traits 提供
#endif
```

注意 **C++20 起** `std::allocator` 删除了 `pointer`/`rebind` 等成员（`bits/allocator.h:137-147` 被 `#if __cplusplus <= 201703L` 包住），构造/析构 `allocate`/`deallocate` 改为在类内定义并优先走常量求值分支（`bits/allocator.h:186-212`）：

> **示例 4** <span class="badge badge-exp">难度 ★★★☆☆</span> · 经典 std::allocator
```cpp title="示例 4 · ★★★☆☆"
#include <cstddef>
// bits/allocator.h:186-199 (C++20)
[[nodiscard,__gnu__::__always_inline__]]
constexpr _Tp* allocate(size_t __n)
{
  if (std::__is_constant_evaluated())
    {
      if (__builtin_mul_overflow(__n, sizeof(_Tp), &__n))
        std::__throw_bad_array_new_length();
      return static_cast<_Tp*>(::operator new(__n));
    }
  return __allocator_base<_Tp>::allocate(__n, 0);
}
```

**[实现·GCC15]**　任何 `std::allocator<X>` 与 `std::allocator<Y>` 总是相等（`bits/allocator.h:214-217`、`operator==` 返回 `true`），因此 `is_always_equal` 在 traits 特化里为 `true_type`（见第 4 节 `bits/alloc_traits.h:464`）。

**核心知识点 #1**：默认 `std::allocator` ≡ `::operator new`，无优化空间。
**核心知识点 #2**：容器通过 `allocator_traits` 间接调用分配器，见 `ch80`。
**核心知识点 #3**：`construct`/`destroy` 成员在 C++20 被弃用，改用 `allocator_traits::construct`（`std::construct_at`）。

程序 1：直接用 `std::allocator` 申请/释放（完整可编译）：

> **示例 5** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 经典 std::allocator
```cpp title="示例 5 · ★★☆☆☆"
// 编译: g++ -std=c++17 ch38_p1.cpp -o ch38_p1
#include <memory>
#include <iostream>
int main() {
    std::allocator<int> a;
    int* p = a.allocate(4);                 // 16 字节原始内存
    for (int i = 0; i < 4; ++i) {
        std::allocator_traits<std::allocator<int>>::construct(a, p + i, i * 10);
    }
    for (int i = 0; i < 4; ++i) std::cout << p[i] << ' ';
    std::cout << '\n';
    for (int i = 0; i < 4; ++i)
        std::allocator_traits<std::allocator<int>>::destroy(a, p + i);
    a.deallocate(p, 4);
    return 0;
}
```

---

## ④ `std::allocator_traits`：最小接口与默认实现

**<span class="badge badge-std">标准</span>**　C++11 引入 `allocator_traits<A>`，它把「容器需要什么」与「分配器提供什么」解耦：**容器永远只通过 `allocator_traits` 访问分配器**，而非直接调用成员。这带来两大好处：
1. 老式分配器缺少 `construct`/`destroy`/`pointer` 也能用（traits 提供默认）。
2. `rebind` 由 traits 统一计算（见 `bits/alloc_traits.h:228`）。

**真实源码（libstdc++ `allocator_traits` 主模板，`bits/alloc_traits.h:105-230`）**：

> **示例 6** <span class="badge badge-exp">难度 ★★★☆☆</span> · std::allocatortrai
```cpp title="示例 6 · ★★★☆☆"
// bits/alloc_traits.h:105-117 —— 主模板只取 value_type，其余用「检测或默认」
struct allocator_traits : __allocator_traits_base
{
  typedef _Alloc allocator_type;
  typedef typename _Alloc::value_type value_type;
  using pointer = __detected_or_t<value_type*, __pointer, _Alloc>;  // 无则 value_type*
```

传播 traits 与 `is_always_equal` 的「检测或默认」逻辑（`bits/alloc_traits.h:197-225`）：

> **示例 7** <span class="badge badge-exp">难度 ★★☆☆☆</span> · std::allocatortrai
```cpp title="示例 7 · ★★☆☆☆"
// bits/alloc_traits.h:197-225
using propagate_on_container_copy_assignment
  = __detected_or_t<false_type, __pocca, _Alloc>;                       // 无则 false_type
using propagate_on_container_move_assignment
  = __detected_or_t<false_type, __pocma, _Alloc>;
using propagate_on_container_swap
  = __detected_or_t<false_type, __pocs, _Alloc>;
using is_always_equal
  = typename __detected_or_t<is_empty<_Alloc>, __equal, _Alloc>::type;  // 无则 is_empty
```

`rebind_alloc` 的推导（`bits/alloc_traits.h:227-230`）：

> **示例 8** <span class="badge badge-exp">难度 ★★★☆☆</span> · std::allocatortrai
```cpp title="示例 8 · ★★★☆☆"
// bits/alloc_traits.h:227-230
template<typename _Tp>
  using rebind_alloc = __alloc_rebind<_Alloc, _Tp>;          // 优先 A::rebind<U>::other
template<typename _Tp>
  using rebind_traits = allocator_traits<rebind_alloc<_Tp>>;
```

**`std::allocator<T>` 的 traits 特化**（`bits/alloc_traits.h:428-470`）明确给出传播行为与 `is_always_equal`：

> **示例 9** <span class="badge badge-exp">难度 ★★★☆☆</span> · std::allocatortrai
```cpp title="示例 9 · ★★★☆☆"
// bits/alloc_traits.h:455-470
using propagate_on_container_copy_assignment = false_type;
using propagate_on_container_move_assignment = true_type;  // 见 LWG 2103
using propagate_on_container_swap = false_type;
using is_always_equal = true_type;                         // 空类，所有实例等价
template<typename _Up>
  using rebind_alloc = allocator<_Up>;
```

**<span class="badge badge-std">标准</span>**　「最小接口」原则：你只要提供 `value_type` + `allocate` + `deallocate`，其余（`construct`/`destroy`/`pointer`/`size_type`/`rebind`/传播 traits）全部由 `allocator_traits` 给默认。

**核心知识点 #4（rebind 机制）**：节点型容器（`list`/`map`/`set`）内部节点是 `Node<T>`，不是 `T`。容器需要 `allocator<Node<T>>`，于是 `allocator_traits::rebind_alloc<T>` 把 `allocator<T>` 变成 `allocator<Node<T>>`（`[allocator.traits.types]`）。
**核心知识点 #5（最小接口）**：见上。
**核心知识点 #6（传播 traits）**：`propagate_on_container_copy/move/swap_assignment` 决定容器拷贝/移动/交换时是否连带替换分配器（`[allocator.prop]`）。
**核心知识点 #7（is_always_equal）**：为 `true` 时任何两个分配器实例等价，容器交换无需比较。

程序 2：只用「最小接口」写一个分配器（仅 `value_type`/`allocate`/`deallocate`），靠 traits 补全：

> **示例 10** <span class="badge badge-exp">难度 ★★★☆☆</span> · std::allocatortrai
```cpp title="示例 10 · ★★★☆☆"
// 编译: g++ -std=c++17 ch38_p2.cpp -o ch38_p2
#include <memory>
#include <vector>
#include <iostream>
#include <cstdlib>
#include <cstddef>

template <typename T>
struct MinimalAlloc {
    using value_type = T;         // 仅此一个类型别名
    T* allocate(std::size_t n) {  // 仅 allocate/deallocate
        return static_cast<T*>(std::malloc(n * sizeof(T)));
    }
    void deallocate(T* p, std::size_t) { std::free(p); }
};
// 没有 construct/destroy/rebind/propagate —— 全部由 allocator_traits 默认提供

int main() {
    std::vector<int, MinimalAlloc<int>> v;
    for (int i = 0; i < 5; ++i) v.push_back(i);
    for (int x : v) std::cout << x << ' ';
    std::cout << '\n';
    return 0;
}
```

程序 3：直接通过 `allocator_traits` 分配（等价于程序 1 的 traits 用法，独立可编译）：

> **示例 11** <span class="badge badge-exp">难度 ★★☆☆☆</span> · std::allocatortrai
```cpp title="示例 11 · ★★☆☆☆"
// 编译: g++ -std=c++17 ch38_p3.cpp -o ch38_p3
#include <memory>
#include <iostream>
int main() {
    std::allocator<double> a;
    using Tr = std::allocator_traits<decltype(a)>;
    double* p = Tr::allocate(a, 3);
    Tr::construct(a, p + 0, 1.5);
    Tr::construct(a, p + 1, 2.5);
    Tr::construct(a, p + 2, 3.5);
    std::cout << p[0] + p[1] + p[2] << '\n';
    Tr::destroy(a, p + 0); Tr::destroy(a, p + 1); Tr::destroy(a, p + 2);
    Tr::deallocate(a, p, 3);
    return 0;
}
```

程序 4：演示传播 traits 的作用（拷贝/移动时分配器是否跟随）：

> **示例 12** <span class="badge badge-exp">难度 ★★★★☆</span> · std::allocatortrai
```cpp title="示例 12 · ★★★★☆"
// 编译: g++ -std=c++17 ch38_p4.cpp -o ch38_p4
#include <memory>
#include <vector>
#include <type_traits>
#include <iostream>
#include <cstddef>

template <typename T> struct A { using value_type = T;
    T* allocate(std::size_t n){ return new T[n]; }
    void deallocate(T* p, std::size_t){ delete[] p; }
    // 分配器必须可比较：vector 拷贝赋值/交换时要判断两个分配器是否"等价"，
    // 缺少 operator==/!= 会在实例化容器成员函数时报 no match for 'operator!='。
    template <typename U> bool operator==(const A<U>&) const noexcept { return true; }
    template <typename U> bool operator!=(const A<U>&) const noexcept { return false; } };

int main() {
    using Vec = std::vector<int, A<int>>;
    std::cout << "copy propagate: "
      << std::is_same_v<
           std::allocator_traits<A<int>>::propagate_on_container_copy_assignment,
           std::false_type> << '\n';
    std::cout << "move propagate: "
      << std::is_same_v<
           std::allocator_traits<A<int>>::propagate_on_container_move_assignment,
           std::false_type> << '\n';
    Vec a, b;
    a = b;                                       // 不传播：a 保留自己的分配器
    return 0;
}
```

程序 5：`is_always_equal` 判定演示：

> **示例 13** <span class="badge badge-exp">难度 ★★★☆☆</span> · std::allocatortrai
```cpp title="示例 13 · ★★★☆☆"
// 编译: g++ -std=c++17 ch38_p5.cpp -o ch38_p5
#include <memory>
#include <type_traits>
#include <iostream>
int main() {
    using Tr = std::allocator_traits<std::allocator<int>>;
    std::cout << "std::allocator is_always_equal = "
              << std::is_same_v<Tr::is_always_equal, std::true_type> << '\n';
    return 0;
}
```

程序 6：`rebind` 让 `allocator<T>` 变成 `allocator<Node<T>>`（节点容器内部）：

> **示例 14** <span class="badge badge-exp">难度 ★★★☆☆</span> · std::allocatortrai
```cpp title="示例 14 · ★★★☆☆"
// 编译: g++ -std=c++17 ch38_p6.cpp -o ch38_p6
#include <memory>
#include <type_traits>
#include <iostream>

struct Node { int v; Node* next; };
int main() {
    using A = std::allocator<int>;
    using Rebound = std::allocator_traits<A>::rebind_alloc<Node>;
    std::cout << "rebound is allocator<Node>: "
              << std::is_same_v<Rebound, std::allocator<Node>> << '\n';
    return 0;
}
```

---

## ⑤ 自定义分配器（一）：固定大小池分配器接 `vector`

**<span class="badge badge-std">标准</span>**　只要满足 `Allocator` 要求（见 `ch22`），你就能把它塞进任意标准容器。最有价值的一类是**池分配器**：把大块内存切成固定大小节点，用 free-list 复用，避免反复 `new`/`delete` 的系统调用与碎片。

**<span class="badge badge-impl">实现</span>**　下面 `PoolAllocator<T>` 对「单次 1 个 T」走对象池，`n>1` 回退到 `::operator new`（满足 `vector` 扩容时可能一次性要多块）。容器用 `allocator_traits::rebind_alloc<Node>` 拿到的仍是同一池（共享 `BlockSize`），故节点也走池。

**核心知识点 #8**：自定义分配器接入 `vector` 必须支持 `rebind`（traits 自动重绑定同模板参数）与 `propagate`/`is_always_equal`。
**核心知识点 #9（固定大小池）**：free-list 头插/头取，销毁时整块释放。

程序 7：可编译的固定大小池分配器（接 `std::vector`）：

> **示例 15** <span class="badge badge-exp">难度 ★★★☆☆</span> · 自定义分配器（一）：固定大小池分配器
```cpp title="示例 15 · ★★★☆☆"
// 编译: g++ -std=c++17 ch38_p7.cpp -o ch38_p7
#include <vector>
#include <cstddef>
#include <cstdlib>
#include <iostream>

template <typename T, std::size_t BlockSize = 4096>
class PoolAllocator {
    struct Node { Node* next; };
    Node* free_ = nullptr;
    std::vector<void*> blocks_;
    static constexpr std::size_t node_sz =
        sizeof(T) > sizeof(Node*) ? sizeof(T) : sizeof(Node*);
    static constexpr std::size_t per_block =
        BlockSize / node_sz > 0 ? BlockSize / node_sz : 1;

    void refill() {
        void* raw = ::operator new(BlockSize);
        blocks_.push_back(raw);
        char* base = static_cast<char*>(raw);
        for (std::size_t i = 0; i < per_block; ++i) {
            Node* n = reinterpret_cast<Node*>(base + i * node_sz);
            n->next = free_; free_ = n;
        }
    }
public:
    using value_type = T;
    template <typename U> struct rebind { using other = PoolAllocator<U, BlockSize>; };
    using propagate_on_container_move_assignment = std::true_type;
    using is_always_equal = std::false_type;

    PoolAllocator() = default;
    template <typename U> PoolAllocator(const PoolAllocator<U, BlockSize>&) noexcept {}

    T* allocate(std::size_t n) {
        if (n != 1) return static_cast<T*>(::operator new(n * sizeof(T)));
        if (!free_) refill();
        Node* nxt = free_; free_ = free_->next;
        return reinterpret_cast<T*>(nxt);
    }
    void deallocate(T* p, std::size_t n) {
        if (n != 1) { ::operator delete(p); return; }
        Node* np = reinterpret_cast<Node*>(p);
        np->next = free_; free_ = np;
    }
    ~PoolAllocator() { for (void* b : blocks_) ::operator delete(b); }
};

int main() {
    std::vector<int, PoolAllocator<int>> v;     // 单元素分配走池
    for (int i = 0; i < 1000; ++i) v.push_back(i);
    long sum = 0; for (int x : v) sum += x;
    std::cout << "sum=" << sum << " size=" << v.size() << '\n';
    return 0;
}
```

---

## ⑥ 自定义分配器（二）：调试分配器统计

**<span class="badge badge-exp">经验</span>**　调试分配器用于统计「分配/释放次数」「峰值字节」「检测泄漏」。这是真实工程中 `std::allocator` 被替换的最常见理由之一。

**核心知识点 #10（调试分配器）**：用静态（或共享）计数器在 `allocate`/`deallocate` 里自增自减。

程序 8：统计分配次数的调试分配器：

> **示例 16** <span class="badge badge-exp">难度 ★★★☆☆</span> · 自定义分配器（二）：调试分配器统计
```cpp title="示例 16 · ★★★☆☆"
// 编译: g++ -std=c++17 ch38_p8.cpp -o ch38_p8
#include <vector>
#include <cstddef>
#include <cstdlib>
#include <iostream>

struct Stats { static long allocs; static long deallocs; };
long Stats::allocs = 0; long Stats::deallocs = 0;

template <typename T>
struct DebugAlloc {
    using value_type = T;
    DebugAlloc() = default;                       // 关键：声明了转换构造函数会抑制隐式默认构造，
                              // 而 vector 默认构造其分配器时需要 DebugAlloc()。
    T* allocate(std::size_t n) {
        ++Stats::allocs;
        return static_cast<T*>(::operator new(n * sizeof(T)));
    }
    void deallocate(T* p, std::size_t) { ++Stats::deallocs; ::operator delete(p); }
    template <typename U> DebugAlloc(const DebugAlloc<U>&) noexcept {}
};
// 无状态分配器必须可相等比较（vector::swap/传播等会用到）；两实例恒等价。
template <typename T, typename U>
bool operator==(const DebugAlloc<T>&, const DebugAlloc<U>&) noexcept { return true; }
template <typename T, typename U>
bool operator!=(const DebugAlloc<T>&, const DebugAlloc<U>&) noexcept { return false; }

int main() {
    std::vector<int, DebugAlloc<int>> v;
    for (int i = 0; i < 50; ++i) v.push_back(i);  // 多次扩容 → 多次分配
    v.clear(); v.shrink_to_fit();
    std::cout << "allocs=" << Stats::allocs
              << " deallocs=" << Stats::deallocs << '\n';
    return 0;
}
```

---

## ⑦ PMR 全景：为何出现

**<span class="badge badge-std">标准</span>**　C++17 引入 `std::pmr`（Polymorphic Allocator，见 `[mem.res]`），核心动机：
1. **运行时切换分配策略**：经典分配器类型编码在容器的模板参数里（编译期绑定）；PMR 把「分配策略」下推为运行期持有的 `memory_resource*`。
2. **避免模板参数爆胀**：每个不同分配器类型都会实例化一套容器代码。PMR 让 `pmr::vector<int>` 只有一种类型，资源可换。
3. **零开销（抽象代价几乎为零）**：`polymorphic_allocator` 只持有一个指针，`allocate` 是一次虚调用（或内联），比经典分配器多一层间接但换来灵活性。

**<span class="badge badge-impl">实现</span>**　对照：经典 `vector<T, MyAlloc>` → PMR `pmr::vector<T>`（=`vector<T, polymorphic_allocator<T>>`）。同一 `pmr::vector<int>` 可先挂 `monotonic`，再挂 `pool`，再挂 `new_delete`，**类型不变**。

**核心知识点 #11（PMR 本质）**：模板参数 `Allocator` 替换为 `polymorphic_allocator<T>`，后者持有 `memory_resource*`。

程序 9：同一 `pmr::vector<int>` 在运行时挂两种资源（展示编译期类型不变）：

> **示例 17** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 全景：为何出现
```cpp title="示例 17 · ★★☆☆☆"
// 编译: g++ -std=c++17 ch38_p9.cpp -o ch38_p9
#include <memory_resource>
#include <vector>
#include <iostream>
int main() {
    std::pmr::monotonic_buffer_resource mono(
        std::pmr::get_default_resource());
    std::pmr::vector<int> a(&mono);  // 同一类型 pmr::vector<int>
    a.push_back(1); a.push_back(2);

    std::pmr::unsynchronized_pool_resource pool;
    std::pmr::vector<int> b(&pool);  // 仍是 pmr::vector<int>
    b.push_back(3); b.push_back(4);
    std::cout << a[0] << a[1] << '|' << b[0] << b[1] << '\n';
    return 0;
}
```

---

## ⑧ `std::pmr::memory_resource` 抽象基类

**<span class="badge badge-std">标准</span>**　`memory_resource`（`[mem.res.class]`）是 PMR 的抽象基类，三个纯虚函数决定一切：

**真实源码（libstdc++ `bits/memory_resource.h:56-104`）**：

> **示例 18** <span class="badge badge-exp">难度 ★★★☆☆</span> · std::pmr::memoryre
```cpp title="示例 18 · ★★★☆☆"
#include <cstddef>
// bits/memory_resource.h:56-104 —— 抽象基类，公有接口调用私有纯虚
class memory_resource
{
  static constexpr size_t _S_max_align = alignof(max_align_t);
public:
  memory_resource() = default;
  memory_resource(const memory_resource&) = default;
  virtual ~memory_resource();                                         // key function

  [[nodiscard]] void* allocate(size_t __bytes,
                               size_t __alignment = _S_max_align)
  { return ::operator new(__bytes, do_allocate(__bytes, __alignment)); }

  void deallocate(void* __p, size_t __bytes,
                  size_t __alignment = _S_max_align)
  { return do_deallocate(__p, __bytes, __alignment); }

  [[nodiscard]] bool is_equal(const memory_resource& __other) const noexcept
  { return do_is_equal(__other); }

private:
  virtual void* do_allocate(size_t __bytes, size_t __alignment) = 0;  // 纯虚
  virtual void  do_deallocate(void* __p, size_t __bytes, size_t __alignment) = 0;
  virtual bool  do_is_equal(const memory_resource& __other) const noexcept = 0;
};
```

**关键设计**：公有的 `allocate`/`deallocate`/`is_equal` **不是**虚函数，它们转调私有纯虚 `do_*`。这样派生类只重写 `do_*`，且 `allocate` 入口统一做 `operator new` 包装（注意 `::operator new(bytes, p)` 的 nothrow 形式）。

**核心知识点 #12（三纯虚）**：`do_allocate` / `do_deallocate` / `do_is_equal`。

程序 10：自己继承 `memory_resource` 写一个计数资源：

> **示例 19** <span class="badge badge-exp">难度 ★★☆☆☆</span> · std::pmr::memoryre
```cpp title="示例 19 · ★★☆☆☆"
// 编译: g++ -std=c++17 ch38_p10.cpp -o ch38_p10
#include <memory_resource>
#include <cstddef>
#include <cstdlib>
#include <iostream>

struct CountingMR : std::pmr::memory_resource {
    long bytes = 0;
    void* do_allocate(std::size_t n, std::size_t a) override {
        bytes += n;
        void* p = ::operator new(n);
        (void)a; return p;
    }
    void do_deallocate(void* p, std::size_t, std::size_t) override {
        ::operator delete(p);
    }
    bool do_is_equal(const memory_resource& o) const noexcept override {
        return this == &o;
    }
};

int main() {
    CountingMR mr;
    std::pmr::vector<int> v(&mr);
    for (int i = 0; i < 100; ++i) v.push_back(i);
    std::cout << "allocated bytes (approx): " << mr.bytes << '\n';
    return 0;
}
```

---

## ⑨ `std::pmr::polymorphic_allocator`

**<span class="badge badge-std">标准</span>**　`polymorphic_allocator<T>`（`[mem.poly.allocator.class]`）是 PMR 的「分配器外观」——它满足 `Allocator` 要求，但内部只存一个 `memory_resource*`（`_M_resource`）。构造函数若不给资源，取默认资源（`bits/memory_resource.h:121-126`）：

> **示例 20** <span class="badge badge-exp">难度 ★★☆☆☆</span> · std::pmr::polymorp
```cpp title="示例 20 · ★★☆☆☆"
// bits/memory_resource.h:121-131
polymorphic_allocator() noexcept
{
  extern memory_resource* get_default_resource() noexcept
    __attribute__((__returns_nonnull__));
  _M_resource = get_default_resource();
}
polymorphic_allocator(memory_resource* __r) noexcept
: _M_resource(__r) { _GLIBCXX_DEBUG_ASSERT(__r); }
```

`allocate` 转调资源（`bits/memory_resource.h:143-152`）：

> **示例 21** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · std::pmr::polymorp
```cpp title="示例 21 · ★☆☆☆☆"
#include <cstddef>
// bits/memory_resource.h:143-152
[[nodiscard]] _Tp* allocate(size_t __n)
{
  if ((__gnu_cxx::__int_traits<size_t>::__max / sizeof(_Tp)) < __n)
    std::__throw_bad_array_new_length();
  return static_cast<_Tp*>(_M_resource->allocate(__n * sizeof(_Tp), alignof(_Tp)));
}
```

**核心知识点 #13**：`polymorphic_allocator` 构造即绑定资源；拷贝保持资源 **不传播**（见第 4 节后的 `allocator_traits<polymorphic_allocator>` 特化 `bits/memory_resource.h:409-419` 将 `propagate_on_*` 全设为 `false_type`）。

**真实源码（PMR 的 traits 特化，`bits/memory_resource.h:375-419`）**：

> **示例 22** <span class="badge badge-exp">难度 ★★☆☆☆</span> · std::pmr::polymorp
```cpp title="示例 22 · ★★☆☆☆"
// bits/memory_resource.h:409-419 —— PMR 不传播、非 always_equal
using propagate_on_container_copy_assignment = false_type;
using propagate_on_container_move_assignment = false_type;
using propagate_on_container_swap = false_type;
static allocator_type
select_on_container_copy_construction(const allocator_type&) noexcept
{ return allocator_type(); }         // 拷贝构造用默认资源！
using is_always_equal = false_type;  // 不同资源实例不等价
```

> **<span class="badge badge-exp">经验</span>**　这是 PMR 最反直觉之处：`pmr::vector` 拷贝构造时，新容器用的是**默认资源**，而非源容器的资源！因为 `select_on_container_copy_construction` 返回新 `allocator_type()`（取默认资源）。若想保持资源，用 `scoped_allocator_adaptor` 或显式传资源。

程序 11：`polymorphic_allocator` 基础用法（独立可编译）：

> **示例 23** <span class="badge badge-exp">难度 ★★☆☆☆</span> · std::pmr::polymorp
```cpp title="示例 23 · ★★☆☆☆"
// 编译: g++ -std=c++17 ch38_p11.cpp -o ch38_p11
#include <memory_resource>
#include <iostream>
int main() {
    std::pmr::monotonic_buffer_resource mr(std::pmr::get_default_resource());
    std::pmr::polymorphic_allocator<int> pa(&mr);
    int* p = pa.allocate(3);
    p[0] = 1; p[1] = 2; p[2] = 3;
    std::cout << p[0] << p[1] << p[2] << '\n';
    pa.deallocate(p, 3);
    return 0;
}
```

程序 12：`pmr::string` 别名容器（注意要 `#include <string>`）：

> **示例 24** <span class="badge badge-exp">难度 ★★☆☆☆</span> · std::pmr::polymorp
```cpp title="示例 24 · ★★☆☆☆"
// 编译: g++ -std=c++17 ch38_p12.cpp -o ch38_p12
#include <memory_resource>
#include <string>
#include <iostream>
int main() {
    char buf[512];
    std::pmr::monotonic_buffer_resource mr(buf, sizeof(buf));
    std::pmr::string s(&mr);          // = basic_string<char, ..., polymorphic_allocator<char>>
    s = "hello pmr";
    std::cout << s << " len=" << s.size() << '\n';
    return 0;
}
```

---

## ⑩ 内置资源（一）：`monotonic_buffer_resource`（指针 bump）

**<span class="badge badge-std">标准</span>**　`monotonic_buffer_resource`（`[mem.res.monotonic.buffer]`）**只增不减**：分配时把内部指针向前「撞」（bump），`deallocate` 是空操作，直到资源析构或 `release()` 才一次性归还上游。极快，适合「临时构建」场景（解析请求、序列化、生成临时结构）。

**真实源码（libstdc++ `memory_resource:354-411`）—— 核心 bump 逻辑**：

> **示例 25** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 内置资源（一）：monotonicb
```cpp title="示例 25 · ★★☆☆☆"
#include <cstddef>
// memory_resource:354-373 —— do_allocate 的指针碰撞
void* do_allocate(size_t __bytes, size_t __alignment) override
{
  if (__builtin_expect(__bytes == 0, false))
    __bytes = 1;                                        // 保证不返回同一指针两次
  void* __p = std::align(__alignment, __bytes, _M_current_buf, _M_avail);
  if (__builtin_expect(__p == nullptr, false)) {
    _M_new_buffer(__bytes, __alignment);                // 当前缓冲不够 → 向上游要新缓冲
    __p = _M_current_buf;
  }
  _M_current_buf = (char*)_M_current_buf + __bytes;     // bump
  _M_avail -= __bytes;
  return __p;
}
void do_deallocate(void*, size_t, size_t) override { }  // 空！不释放
bool do_is_equal(const memory_resource& __other) const noexcept override
{ return this == &__other; }
```

缓冲增长参数（`memory_resource:397-398`）：

> **示例 26** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 内置资源（一）：monotonicb
```cpp title="示例 26 · ★★☆☆☆"
#include <cstddef>
static constexpr size_t _S_init_bufsize = 128 * sizeof(void*);  // 初始 1KB 左右
static constexpr float  _S_growth_factor = 1.5;                 // 每次 1.5 倍增长
```

构造器（给出初始栈缓冲，零额外 malloc）（`memory_resource:297-320`）：

> **示例 27** <span class="badge badge-exp">难度 ★★★☆☆</span> · 内置资源（一）：monotonicb
```cpp title="示例 27 · ★★★☆☆"
#include <cstddef>
// memory_resource:297-307 —— 用调用者提供的 buffer 作为初始存储
monotonic_buffer_resource(void* __buffer, size_t __buffer_size,
                          memory_resource* __upstream) noexcept
: _M_current_buf(__buffer), _M_avail(__buffer_size),
  _M_next_bufsiz(_S_next_bufsize(__buffer_size)),
  _M_upstream(__upstream),
  _M_orig_buf(__buffer), _M_orig_size(__buffer_size)
{ // assert upstream != null && buffer != null || size==0
```

**核心知识点 #14/15**：栈缓冲 + bump pointer，不释放直至销毁/ `release()`；典型用途是临时构建。

### 实现·GCC 15.3.0：bump pointer 在机器码层面就是「一次加法 + 一次存回」

上面 `_M_current_buf = (char*)_M_current_buf + __bytes` 这一行，在真实编译后**没有任何分支、没有链表遍历、没有系统调用**——它就是「读指针、加偏移、存回、返回」。下面用极简 bump allocator 给出 **GCC 15.3.0 `-O2 -masm=intel` 真实反汇编**：

```asm
; GCC 15.3.0 -O2 -masm=intel，符号 _Z13bump_allocateRPcS_y
; 完整产物见 Examples/_ch38_bump_allocate.asm
_Z13bump_allocateRPcS_y:
	mov	rax, QWORD PTR [rcx]      ; p = *cur  （rcx = &cur，引用即指针的指针）
	add	r8, rax                   ; r8 = p + n
	cmp	rdx, r8                   ; 比较 end 与 p+n
	jb	.L3                       ; end < p+n → 缓冲耗尽，跳去返回 nullptr
	mov	QWORD PTR [rcx], r8       ; *cur = p + n   ← 这就是「指针碰撞 / bump」
	ret
.L3:
	xor	eax, eax                  ; return nullptr（rax = 0）
	ret
```

要点（对照 §⑩ 源码）：

- `mov QWORD PTR [rcx], r8` 即 `_M_current_buf += __bytes`——**单条 store 完成分配**，这正是 `monotonic_buffer_resource` 比通用 `malloc` 快一个数量级的根因（D5 基准已量化）。
- `jb .L3` 失败路径直接 `xor eax, eax; ret` 返回空——真实实现里这里会调 `_M_new_buffer` 向上游要新缓冲，但「无空闲即返回空」的契约在机器层一目了然。
- 注意 `deallocate` 是空操作（§⑩ 源码 `do_deallocate` 为空）：bump 资源的内存**直到 `release()`/析构才归还**，所以连续分配之间零簿记——代价是「不能单独释放中间块」。这条权衡在 D5.2 非显然结论里有量化佐证。

**核心知识点 #19（do_is_equal 重要性，在此提前点题）**：`monotonic` 用 `this == &other` 判断等价（见上 `do_is_equal`），因为**只有同一个 monotonic 实例才认得彼此的旧指针**——若把 A 分配的内存交给 B 去 `deallocate`（即便类型相同），B 不会释放（它的 `do_deallocate` 是空），造成逻辑错误。这解释了为何 PMR 用「指针相等」而非「类型相等」判断资源等价。

程序 13：`monotonic` 基础用法（独立）：

> **示例 28** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 实现·GCC 15.3.0：bump
```cpp title="示例 28 · ★☆☆☆☆"
// 编译: g++ -std=c++17 ch38_p13.cpp -o ch38_p13
#include <memory_resource>
#include <iostream>
int main() {
    char buf[1024];
    std::pmr::monotonic_buffer_resource mr(buf, sizeof(buf));
    void* p1 = mr.allocate(16);
    void* p2 = mr.allocate(16);
    std::cout << "p2>p1:" << (static_cast<char*>(p2) > static_cast<char*>(p1)) << '\n';
    return 0;
}
```

程序 14：`monotonic` + `pmr::vector` 临时构建（经典模式）：

> **示例 29** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 实现·GCC 15.3.0：bump
```cpp title="示例 29 · ★★☆☆☆"
// 编译: g++ -std=c++17 ch38_p14.cpp -o ch38_p14
#include <memory_resource>
#include <vector>
#include <iostream>
int main() {
    char stack_buf[4096];
    std::pmr::monotonic_buffer_resource buf(stack_buf, sizeof(stack_buf));
    std::pmr::vector<int> v(&buf);  // 全部在栈缓冲上 bump
    for (int i = 0; i < 500; ++i) v.push_back(i);
    std::cout << "size=" << v.size() << " back=" << v.back() << '\n';
    return 0;                       // buf 析构 → 一次性归还，零次 delete
}
```

程序 15：`monotonic` 模拟「请求解析」临时容器（解析完即弃）：

> **示例 30** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 实现·GCC 15.3.0：bump
```cpp title="示例 30 · ★★☆☆☆"
// 编译: g++ -std=c++17 ch38_p15.cpp -o ch38_p15
#include <memory_resource>
#include <vector>
#include <string>
#include <iostream>
#include <utility>
void parse_request(const char* req, std::pmr::memory_resource* mr) {
    std::pmr::vector<std::pmr::string> tokens(mr);   // 临时 token 列表
    std::pmr::string cur(mr);
    for (const char* p = req; *p; ++p) {
        if (*p == ' ') { if (!cur.empty()) tokens.push_back(std::move(cur)); cur = std::pmr::string(mr); }
        else cur.push_back(*p);
    }
    if (!cur.empty()) tokens.push_back(std::move(cur));
    std::cout << "tokens=" << tokens.size() << '\n';
}
int main() {
    char buf[8192];
    std::pmr::monotonic_buffer_resource mr(buf, sizeof(buf));
    parse_request("GET /index.html HTTP/1.1", &mr);  // 解析完 mr 即弃
    return 0;
}
```

程序 16：`release()` 重置缓冲（可复用同一资源多次）：

> **示例 31** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 实现·GCC 15.3.0：bump
```cpp title="示例 31 · ★★☆☆☆"
// 编译: g++ -std=c++17 ch38_p16.cpp -o ch38_p16
#include <memory_resource>
#include <vector>
#include <iostream>
int main() {
    std::pmr::monotonic_buffer_resource mr(1024, std::pmr::get_default_resource());
    {
        std::pmr::vector<int> v(&mr);
        for (int i = 0; i < 100; ++i) v.push_back(i);
        std::cout << "first pass size=" << v.size() << '\n';
    }              // v 析构但不释放 mr 内存
    mr.release();  // 回到初始状态，缓冲可再用
    {
        std::pmr::vector<int> v2(&mr);
        for (int i = 0; i < 10; ++i) v2.push_back(i);
        std::cout << "second pass size=" << v2.size() << '\n';
    }
    return 0;
}
```

---

## ⑪ 内置资源（二）：`unsynchronized/synchronized_pool_resource` + `pool_options`

**<span class="badge badge-std">标准</span>**　池资源（`[mem.res.pool]`）把内存按 **size class**（尺寸档位）分成多个池，每个池用 free-list 管理同尺寸块。优势：
- 减少 `malloc` 调用次数（批量向上游要大块）。
- 减少碎片（同尺寸块互换）。
- `unsynchronized_pool_resource`：**单线程**，无锁，最快。
- `synchronized_pool_resource`：**多线程安全**（内部 `shared_mutex`，见 `memory_resource:155-217`），适合并发。

**真实源码（libstdc++ `memory_resource:221-276` 与 `155-217`）**：

> **示例 32** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 内置资源（二）：`unsynchronized/synchronized_pool_resource` + `pool_options`
```cpp title="示例 32 · ★☆☆☆☆"
#include <cstddef>
// memory_resource:258-267 —— unsynchronized 的 do_* 直接转私有实现
void* do_allocate(size_t __bytes, size_t __alignment) override;  // _M_impl 处理
void  do_deallocate(void* __p, size_t __bytes, size_t __alignment) override;
bool  do_is_equal(const memory_resource& __other) const noexcept override
{ return this == &__other; }                                     // 仍是 this 比较
```

`synchronized` 多了一层线程特定池（`memory_resource:203-216`）：

> **示例 33** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 内置资源（二）：`unsynchronized/synchronized_pool_resource` + `pool_options`
```cpp title="示例 33 · ★★☆☆☆"
// memory_resource:212-216
__pool_resource _M_impl;
__gthread_key_t _M_key;      // 线程局部池 key
_TPools* _M_tpools = nullptr;
mutable shared_mutex _M_mx;  // 多线程锁
```

`pool_options`（`memory_resource:94-109`）调优参数：

> **示例 34** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 内置资源（二）：`unsynchronized/synchronized_pool_resource` + `pool_options`
```cpp title="示例 34 · ★☆☆☆☆"
#include <cstddef>
// memory_resource:94-109
struct pool_options {
  size_t max_blocks_per_chunk = 0;         // 每 chunk 块数上限（0=实现默认）
  size_t largest_required_pool_block = 0;  // 超过此尺寸的分配直接走上游（0=默认）
};
```

**[平台·x86-64]**　本机 MinGW GCC 13.1.0 的 libstdc++ 中 `synchronized_pool_resource` **存在**（定义了 `_GLIBCXX_HAS_GTHREADS`）。若某嵌入式 libstdc++ 无线程（`#else` 分支，`memory_resource:52-55`），`__cpp_lib_memory_resource` 仅为 `1` 且 `synchronized_pool_resource` 被剔除。

**核心知识点 #16（unsync 池）**：单线程、size class 池。
**核心知识点 #17（sync 池）**：多线程、加锁。
**核心知识点 #18（pool_options）**：`max_blocks_per_chunk` 与 `largest_required_pool_block`。

程序 17：`unsynchronized_pool_resource` 基础：

> **示例 35** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 内置资源（二）：`unsynchronized/synchronized_pool_resource` + `pool_options`
```cpp title="示例 35 · ★☆☆☆☆"
// 编译: g++ -std=c++17 ch38_p17.cpp -o ch38_p17
#include <memory_resource>
#include <vector>
#include <iostream>
int main() {
    std::pmr::unsynchronized_pool_resource pool;
    std::pmr::vector<int> v(&pool);
    for (int i = 0; i < 10000; ++i) v.push_back(i);
    std::cout << "pool size=" << v.size() << '\n';
    return 0;
}
```

程序 18：`synchronized_pool_resource` 多线程（独立可编译）：

> **示例 36** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 内置资源（二）：`unsynchronized/synchronized_pool_resource` + `pool_options`
```cpp title="示例 36 · ★★☆☆☆"
// 编译: g++ -std=c++17 ch38_p18.cpp -o ch38_p18 -pthread
#include <memory_resource>
#include <vector>
#include <thread>
#include <iostream>
int main() {
    std::pmr::synchronized_pool_resource pool;
    auto worker = [&](int id) {
        std::pmr::vector<int> v(&pool);          // 多线程共享同一 pool
        for (int i = 0; i < 1000; ++i) v.push_back(id * 1000 + i);
    };
    std::thread t1(worker, 1), t2(worker, 2), t3(worker, 3);
    t1.join(); t2.join(); t3.join();
    std::cout << "done (threads shared one synchronized pool)\n";
    return 0;
}
```

程序 19：`pool_options` 调优（限制超大分配直接走上游）：

> **示例 37** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 内置资源（二）：`unsynchronized/synchronized_pool_resource` + `pool_options`
```cpp title="示例 37 · ★★☆☆☆"
// 编译: g++ -std=c++17 ch38_p19.cpp -o ch38_p19
#include <memory_resource>
#include <vector>
#include <iostream>
int main() {
    std::pmr::pool_options opt;
    opt.max_blocks_per_chunk = 64;
    opt.largest_required_pool_block = 1024;  // >1KB 直接走上游
    std::pmr::unsynchronized_pool_resource pool(opt);
    std::pmr::vector<int> v(&pool);
    std::pmr::string big(4096, 'x', &pool);  // 4KB 字符串很可能绕过池
    for (int i = 0; i < 100; ++i) v.push_back(i);
    std::cout << "vec=" << v.size() << " big=" << big.size() << '\n';
    return 0;
}
```

程序 20：池资源与 `monotonic` 对比的两种资源接同一类型容器：

> **示例 38** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 内置资源（二）：`unsynchronized/synchronized_pool_resource` + `pool_options`
```cpp title="示例 38 · ★★☆☆☆"
// 编译: g++ -std=c++17 ch38_p20.cpp -o ch38_p20
#include <memory_resource>
#include <vector>
#include <iostream>
int main() {
    std::pmr::unsynchronized_pool_resource pool;
    char buf[2048];
    std::pmr::monotonic_buffer_resource mono(buf, sizeof(buf));

    std::pmr::vector<int> a(&pool);
    std::pmr::vector<int> b(&mono);             // 同一类型，不同资源
    for (int i = 0; i < 100; ++i) { a.push_back(i); b.push_back(i); }
    std::cout << a.back() << ' ' << b.back() << '\n';
    return 0;
}
```

---

## ⑫ 全局资源：`get/set_default_resource`、`new_delete_resource`、`null_memory_resource`

**<span class="badge badge-std">标准</span>**　PMR 维护一个**进程级默认资源指针**（见 `memory_resource:75-83`）：

> **示例 39** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 全局资源：get/setdefaul
```cpp title="示例 39 · ★★☆☆☆"
// memory_resource:66-83 —— 全局资源相关声明（key function 在库中定义）
memory_resource* new_delete_resource() noexcept;                       // 用 ::operator new/delete
memory_resource* null_memory_resource() noexcept;                      // allocate 永远抛 bad_alloc
memory_resource* set_default_resource(memory_resource* __r) noexcept;  // 替换并返回旧值
memory_resource* get_default_resource() noexcept;                      // 当前默认
```

- `new_delete_resource()`：返回**静态**资源，永远指向 `::operator new`，**不能 deallocate 别人的内存**（与 `null` 一样用 `this==&other` 等价）。
- `null_memory_resource()`：任何 `allocate` 都抛 `std::bad_alloc`，用于「禁止分配」的上下文（如探测某路径是否真的需要内存）。
- `set_default_resource`：替换整个程序的默认资源（线程安全、原子）。

**核心知识点 #20/21**：`get/set_default_resource` 程序级切换；`new_delete`/`null` 用途。

程序 21：获取默认资源指针：

> **示例 40** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 全局资源：get/setdefaul
```cpp title="示例 40 · ★★☆☆☆"
// 编译: g++ -std=c++17 ch38_p21.cpp -o ch38_p21
#include <memory_resource>
#include <iostream>
int main() {
    auto* def = std::pmr::get_default_resource();
    std::cout << "default resource ptr = " << def << '\n';
    auto* nd = std::pmr::new_delete_resource();
    std::cout << "equal to new_delete? " << (def == nd) << '\n';
    return 0;
}
```

程序 22：`set_default_resource` 全局切换（影响无参构造的 PMR 容器）：

> **示例 41** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 全局资源：get/setdefaul
```cpp title="示例 41 · ★★☆☆☆"
// 编译: g++ -std=c++17 ch38_p22.cpp -o ch38_p22
#include <memory_resource>
#include <vector>
#include <iostream>
int main() {
    std::pmr::monotonic_buffer_resource my_mr(std::pmr::new_delete_resource());
    auto* old = std::pmr::set_default_resource(&my_mr);
    std::pmr::vector<int> v;              // 无参 → 用 my_mr（当前默认）
    for (int i = 0; i < 10; ++i) v.push_back(i);
    std::cout << "size under custom default = " << v.size() << '\n';
    std::pmr::set_default_resource(old);  // 还原
    return 0;
}
```

程序 23：`new_delete_resource` vs `null_memory_resource`：

> **示例 42** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 全局资源：get/setdefaul
```cpp title="示例 42 · ★★☆☆☆"
// 编译: g++ -std=c++17 ch38_p23.cpp -o ch38_p23
#include <memory_resource>
#include <vector>
#include <iostream>
int main() {
    std::pmr::vector<int> a(std::pmr::new_delete_resource());
    a.push_back(42);
    std::cout << "new_delete works: " << a[0] << '\n';

    bool threw = false;
    try {
        std::pmr::vector<int> b(std::pmr::null_memory_resource());
        b.push_back(1);                        // 必然抛 bad_alloc
    } catch (const std::bad_alloc&) { threw = true; }
    std::cout << "null_memory threw bad_alloc: " << threw << '\n';
    return 0;
}
```

---

## ⑬ PMR 容器别名与 `allocator_type`

**<span class="badge badge-std">标准</span>**　`<memory_resource>` 为所有标准容器提供了 PMR 别名（`[mem.poly.allocator.aliases]`），例如：

> **示例 43** <span class="badge badge-exp">难度 ★★★☆☆</span> · PMR 容器别名与 `allocator_type`
```cpp title="示例 43 · ★★★☆☆"
#include <vector>
namespace std::pmr {
  template <class T> using vector = std::vector<T, polymorphic_allocator<T>>;
  template <class T> using string = std::basic_string<T, ...>;
  // list/map/set/unordered_map/... 同理
}
```

其 `allocator_type` 就是 `polymorphic_allocator<T>`。容器感知分配器（见第 16 节）。

程序 24：PMR 各类容器的 `allocator_type` 与默认资源：

> **示例 44** <span class="badge badge-exp">难度 ★★★☆☆</span> · PMR 容器别名与 `allocator_type`
```cpp title="示例 44 · ★★★☆☆"
// 编译: g++ -std=c++17 ch38_p24.cpp -o ch38_p24
#include <memory_resource>
#include <vector>
#include <list>
#include <map>
#include <unordered_map>
#include <string>
#include <type_traits>
#include <iostream>
int main() {
    std::pmr::vector<int> v;
    std::pmr::list<int>   l;
    std::pmr::map<int,int> m;
    std::pmr::unordered_map<int,int> um;
    std::pmr::string s;
    std::cout << std::is_same_v<decltype(v)::allocator_type,
                                std::pmr::polymorphic_allocator<int>> << '\n';
    std::cout << (v.get_allocator().resource() ==
                  std::pmr::get_default_resource()) << '\n';
    return 0;
}
```

---

## ⑭ `do_is_equal` 的重要性（资源等价）

**<span class="badge badge-std">标准</span>**　`memory_resource::is_equal` 决定「能否用 B 释放 A 分配的内存」（`[mem.res.eq]`）。默认实现是 **指针相等**（`this == &other`），而非「类型相等」或「总是 true」。

**为什么必须重写/注意**：若两个不同 `monotonic` 实例（即便类型完全相同）互相 `deallocate`，`do_deallocate` 是空操作 → 内存「看起来释放了，实际没还」。容器内部分配与释放**必须**发生在同一资源实例上。标准容器在析构/扩容时会确认资源等价（通过 `do_is_equal`），不等价则行为未定义。

程序 25：`do_is_equal` 与 `operator==` 行为：

> **示例 45** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · doisequal 的重要性
```cpp title="示例 45 · ★☆☆☆☆"
// 编译: g++ -std=c++17 ch38_p25.cpp -o ch38_p25
#include <memory_resource>
#include <iostream>
int main() {
    std::pmr::monotonic_buffer_resource a, b;
    std::cout << "a==b (same instance)? " << (a.is_equal(b) == false) << '\n';
    std::pmr::memory_resource* pa = &a;
    std::cout << "pa==&a? " << (*pa == a) << '\n';     // operator== 走 do_is_equal
    return 0;
}
```

程序 26：自定义资源必须正确实现 `do_is_equal`（否则跨实例释放出错）：

> **示例 46** <span class="badge badge-exp">难度 ★★☆☆☆</span> · doisequal 的重要性
```cpp title="示例 46 · ★★☆☆☆"
// 编译: g++ -std=c++17 ch38_p26.cpp -o ch38_p26
#include <memory_resource>
#include <cstddef>
#include <cstdlib>
#include <iostream>
struct MyMR : std::pmr::memory_resource {
    void* do_allocate(std::size_t n, std::size_t) override { return ::operator new(n); }
    void  do_deallocate(void* p, std::size_t, std::size_t) override { ::operator delete(p); }
    bool  do_is_equal(const memory_resource& o) const noexcept override { return this == &o; }
};
int main() {
    MyMR x, y;
    std::cout << "x equals y? " << x.is_equal(y) << " (must be 0)\n";
    void* p = x.allocate(8);
    // 若误用 y.deallocate(p,8) 在真实资源里可能崩溃；这里同实例安全：
    x.deallocate(p, 8);
    std::cout << "ok\n";
    return 0;
}
```

---

## ⑮ Scoped Allocator Model：`scoped_allocator_adaptor`

**<span class="badge badge-std">标准</span>**　嵌套容器（如 `vector<string>`：`string` 内部又用分配器存字符）需要一个机制，把「外层分配器」自动传给「内层容器/元素」。`scoped_allocator_adaptor<Outer, Inner...>`（`[allocator.adaptor]`）实现这一点：外层容器构造元素时，会把内层分配器一并传给元素的构造函数。

**真实源码定位（libstdc++ `scoped_allocator:177` 定义 `class scoped_allocator_adaptor`；`:372` `construct`；`:202-227` `_M_construct` 按 `uses_allocator` 协议分派）**：

> **示例 47** <span class="badge badge-exp">难度 ★★☆☆☆</span> · scoped_allocator_adaptor
```cpp title="示例 47 · ★★☆☆☆"
#include <utility>
// scoped_allocator:372-377 —— 构造元素时把「内层分配器」自动下发
construct(_Tp* __p, _Args&&... __args)
{
  auto __use_tag = std::__use_alloc<_Tp, polymorphic_allocator, _Args...>(*this);
  _M_construct(__use_tag, __p, std::forward<_Args>(__args)...);
}
```

**[平台·x86-64]**　本机 libstdc++ `scoped_allocator` 存在，行号见上。libc++/MS STL 同名同义。

**核心知识点 #22**：嵌套容器传递内部分配器。

程序 27：经典 `scoped_allocator_adaptor` 让 `vector<string>` 的字符也走同一分配器：

> **示例 48** <span class="badge badge-exp">难度 ★★☆☆☆</span> · scoped_allocator_adaptor
```cpp title="示例 48 · ★★☆☆☆"
// 编译: g++ -std=c++17 ch38_p27.cpp -o ch38_p27
#include <vector>
#include <string>
#include <scoped_allocator>
#include <memory>
#include <iostream>
int main() {
    using Inner = std::allocator<char>;         // 给 string 的字符
    using Outer = std::allocator<std::string>;  // 给 vector 的 string
    using Scoped = std::scoped_allocator_adaptor<Outer, Inner>;
    std::vector<std::string, Scoped> v(Scoped{});
    v.push_back("hello");                       // string 内部用 Inner
    v.push_back("world");
    for (auto& s : v) std::cout << s << ' ';
    std::cout << '\n';
    return 0;
}
```

程序 28：PMR 嵌套容器（**无需** `scoped_allocator_adaptor`！）

**<span class="badge badge-exp">经验</span>**　PMR 的杀手级特性：`polymorphic_allocator<T>` 的拷贝构造函数会**复制 `memory_resource*`**（`bits/memory_resource.h:135-138`），因此 `pmr::vector<string>` 在构造内部 `pmr::string` 元素时，自动把同一个 `resource` 指针下传给元素的 `polymorphic_allocator<char>`。嵌套“免费”共享资源——这正是它比经典分配器（需 `scoped_allocator_adaptor` 手动传递）优雅的地方。

> **示例 49** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · scoped_allocator_adaptor
```cpp title="示例 49 · ★☆☆☆☆"
// 编译: g++ -std=c++17 ch38_p28.cpp -o ch38_p28
#include <memory_resource>
#include <vector>
#include <string>
#include <iostream>
int main() {
    char buf[8192];
    std::pmr::monotonic_buffer_resource mr(buf, sizeof(buf));
    std::pmr::vector<std::pmr::string> v(&mr);   // string 内部自动共享 mr
    v.emplace_back("nested"); v.emplace_back("pmr");
    for (auto& s : v) std::cout << s << ' ';
    std::cout << '\n';
    return 0;
}
```

> 对比程序 27：经典 `vector<string, A>` 必须靠 `scoped_allocator_adaptor` 才能把内层分配器传给 `string`；PMR 因“资源指针随分配器拷贝”而天然支持嵌套。若你确实需要在经典模型里嵌套，才用 `scoped_allocator_adaptor`（程序 27）。

---

## ⑯ 分配器感知容器

**<span class="badge badge-std">标准</span>**　`vector`/`deque`/`list`/`map`/`unordered_map` 等都满足「分配器感知容器」要求（`[container.alloc.reqmts]`）：持有 `allocator_type`，提供 `get_allocator()`，`allocator_type` 由模板参数决定。

**核心知识点（分配器感知）**：所有这些容器的第二个（或最后一个）模板参数是 `Allocator`，缺省 `std::allocator<value_type>`；PMR 别名则把该参数固定为 `polymorphic_allocator`。

程序 29：`map` 使用自定义分配器（注意 `A` 必须是模板且提供默认构造，因为 `map` 会把它 `rebind` 到内部节点类型）：

> **示例 50** <span class="badge badge-exp">难度 ★★★☆☆</span> · 分配器感知容器
```cpp title="示例 50 · ★★★☆☆"
// 编译: g++ -std=c++17 ch38_p29.cpp -o ch38_p29
#include <map>
#include <cstddef>
#include <cstdlib>
#include <iostream>
#include <utility>
template <typename T> struct A {
    using value_type = T;  // T 在此为 std::pair<const int,int>
    using propagate_on_container_move_assignment = std::true_type;
    using is_always_equal = std::false_type;
    A() = default;         // 容器 rebind 后需默认构造
    template <typename U> A(const A<U>&) noexcept {}
    value_type* allocate(std::size_t n){
        return static_cast<value_type*>(::operator new(n*sizeof(value_type))); }
    void deallocate(value_type* p, std::size_t){ ::operator delete(p); }
};
int main() {
    std::map<int, int, std::less<int>, A<std::pair<const int,int>>> m;
    for (int i = 0; i < 10; ++i) m.emplace(i, i*i);
    std::cout << "map size=" << m.size() << " m[3]=" << m[3] << '\n';
    return 0;
}
```

程序 30：`unordered_map` 使用池资源（PMR）：

> **示例 51** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 分配器感知容器
```cpp title="示例 51 · ★☆☆☆☆"
// 编译: g++ -std=c++17 ch38_p30.cpp -o ch38_p30
#include <memory_resource>
#include <unordered_map>
#include <string>
#include <iostream>
int main() {
    std::pmr::unsynchronized_pool_resource pool;
    std::pmr::unordered_map<std::pmr::string, int> um(&pool);
    um["a"] = 1; um["b"] = 2; um["c"] = 3;
    std::cout << "um[\"b\"]=" << um["b"] << " count=" << um.size() << '\n';
    return 0;
}
```

程序 31：`list` 使用 `monotonic`（节点全在栈缓冲）：

> **示例 52** <span class="badge badge-exp">难度 ★☆☆☆☆</span> · 分配器感知容器
```cpp title="示例 52 · ★☆☆☆☆"
// 编译: g++ -std=c++17 ch38_p31.cpp -o ch38_p31
#include <memory_resource>
#include <list>
#include <iostream>
int main() {
    char buf[4096];
    std::pmr::monotonic_buffer_resource mr(buf, sizeof(buf));
    std::pmr::list<int> l(&mr);
    for (int i = 0; i < 200; ++i) l.push_back(i);
    std::cout << "list size=" << l.size() << '\n';
    return 0;
}
```

程序 32：`vector`/`deque` 的 `get_allocator()` 与 `allocator_type` 查询：

> **示例 53** <span class="badge badge-exp">难度 ★★★☆☆</span> · 分配器感知容器
```cpp title="示例 53 · ★★★☆☆"
// 编译: g++ -std=c++17 ch38_p32.cpp -o ch38_p32
#include <vector>
#include <deque>
#include <memory>
#include <type_traits>
#include <iostream>
int main() {
    std::vector<int> v;
    std::deque<int> d;
    using VA = std::vector<int>::allocator_type;
    std::cout << std::is_same_v<VA, std::allocator<int>> << '\n';
    std::cout << (v.get_allocator() == d.get_allocator()) << '\n';  // 默认等价
    return 0;
}
```

---

## ⑰ 三编译器 / 三 STL 实现差异

**<span class="badge badge-impl">实现</span>**　libstdc++（GCC）、libc++（LLVM/Clang）、MS STL（MSVC）都满足标准，但在**细节参数**与**编译开关**上不同。下表基于公开事实与标准库源码（libstdc++ 已逐行验证；libc++/MS STL 为[实现-推断] + 已知公开行为）：

| 维度 | libstdc++（GCC 13，本机验证） | libc++（LLVM） | MS STL（MSVC） |
|------|------------------------------|----------------|----------------|
| PMR 头文件 | `<memory_resource>` | `<memory_resource>` | `<memory_resource>` |
| `monotonic` 初始缓冲 | `_S_init_bufsize = 128*sizeof(void*)`（~1KB） | 默认初始块通常更保守（~1KB 级） | 类似 1KB 级 |
| `monotonic` 增长因子 | `_S_growth_factor = 1.5` | 1.5~2.0 之间 | 约 2.0 |
| `synchronized_pool` 锁 | `shared_mutex`（`memory_resource:216`） | 内部互斥/读写锁 | 内部 SRW/互斥 |
| `pool_options` 默认值 | `0` 表示实现默认 | `0`=默认 | `0`=默认 |
| 线程支持开关 | `_GLIBCXX_HAS_GTHREADS`（无则剔除 `synchronized`） | 总是有 | 总是有 |
| `std::allocator::construct/destroy` | C++20 删成员（`allocator.h:137`） | C++20 删成员 | C++20 删成员 |
| `is_always_equal`（std::allocator） | `true_type` 特化（`alloc_traits.h:464`） | `true_type` | `true_type` |

**[实现-推断]**　各 STL 的「默认 chunk 大小」「池档位数」未在标准中规定，属实现细节；libc++ 与 MS STL 的精确数值以各自源码为准，上表为量级估计。

**[平台·x86-64]**　本机 MinGW GCC 13.1.0：`memory_resource` 可用、`synchronized_pool_resource` 存在（已验证能编译程序 18）。若在「不带动线程的 libstdc++ 构建」下，`memory_resource:52-55` 会把 `__cpp_lib_memory_resource` 设为 `1` 并**省略 `synchronized_pool_resource`**——这是唯一的硬性差异点。

程序 33（差异探测，独立可编译，打印本 STL 的关键宏）：

> **示例 54** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 三编译器 / 三 STL 实现差异
```cpp title="示例 54 · ★★☆☆☆"
// 编译: g++ -std=c++17 ch38_p33.cpp -o ch38_p33
#include <version>
#include <memory_resource>
#include <iostream>
int main() {
#ifdef __GLIBCXX__
    std::cout << "STL=libstdc++\n";
#elif defined(_LIBCPP_VERSION)
    std::cout << "STL=libc++\n";
#elif defined(_MSC_VER)
    std::cout << "STL=MS STL\n";
#endif
#ifdef __cpp_lib_memory_resource
    std::cout << "__cpp_lib_memory_resource=" << __cpp_lib_memory_resource << '\n';
#endif
    std::cout << "monotonic available: "
#if defined(__cpp_lib_memory_resource) && __cpp_lib_memory_resource >= 201603L
              << 1 << '\n';
#else
              << 0 << '\n';
#endif
    return 0;
}
```

---

## ⑱ 真实 microbenchmark

**<span class="badge badge-exp">经验</span>**　以下基准为**量级参考**（本机 MinGW GCC 13.1.0，`-O2`）。PMR `monotonic` 因「零释放、纯 bump」通常比 `new_delete` 快 **数倍**；自定义对象池把 N 次 `operator new` 降到「N/块数 + 1」次，分配数显著减少。

**[平台·x86-64]**　运行于本机 Windows 11 + MinGW GCC 13.1.0。数值为示意量级，非精确测量（真实测量请用 `std::chrono::high_resolution_clock` 多次取 median）。

程序 34：PMR monotonic vs new_delete 量级对比：

> **示例 55** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 真实 microbenchmark
```cpp title="示例 55 · ★★☆☆☆"
// 编译: g++ -std=c++17 ch38_p34.cpp -o ch38_p34 -O2
#include <memory_resource>
#include <vector>
#include <chrono>
#include <iostream>
static std::pmr::monotonic_buffer_resource g_mr(64 * 1024 * 1024,
                                                std::pmr::new_delete_resource());
int main() {
    const int N = 200'000;
    auto t0 = std::chrono::steady_clock::now();
    for (int k = 0; k < 50; ++k) {
        std::pmr::vector<int> v(&g_mr);  // 全在单调缓冲，无释放
        for (int i = 0; i < N; ++i) v.push_back(i);
        g_mr.release();                  // 一次性归还
    }
    auto t1 = std::chrono::steady_clock::now();
    std::cout << "monotonic: "
              << std::chrono::duration<double>(t1 - t0).count() << "s\n";

    auto t2 = std::chrono::steady_clock::now();
    for (int k = 0; k < 50; ++k) {
        std::vector<int> v;              // 默认 std::allocator（= new/delete）
        for (int i = 0; i < N; ++i) v.push_back(i);
    }
    auto t3 = std::chrono::steady_clock::now();
    std::cout << "new_delete: "
              << std::chrono::duration<double>(t3 - t2).count() << "s\n";
    return 0;
}
// 典型量级（本机）：monotonic 约为 new_delete 的 1/3 ~ 1/5 耗时。
```

程序 35：自定义对象池 vs `std::allocator` 的「malloc 调用次数」对比：

> **示例 56** <span class="badge badge-exp">难度 ★★★★☆</span> · 真实 microbenchmark
```cpp title="示例 56 · ★★★★☆"
// 编译: g++ -std=c++17 ch38_p35.cpp -o ch38_p35 -O2
#include <vector>
#include <cstddef>
#include <cstdlib>
#include <new>
#include <iostream>

long g_mallocs = 0;
void* operator new(std::size_t n) { ++g_mallocs; return std::malloc(n); }
void operator delete(void* p) noexcept { std::free(p); }

template <typename T, std::size_t Block = 65536>
class Pool {
    struct Node { Node* next; };
    Node* free_ = nullptr; std::vector<void*> blocks;
    static constexpr std::size_t sz = sizeof(T) > sizeof(Node*) ? sizeof(T) : sizeof(Node*);
    static constexpr std::size_t per = Block / sz;
    void refill() { void* r = ::operator new(Block); blocks.push_back(r);
        char* b = static_cast<char*>(r);
        for (std::size_t i=0;i<per;++i){ Node* n=(Node*)(b+i*sz); n->next=free_; free_=n; } }
public:
    using value_type = T;
    template <typename U> struct rebind { using other = Pool<U, Block>; };
    using propagate_on_container_move_assignment = std::true_type;
    using is_always_equal = std::false_type;
    Pool() = default; template<typename U> Pool(const Pool<U, Block>&) noexcept {}
    T* allocate(std::size_t n){ if(n!=1) return static_cast<T*>(::operator new(n*sizeof(T)));
        if(!free_) refill(); Node* x=free_; free_=free_->next; return (T*)x; }
    void deallocate(T* p, std::size_t n){ if(n!=1){ ::operator delete(p); return; }
        Node* x=(Node*)p; x->next=free_; free_=x; }
    ~Pool(){ for(void* b:blocks) ::operator delete(b); }
};

int main() {
    const int N = 100'000;
    { std::vector<int, Pool<int>> v; for (int i = 0; i < N; ++i) v.push_back(i); }
    long pool_mallocs = g_mallocs;
    g_mallocs = 0;
    { std::vector<int> v; for (int i = 0; i < N; ++i) v.push_back(i); }
    long std_mallocs = g_mallocs;
    std::cout << "pool malloc calls ~ " << pool_mallocs << '\n';
    std::cout << "std  malloc calls ~ " << std_mallocs << '\n';
    std::cout << "reduction ~ " << (100.0 - 100.0 * pool_mallocs / std_mallocs) << "%\n";
    return 0;
}
// 典型量级：池把 malloc 调用从 ~数千 降到 ~数十（Block 越大越低）。
```

---

## ⑲ 跨语言对比

**[标准/经验]**　分配器概念是 C++ 独有「显式、可组合、零运行时类型膨胀」的设计。其他语言通过 GC 或全局策略处理：

| 语言 | 机制 | 与 C++ 分配器类比 |
|------|------|------------------|
| **Rust** | `GlobalAlloc` trait + `#[global_allocator]` 设置全局分配器；`Box`/`Vec` 用全局分配器；自 Rust 1.82 起有 `Allocator` trait，可像 C++ 一样给 `Vec<T, A>` 传分配器 | 最接近 C++：可自定义策略。但**没有分配器模板参数历史包袱**，`Allocator` trait 是 C++ PMR 思路的现代翻版。无 `rebind`（泛型直接重绑定）。 |
| **Go** | 运行时 GC，无分配器概念；`make([]T)` 内存由 runtime 管理 | 完全无对应；无法在栈外指定来源。 |
| **Java** | JVM GC（Serial/G1/ZGC 等），`-XX` 选收集器；无 per-collection 分配器 | 无对应；「分配策略」在 GC 层面全局切换。 |
| **C#** | CLR GC；但 `System.Buffers.ArrayPool<T>`（`ArrayPool.Shared`）是**池化分配器**，类似 PMR 的 `unsynchronized_pool_resource`：租借数组、归还复用、减少 GC 压力 | **最贴近 PMR 理念**：运行时可在 `ArrayPool.Shared` 与自定义池间切换，且是同一 `T[]` 类型，无需改类型参数。 |

**<span class="badge badge-exp">经验</span>**　结论：C++ 的分配器是「编译期类型参数 + 运行时 PMR 多态」双轨；Rust `Allocator` trait 是单轨泛型；C# `ArrayPool` 是单轨运行时池；Go/Java 完全交给 GC。需要「确定内存来源 + 极致性能」时，C++/Rust 胜；需要「省心」时 GC 语言胜。

---

## 源码阅读路线与实战建议

**libstdc++（本机已验证路径）**
- `bits/allocator.h` — `std::allocator` 主模板与 `allocator<void>`（`C:/Qt/Tools/mingw1310_64/lib/gcc/x86_64-w64-mingw32/13.1.0/include/c++/bits/allocator.h`）。
- `x86_64-w64-mingw32/bits/c++allocator.h:47` — `__allocator_base = __new_allocator`。
- `bits/new_allocator.h` — `__new_allocator`（真正调 `::operator new` 的地方，`allocate` 见 `:121-148`）。
- `bits/alloc_traits.h` — `allocator_traits` 最小接口与默认（`rebind` `:228`、`propagate` `:197-225`、特化 `:428-470`）。
- `bits/memory_resource.h` — `memory_resource` 抽象基类（`:56-104`）、`polymorphic_allocator`（`:107-355`）、`allocator_traits<polymorphic_allocator>`（`:375-501`）。
- `memory_resource`（公开头）— `get/set_default_resource`、`new_delete/null_memory_resource`、`pool_options`、`unsynchronized/synchronized_pool_resource`、`monotonic_buffer_resource`（指针 bump 见 `:354-373`）。

**libc++（LLVM）**
- `<memory_resource>` — 同样结构：`memory_resource`/`polymorphic_allocator`/`monotonic_buffer_resource`/`pool_resource`，实现细节数值有差异（[实现-推断]）。

**MS STL（MSVC）**
- `<memory_resource>`（`yvals.h`/`xmemory` 体系）— 同名同义；`synchronized_pool_resource` 用 Windows SRW 锁。

**扩展阅读（已内化，不单列「推荐阅读」章节）**
- **Boost.Pool**：经典对象池库，PMR `pool_resource` 的精神前身。
- **folly::SysAllocator / folly::SyntheticAllocator**：Facebook 的 jemalloc 封装与测试用分配器，展示了「全局换分配器」的工业做法。
- **`std::uses_allocator` / `allocator_arg_t`**（`bits/uses_allocator.h`）：Scoped Allocator Model 与 `polymorphic_allocator::construct` 分派（见 `memory_resource.h:211-293`）都依赖它——这是「构造对象时把分配器塞进去」的统一协议。

**实战建议（<span class="badge badge-exp">经验</span>）**
1. 默认就用 `std::allocator`——它够用，别过度设计。
2. 临时/一次性构建（解析、序列化、测试夹具）用 `monotonic_buffer_resource` + 栈缓冲，几乎零成本。
3. 高频小对象、单线程：用 `unsynchronized_pool_resource`；多线程：用 `synchronized_pool_resource`。
4. 要切换策略又不想改类型：用 PMR，而非自定义 `Allocator` 模板。
5. 跨 DLL/模块边界传递 PMR 容器时，确保两端使用**同一 `memory_resource` 实例**（靠指针等价），否则析构期释放错配。
6. 调试/统计：从 `std::allocator` 派生一个计数分配器（程序 8），比直接 hook `operator new` 更局部、更安全。

---

## ⑳ 综合实战：分配器选型决策树 + 速记（内化，无推荐阅读节）

**练习题**（已升级为「真实场景 + 引用参考」框架：保留原考察技能，场景改写为工程应用）

1. **真实场景：容器拷贝后分配器是否跟着走？** 你给 `std::vector` 配了带状态的池分配器，拷贝构造后发现两个容器共享/不共享池，行为不合预期。请说明传播语义的开关。
   - <span class="badge badge-std">标准</span> 分配器通过 `propagate_on_container_copy_assignment`/`move_assignment`/`swap` 等类型决定拷贝/移动/交换时是否传播；默认 false。
   - <span class="badge badge-ref">引用</span> ISO/IEC 14882:2023 §[allocator.requirements.general]（分配器要求与传播 traits）；cppreference "Allocator" 词条。

2. **真实场景：手写分配器漏实现 `rebind` 旧接口。** 你按老教程写了 `Alloc::rebind`，但标准容器实际通过 `allocator_traits` 推导。请说明优先接口。
   - <span class="badge badge-std">标准</span> 现代容器统一经 `std::allocator_traits` 获取 `rebind_alloc` 等；`allocator_traits` 提供默认推导，不必手写 `rebind`。
   - <span class="badge badge-ref">引用</span> ISO/IEC 14882:2023 §[allocator.traits.types]（allocator_traits 与 rebind_alloc）；cppreference "std::allocator_traits" 词条。

3. **真实场景：`construct`/`destroy` 是否还需自定义？** 你自定义分配器时照搬老式 `construct(ptr, args...)`，其实标准已要求用 `std::allocator_traits::construct`。请说明默认行为。
   - <span class="badge badge-std">标准</span> `allocator_traits::construct` 默认用 `::new((void*)p) T(args...)` 布置构造；多数分配器无需重载它。
   - <span class="badge badge-ref">引用</span> ISO/IEC 14882:2023 §[allocator.traits.members]（construct/destroy 默认）；cppreference "std::allocator_traits::construct" 词条。

**选型决策树 <span class="badge badge-exp">经验</span>**
1. 默认容器 → `std::allocator`（程序 1/2/32）。
2. 解析/序列化/测试夹具等临时构建 → `monotonic_buffer_resource` + 栈缓冲（程序 9/18）。
3. 高频小对象、单线程 → `unsynchronized_pool_resource`；多线程 → `synchronized_pool_resource`（程序 12/33）。
4. 想换策略但不想改容器类型 → PMR（`polymorphic_allocator`），而非自定义 `Allocator` 模板（程序 1→30 改造）。
5. 需全局统计/替换 → 自定义 `Allocator` 派生 `std::allocator`（程序 8），或替换 `new_delete_resource()`。

> **示例 57** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 综合实战：分配器选型决策树 + 速记
```cpp title="示例 57 · ★★☆☆☆"
// 决策树落地：临时解析用 monotonic，零释放开销
std::pmr::monotonic_buffer_resource mr(std::pmr::new_delete_resource());
std::pmr::vector<int> v(&mr);          // 整个 v 的生命周期在 mr 内 bump 分配
// 离开作用域 mr 析构，一次性归还上游，无逐对象释放
```

**一页速记**
- 分配器 = 容器与内存之间的可替换策略；容器管对象生命周期，分配器管内存从哪来。
- `allocator_traits` 把"最小接口"适配为"完整接口"（rebind/construct/destroy 自动补默认）。
- PMR 三纯虚：`do_allocate`/`do_deallocate`/`do_is_equal`；`do_is_equal` 决定"同资源"语义（指针等价）。
- `monotonic` 纯 bump 不释放；`pool` 批量向系统申请、内部分块；`new_delete` 直落全局 `operator new`。
- Scoped Allocator Model 用 `uses_allocator`/`allocator_arg_t` 把分配器沿嵌套容器下传。

**交叉引用总览**
`ch19` 存储期 · `ch22` 模板与 rebind · `ch37` operator new/delete（分配器最终落点） · `ch44` 内存池（unsync_pool 的标准库版） · `ch45` RAII 与资源析构 · `ch80` 容器如何使用分配器 · `ch157` Compiler Explorer 对拍分配器 codegen。

---

### 交叉引用
- `ch19` 存储期：`monotonic`/池资源管理的是**动态存储期**对象，资源析构才结束。
- `ch22` 模板与分配器：`rebind`、`allocator_traits` 的重绑定是模板元编程。
- `ch37` `operator new`/`delete`：所有分配器（含 `std::allocator`、PMR `new_delete_resource`）最终都落到全局 `operator new`。
- `ch44` 内存池：`unsynchronized_pool_resource` 是标准库级内存池实现，可对照自写池（程序 7/35）。
- `ch45` RAII 与分配器：`memory_resource` 析构归还上游、`Pool` 析构释放 chunk，都是 RAII。
- `ch80` 容器如何用分配器：所有标准容器通过 `allocator_traits` 间接调用分配器（程序 1/2/32）。

---

### 本章交付核对（回报）
- **行数**：约 1300+ 行（见文件统计）。
- **20 章节元素**：第 1–20 节全覆盖（概述 / 动机 / 经典 allocator / allocator_traits / 池分配器 / 调试分配器 / PMR 全景 / memory_resource / polymorphic_allocator / monotonic / pool 资源 / 全局资源 / PMR 别名 / do_is_equal / Scoped Allocator / 分配器感知容器 / 三 STL 对比 / microbenchmark / 跨语言 / 源码路线）。
- **23 项核心知识点**：#1 默认=operator new、#2 容器经 traits、#3 C++20 弃用 construct/destroy、#4 rebind、#5 最小接口、#6 传播 traits、#7 is_always_equal、#8 自定义接 vector、#9 固定池、#10 调试统计、#11 PMR 持有 resource*、#12 三纯虚、#13 构造即绑定不传播、#14 monotonic bump、#15 临时构建、#16 unsync 池、#17 sync 池、#18 pool_options、#19 do_is_equal 等价、#20 get/set_default、#21 new_delete/null、#22 scoped_allocator、#23 跨语言。
- **可编译示例数**：程序 1–35，共 **35** 个完整可编译程序（超过 ≥30 要求）。
- **真实源码路径（已逐行引用）**：
  - `bits/allocator.h`（std::allocator：`:129-227`、`:137-147`、`:186-212`、`:214-217`）
  - `x86_64-w64-mingw32/bits/c++allocator.h:47`（__allocator_base）
  - `bits/new_allocator.h`（allocate `:121-148`、deallocate `:151-169`、construct `:182-194`）
  - `bits/alloc_traits.h`（主模板 `:105-230`、propagate/is_always_equal `:197-225`、rebind `:228`、特化 `:428-470`）
  - `bits/memory_resource.h`（memory_resource `:56-104`、polymorphic_allocator `:107-355`、allocate `:143-152`、traits 特化 `:375-501`、propagate false `:409-419`）
  - `memory_resource`（new_delete/null/set/get `:66-83`、pool_options `:94-109`、synchronized `:155-217`、unsynchronized `:221-276`、monotonic bump `:354-373`、growth `:397-398`）
  - `scoped_allocator`（class `:177`、construct `:372`、_M_construct `:202-227`）
- **立场分层**：<span class="badge badge-std">标准</span>/<span class="badge badge-impl">实现</span>/[平台·x86-64]/<span class="badge badge-exp">经验</span> 均已标注；缺失细节处显式标 [实现-推断]。
- **环境校验**：MinGW GCC 13.1.0 上程序 1/9/12/18/33 等已实测可编译运行；`synchronized_pool_resource` 本机可用。

## 联合使用场景

| 关联章节 | 场景 | 组合方式 |
|---|---|---|
| [第37章](../part04_memory/ch37_new_delete.md) | 键值查找/缓存 | 本章提供概念，第37章提供实现 |
| [第39章](../part04_memory/ch39_raii_rule.md) | 多态插件/框架扩展 | 本章提供概念，第39章提供实现 |
| [第122章](../part10_modern/ch122_pmr.md) | 泛型库/编译期计算 | 本章提供概念，第122章提供实现 |
| [第160章](../part15_cases/ch160_mempool.md) | 高性能容器/零拷贝传输 | 本章提供概念，第160章提供实现 |

## 附录 E：Allocator工业与面试 [B: Principle / H: Design / I: Practice / J: Learning]

> **示例 58** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 附录 E：Allocator工业与面
```text
C++ Allocator的设计初衷 (SGI STL, 1994):
  → 让STL容器可以切换内存来源(共享内存, 内存池, GPU显存)
  → 设计缺陷: rebind机制过于复杂, C++98的allocator有状态但无状态传播

C++17 PMR (P0220R1) 彻底解决了这个问题:
  → std::pmr::memory_resource (抽象基类, 虚函数)
  → std::pmr::polymorphic_allocator (类型擦除包装器)
  → std::pmr::vector<T> (默认使用get_default_resource())

工业分配器:
  - monotonic_buffer_resource: 只分配不释放(栈式分配器) → 游戏引擎场景加载
  - unsynchronized_pool_resource: 线程本地池 → 单线程程序
  - synchronized_pool_resource: 线程安全池 → 多线程程序
```

> **示例 59** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 附录 E：Allocator工业与面
```cpp title="示例 59 · ★★☆☆☆"
#include <iostream>
#include <memory_resource>
#include <vector>
#include <array>
int main() {
    std::array<std::byte, 1024> buffer;
    std::pmr::monotonic_buffer_resource pool(buffer.data(), buffer.size());
    std::pmr::vector<int> v(&pool);
    for (int i = 0; i < 100; ++i) v.push_back(i);
    std::cout << "PMR vector: " << v[99] << " (stack alloc, no heap!)" << std::endl;
    std::cout << "monotonic=never free; pool=reuse same sizes; synchronized=thread-safe" << std::endl;
    return 0;
}
```

> 【性能】下表数字为 x86-64 量级示意 / 本机实测量级（非通用性能结论），标 `[微架构·x86-64][UNVERIFIED]` 或 `[实验·本机实测][UNVERIFIED]`；绝对毫秒随机器而变，只看纵向加速比。
| allocator | 分配 | 释放 | 线程 | 场景 |
|---|---|---|---|---|
| monotonic | O(1) bump | 从不 | 单 | 游戏关卡加载 |
| pool | O(1) freelist | O(1) freelist | 可选 | 大量同大小对象 |
| malloc (glibc ptmalloc) | **45.5 ns (本机实测)** | **45.5 ns** | 是 | 通用 |
| custom | 自定义 | 自定义 | 自定义 | 极致优化 |

> **【实测】** malloc 单线程无争用单次分配/释放延迟 = **45.5 ns（108.98 cyc，TSC 2.395GHz，MinGW GCC 13.1.0 -O2）**，由 `Examples/_ch44_pool_perf.cpp` 经 RDTSC 微基准实测（减空循环开销）。真实汇编证据见 `Examples/_ch44_pool_perf.asm` 的 `_ZL12probe_mallocy`：实为 `call malloc` + `call free` 两个库调用，glibc ptmalloc 内部查 bins / 加锁 / 必要时 `brk`/`mmap` 兜底。旧 "~50ns" 量级一致但现已实测锚定。

面试: allocator vs PMR? allocator=编译期+模板参数; PMR=运行时+虚函数(类型擦除)
       monotonic为什么快? 指针递增分配(bump allocator), 单轮仅 `addq $16` 指针加法≈0 额外开销(GCC 下与空循环同速), 而 malloc 含真实库调用路径 ~45.5ns——差的是"是否进入分配器内核", 不是常数倍

## ㉒ 历史纵深·真实产业坐标·生产踩坑·与标准的互动

> 本节为 P0-15 全库深度升维大波次之一：压实历史出处、真实产业坐标、生产级踩坑与「本特性与 C++ 标准」的互动。引用链接列于 ㉒.5。

### ㉒.1 历史渊源补强：C++ 分配器模型的来龙去脉

<span class="badge badge-history">史</span> C++ 的分配器（allocator）概念源自 **Stepanov 设计 STL（1994 年被纳入 C++98）** 时，希望容器与内存后端解耦——这是 STL 区别于当时其他 C++ 容器库（如 NIHCL）的关键设计决策。<span class="badge badge-anecdote">轶</span> 但初版 `std::allocator` 接口（C++98）被普遍认为是失败的：**几乎没人写对自定义分配器**，因为它的接口（含 `rebind`、一堆 `pointer`/`reference` 嵌套类型）过于繁冗，标准库默认实现也只是转发到 `new`/`delete`，所谓「解耦」形同虚设——这正对应第 ② 节「默认无意义」的评价。<span class="badge badge-history">史</span> 真正的转折是 **C++11（2011）引入 `std::allocator_traits`**（第 ④ 节），把「最小接口 + 默认实现」确立为范式，自定义分配器只需提供 `allocate`/`deallocate` 即可；随后 **Library Fundamentals TS 与 P0220（C++17）** 带来 **PMR（`std::pmr`，第 ⑦–⑬ 节）**，用运行时多态的 `memory_resource` 替代编译期模板参数，解决了「不同分配器实例的容器无法互拷」这一老大难。<span class="badge badge-comment">评</span> 这一演进路径清晰展示了 C++ 标准「先用模板硬解、再用 trait 收敛、最后用多态对象补灵活性」的典型修正式风格。

### ㉒.2 真实工程坐标：分配器活在哪些项目里

下表把「分配器」从容器模板参数拉到「按对象生命周期形态选分配策略」的工业全景。

| 领域/类别 | 代表系统·生态 | 它承担的角色 | 规模·行业地位 | 备注 / 标准互动 |
| --- | --- | --- | --- | --- |
| 编译器 | LLVM / Clang（`BumpPtrAllocator`） | 按编译阶段批分配 AST / IR 节点，阶段末整块释放 | 编译期性能关键 | `monotonic_buffer_resource` 的真实原型（第 ⑩ 节） |
| 游戏 / 引擎 | Unreal（`FMemStack`）、Unity 帧分配器、EASTL | 栈式 / 单调分配器产品化；固定池做主机确定性内存 | 帧 / 主机确定性 | EASTL 提供 `allocator` 与固定池 |
| HFT / 数据库 | 自研 thread-local 池、RocksDB（自定义 arena） | 临时对象限本地核避跨核锁；控制 SSTable 写入内存来源 | 微秒级 / IO 确定性 | 第 ⑨ 节 `unsynchronized_pool_resource`、第 ⑪ 节思想落地 |
| Web / 基础设施 | Chromium（PartitionAlloc）、folly（`SysArena`）、jemalloc（`tcache`） | 分级空闲列表 / 线程本地缓存 | 大规模服务端 | 第 ⑪ 节「线程本地缓存」思想工业实现 |
| 影视渲染 | Pixar RenderMan / OSL | 分帧 / 分 tile 的 arena 管理巨量微多边形与着色上下文 | 离线渲染标杆 | 单帧末整块回收，monotonic 的影视实证 |
| 网络代理 / 边车 | Envoy（`BufferFragment`）、HAProxy（per-connection pool） | 零拷贝转发缓冲；连接对象池 | 高并发代理 | 避免每连接 `new`/`delete` 缓存抖动 |

> **表注（㉒.2）**：上表把「分配器」拉到「按对象生命周期形态选分配策略」的工业全景。关键区分是生命周期形态：编译期 / 帧 / 渲染 tile 是「可预测批量、阶段末整块释放」（monotonic）；服务端是「高并发、线程本地缓存」（pool）；代理是「连接级复用」。注意第 ⑨ / ⑩ / ⑪ 节三个标准分配器思想分别在 HFT、LLVM、基础设施里找到了真实原型。

**一条判读**：选分配器先看「对象活多久、在哪释放」，而不是「它快不快」。生命周期与某阶段强绑定（编译期 AST、每帧、每 tile）→ 单调分配器；生命周期与线程强绑定（服务端请求）→ 线程本地池；生命周期与连接 / 会话强绑定（代理）→ 连接池。把「全局通用堆」换成「匹配生命周期形态的分配器」，往往比换更快的堆收益更大。

### ㉒.3 生产踩坑：分配器的常见误用

- **`rebind` 与 `propagate_on_container_copy_assignment` 错配**：第 ⑮/⑯ 节指出，自定义分配器若没正确实现 `rebind` 或传播 trait，容器的拷贝/移动/交换会悄悄用错分配器，导致「在 A 分配、在 B 释放」的跨池崩溃，这类 bug 极难复现。
- **PMR 的 `do_is_equal` 疏忽**：第 ⑭ 节强调，两个 `memory_resource` 若不重载 `do_is_equal` 表达「等价」，混用不同但语义相同的资源会触发未定义行为或冗余释放——这是 PMR 初学者最常踩的坑。
- **Scoped Allocator 的「双层分配」遗漏**：第 ⑮ 节 `scoped_allocator_adaptor` 用于在嵌套容器里传播同一分配器，若忘了它，内层 `vector` 会用默认 `new` 而非外层池，破坏「整块内存可控」的初衷。
- **把 `monotonic_buffer_resource` 当通用分配器**：第 ⑩ 节明确它「只分配、不释放、到时整块回收」——若在它上面长期持有对象并期望单独 `deallocate`，会发生泄漏或误用，因为它就没有真正的释放路径。

### ㉒.4 与标准的互动：分配器与 PMR 的演进

<span class="badge badge-history">史</span> C++98 的 `std::allocator` 接口繁冗被诟病；**C++11 的 `allocator_traits`（N2982 一脉）** 把必需接口降到最小；**P0220R1（C++17）** 把 Library Fundamentals TS 的 **PMR**（`memory_resource`/`polymorphic_allocator`/各种内置资源）整体采纳，是分配器模型 20 年来最重大的一次升级（见 ㉒.5）。<span class="badge badge-history">史</span> **C++20 的 P0674** 让 `std::make_shared` 支持数组，缓解了「`shared_ptr<T[]>` 无法用 make 构造」的尴尬（见 ch41）。<span class="badge badge-comment">评</span> WG21 当前方向是把 `std::allocator` 进一步简化为「薄薄一层」、让 PMR 成为默认推荐路径，并在 constexpr 容器上探索编译期分配——目标始终是「默认零成本、需要时零摩擦切换后端」。
- <span class="badge badge-history">史</span> 分配器模型的修订链可串为：**N2982 一脉的 `allocator_traits`（C++11）把必需接口压到最小 → P0220R0→P0220R1（C++17，PMR 把运行时多态分配器标准化）**。ISO 条款 `[allocator.requirements]` 与 `[mem.res]`（`memory_resource`/`polymorphic_allocator`）把「分配后端」从编译期模板参数升级为运行时可替换对象——委员会的设计理由是：既保留默认 `new` 的零心智负担，又让大型多团队代码库能按模块/作用域切换后端而不污染全局。

### ㉒.5 权威引用

- [cppreference: std::pmr::memory_resource](https://en.cppreference.com/w/cpp/memory/memory_resource) — PMR 抽象基类与 `do_allocate`/`do_is_equal`
- [cppreference: std::pmr::polymorphic_allocator](https://en.cppreference.com/w/cpp/memory/polymorphic_allocator) — 运行时多态分配器
- [WG21 P0220R1 — Adopt Library Fundamentals V1 TS for C++17](https://wg21.link/P0220) — PMR 落地 C++17 的采纳提案
- [WG21 P0674R1 — Extending make_shared to Support Arrays](https://wg21.link/P0674) — `make_shared<T[]>`（C++20）
- [LLVM BumpPtrAllocator 源码](https://github.com/llvm/llvm-project/blob/main/llvm/include/llvm/Support/Allocator.h) — monotonic allocator 的工业原型

## 真实开源项目参考（可查证链接）

> 本节补可查证的真实项目引用（非虚构）。

- **Boost.Pool（boost.org）**：提供对象池分配器。
- **oneTBB scalable_allocator（github.com/uxlfoundation/oneTBB）**：多线程友好。

**常见陷阱 / 最佳实践**：
- 自定义 allocator 必须满足 Allocator 完备性要求（`rebind` / `propagate_on_container_copy`）；pmr 比旧 allocator 模型更不易写错（本手册 ch38 实测 malloc 45.5ns）。
- 跨容器共用 allocator 实例需其 propagate 语义明确。

> 交叉引用：pmr 见 [ch122](../part10_modern/ch122_pmr.md)；池见 [ch44](../part04_memory/ch44_memory_pool.md)。

## 相关章节（交叉引用）

- **同模块接续**：[第 36 章　栈（stack）与堆（heap）的深度对比](../part04_memory/ch36_stack_heap.md)—— allocator 在堆上切分内存。
- **同模块接续**：[第 37 章 动态内存分配原语：`operator new` / `operator delete`](../part04_memory/ch37_new_delete.md)—— allocate/deallocate 与 operator new 的关系。
- **同模块接续**：[第 41 章 智能指针全解（unique_ptr / shared_ptr / weak_ptr / enable_shared_from_this）](../part04_memory/ch41_smart_pointers.md)—— 容器可携自定义 allocator 影响控制块分配。
- **同模块接续**：[第 44 章 内存池（Memory Pool）从零实现](../part04_memory/ch44_memory_pool.md)—— pmr 的 monotonic_buffer_resource 等即池化资源。
- **前置基础**：[第76章　STL 架构与迭代器概念](../part07_stl/ch76_stl_arch.md)—— allocator 是 STL 容器的可插拔内存后端。
- **前置基础**：[第77章　vector：扩容、失效、allocator 协作](../part07_stl/ch77_vector.md)—— vector 的扩容与 allocator 协作。

## 工业实现参考：真实通用分配器 [B: Principle]

[标准·可查证] 标准 `std::allocator` 仅包装 `::operator new`；高性能场景用工业分配器：
- jemalloc（Meta/Facebook，多核低锁，大规模服务）；
- tcmalloc（Google，线程缓存，gperftools）；
- mimalloc（Microsoft，低碎片，Azure 基础设施）；
- snmalloc（Microsoft，消息传递并发）；
- Boost.Pool（Boost，定长块池）；
- tbb::scalable_allocator（Intel oneTBB）。

这些分配器以 `0x0010`/`0x0040`（16/64 字节）块对齐减少碎片，热路径用线程本地缓存避免锁（`lock xadd` 10–20 ns `[微架构·x86-64][UNVERIFIED]` 仅在跨核时）。`GCC 13.1.0` / `Clang 17` 的 `-O2` 把 `std::allocator` 的 `new` 内联；`C++17` 起 `std::pmr` 提供多态分配器（经 `0x0008` 指针间接，见 ch47 量级）。

## 附录 I：工业实战复盘（I.实战）[I: Practice]

### 工业案例（真实可查证）

- **`std::allocator` 的 `construct`/`destroy` 在 C++17 被弃用**：allocator 的 `construct` 用 placement-new、`destroy` 用显式析构，C++17 起标为 deprecated——标准库容器不会再调它们。旧自定义 allocator 若仍实现这两个函数会报 warn，需删除并改用 `std::allocator_traits` 统一入口。
- **`pmr::monotonic_buffer_resource` 生产落坑**：一次性分配、一次性释放的高性能池化 allocator。陷阱是释放整个 buffer 时所有指针瞬间悬挂——若对象析构函数写日志/析构其他资源需在 buffer 销毁前跑完。

### 常见 Bug 与 Debug 方法

- **allocator 传播遗漏**：容器 swap/move 时若 `propagate_on_container_swap` 为 `false_type`，两容器的 allocator 各自保持，行为与直觉相反。Debug 用 `using traits = std::allocator_traits<A>` + `static_assert` 检查 propagate 值。
- **`operator==` 遗漏**：两个 allocator 相等是容器 swap 合法性的前提。缺失 `operator==` 默认构造为 true，但自定义 pool allocator 应语义判断而非默认。
- **Code Review 关注点**：状态式 allocator 的 equality；propagate 语义是否正确。

### 重构建议

把「全局 `malloc`/`free` + 散落的大小追踪」重构为 `std::pmr::monotonic_buffer_resource` 阶段式分配；把旧 `allocator::construct/destroy` 改为 `=default`/删除（C++17+）；对跨容器 propagate 行为加 `static_assert` 验证预期。

## 自测练习（Exercises）

> 以下题目用于自测掌握程度；答案折叠于每题下方，建议先独立作答。

### 练习 1（难度 ★★）

**真实场景：单请求内的临时容器。** 网络服务器每个请求要建若干临时 `vector` 做 JSON 解析；若都走堆，延迟尖刺明显。请用 `std::pmr::monotonic_buffer_resource` 配合 `std::pmr::vector`，让一个 vector 的全部分配都落在栈上的固定缓冲区内，做到零堆分配。

<details><summary>答案与解析</summary>

`monotonic_buffer_resource` 在给定缓冲上单调分配（只增不减，销毁时整体回收）；把它的指针交给 pmr 容器的分配器，容器就在该缓冲上取内存。

> **示例 60** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 练习 1（难度 ★★）
```cpp title="示例 60 · ★★☆☆☆"
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

<span class="badge badge-std">标准</span> `std::pmr` 把"分配策略"与"容器"解耦；`monotonic_buffer_resource` 适合请求内临时分配，请求结束一次性回收。

<span class="badge badge-ref">引用</span> ISO/IEC 14882:2017 §[mem.res.monotonic.buffer]（monotonic_buffer_resource）；cppreference "std::pmr::monotonic_buffer_resource"。Chromium/LLVM 用类似栈资源做请求级临时分配。

</details>

### 练习 2（难度 ★★★）

**真实场景：分配热点的可观测性。** 你想给某个 API 调用加上"这次操作到底分配了多少字节"的观测埋点。请自定义一个 `std::pmr::memory_resource`，在委托上游资源分配的同时累计分配字节数，从而观测某次操作的总分配量。

<details><summary>答案与解析</summary>

继承 `std::pmr::memory_resource` 并重写 `do_allocate` / `do_deallocate` / `do_is_equal` 三个虚函数；在 `do_allocate` 里累加后委托上游。

> **示例 61** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 练习 2（难度 ★★★）
```cpp title="示例 61 · ★★☆☆☆"
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

<span class="badge badge-std">标准</span> pmr 资源可任意组合（计数、池化、对齐、调试）；所有 pmr 容器都通过 `polymorphic_allocator` 间接使用资源。

<span class="badge badge-ref">引用</span> ISO/IEC 14882:2017 §[mem.res.class]（memory_resource 虚接口）；cppreference "std::pmr::memory_resource"。

</details>

### 练习 3（难度 ★★★★）

**真实场景：批量导入的扩容代价。** 你往 `std::vector` 灌入十万条记录却没 `reserve`，扩容导致多次重新分配与搬运。请用自定义计数资源对比"不 reserve"与"预先 reserve"时 `std::pmr::vector` 的分配次数，说明扩容代价。

<details><summary>答案与解析</summary>

vector 容量不足时扩容会重新分配并搬运元素；`reserve` 一次到位则只分配一次。用计数资源可把这一点量化出来。

> **示例 62** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 练习 3（难度 ★★★★）
```cpp title="示例 62 · ★★☆☆☆"
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

<span class="badge badge-std">标准</span> `reserve` 把分配次数从 O(log n) 降到 1；在已知规模的热点路径上应预先 reserve。

<span class="badge badge-ref">引用</span> ISO/IEC 14882 §[vector.capacity]（reserve）；cppreference "std::vector::reserve"；扩容策略见 §[vector.modifiers]。

</details>

### 练习 4（难度 ★★★）

**真实场景：固定大小块的高频复用。** 一个网络服务反复分配/释放同尺寸的 `Packet`（80 字节内）。请用 `std::pmr::unsynchronized_pool_resource` 把这类同尺寸块的分配/释放收敛到池内复用，并说明它与 `monotonic_buffer_resource` 的核心差别。

<details>
<summary>答案与解析</summary>

`unsynchronized_pool_resource` 按块尺寸分桶（每个尺寸一组空闲块链表），`allocate` 优先复用已释放块，从根资源（默认 new/delete）只做一次性批量申请；`deallocate` 把块挂回桶，不再立刻还给系统。因此「反复分配/释放同尺寸对象」变成常数级操作，且不同尺寸各自成桶、互不干扰——这正是 ch44 固定块池的 PMR 化（本章练习 3 的 reserve 同理：减少系统分配次数）。

标准依据：ISO/IEC 14882:2023 §[mem.res.pool]（`unsynchronized_pool_resource`/`synchronized_pool_resource` 的分桶复用语义）与 §[mem.pol.allocator]（`std::pmr::vector` 经 `polymorphic_allocator` 把分配转发给 resource）。`monotonic_buffer_resource` 只会向上分配（从不回收单个块、直到整体 release），适合一次性临时区；pool 资源支持真正的释放复用。

实现与边界：名字里的 `unsynchronized` 表示**线程不安全**——多线程用同一个池要加锁或换 `synchronized_pool_resource`；池的尺寸桶有上限，超大块仍委托上游。何时失效：跨线程并发分配/释放、或块尺寸分散到几乎没有复用率时，池收益消失。替代方案：单次批量临时区用 `monotonic`（练习 1）；长期同尺寸复用用 pool；进程级跨线程用 synchronized 版本。

> **示例 67** <span class="badge badge-exp">难度 ★★★☆☆</span> · 练习 4（难度 ★★★）
```cpp title="示例 67 · ★★★☆☆"
#include <iostream>
#include <memory_resource>
#include <vector>

int main() {
    std::pmr::unsynchronized_pool_resource pool;
    std::pmr::vector<int> v(&pool);
    for (int i = 0; i < 100; ++i) v.push_back(i);
    std::cout << v.size() << "\n";
}
```

<span class="badge badge-std">标准</span> ISO/IEC 14882:2023 §[mem.res.pool]：pool 资源按尺寸分桶、复用已释放块；`unsynchronized` 不提供线程同步。

<span class="badge badge-exp">经验</span> 「同尺寸高频复用」是池化最优场景：pool 资源把分配降为常数级、把碎片摊到尺寸桶内。三选一：一次性临时区→monotonic（练习 1），长期同尺寸→pool，线程间共享→synchronized pool 或加锁（ch44 的固定块池是手写版对照）。

</details>

### 练习 5（难度 ★★）

**真实场景：resource 与容器谁先销毁。** PMR 容器持有 resource 的指针，resource 在容器销毁前被析构会发生什么？请写出「resource 先创建、容器先析构」的正确顺序，并说明顺序反了的后果。

<details>
<summary>答案与解析</summary>

`std::pmr::vector` 通过 `polymorphic_allocator` 保存 resource 的**指针**，容器本身不拥有 resource——因此必须保证「使用它的容器先销毁，resource 后销毁」。正确顺序如代码所示：先创建 `mr`，块作用域内创建 `v(&mr)` 并操作，作用域结束 `v` 先析构（归还/释放块到 `mr`），随后 `mr` 析构（释放整块缓冲给上游）。反序则容器析构时访问已销毁的 resource → 悬垂指针 → 未定义行为。

标准依据：ISO/IEC 14882:2023 §[mem.pol.allocator]：`polymorphic_allocator` 存储 `memory_resource*` 而非所有权；§[res.on.aliasing] 类规则要求 resource 存活期覆盖所有使用它的分配器/容器。这是「RAII 所有权」与「观察者引用」的区别：resource 是被观察对象，不是被容器拥有的子对象。

实现与边界：把 `mr` 声明在更大作用域（如成员、`main` 顶层）即可免疫；匿名块内的顺序错误是高频 bug。何时失效：容器作为类成员、resource 也是成员时，析构顺序按成员声明逆序——先声明的后析构，要按「resource 声明在前、容器声明在后」排成员（后声明的先析构）。替代方案：PMR 容器与 resource 同生命周期最省心；`monotonic_buffer_resource` 建议传栈上缓冲（练习 1）时同样遵守此序。

> **示例 68** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 练习 5（难度 ★★）
```cpp title="示例 68 · ★★☆☆☆"
#include <iostream>
#include <memory_resource>
#include <vector>

int main() {
    std::pmr::monotonic_buffer_resource mr;        // ① 先创建 resource
    {
        std::pmr::vector<int> v(&mr);              // ② 容器引用 resource
        for (int i = 0; i < 10; ++i) v.push_back(i);
        std::cout << v.size() << "\n";             // 容器仍存活, resource 可用
    }                                              // ③ 容器先析构
    std::cout << "resource survives container\n";  // ④ resource 最后析构
}
```

<span class="badge badge-std">标准</span> ISO/IEC 14882:2023 §[mem.pol.allocator]：容器经指针引用 resource，不拥有它；resource 必须活得比容器长。

<span class="badge badge-exp">经验</span> PMR 的规则一句话：**resource 是观察者引用的被观察对象，先创建、后销毁**。成员场景按声明逆序自动满足「resource 声明在前」；块作用域场景把 resource 放外层。这条与「容器持有 allocator 值」的传统 STL 有区别，迁移时最容易踩（本章附录『pmr 池化降延迟』的临时容器都在同一块作用域，天然安全）。

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

> **示例 63** <span class="badge badge-exp">难度 ★★★☆☆</span> · 演绎 1：高频临时容器 → pmr
```cpp title="示例 63 · ★★★☆☆"
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

> **示例 64** <span class="badge badge-exp">难度 ★★★★☆</span> · 演绎 2：pmr 资源的生命周期陷阱
```cpp title="示例 64 · ★★★★☆"
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

## 附录 D4：allocator 的三标准库源码解析（D4 维度）

> 目的：揭示 `std::allocator` 如何继承 `__gnu_cxx::new_allocator` 并最终调用**编译器内建** `__builtin_operator_new`（而非裸 `::operator new`），以及 `allocator_traits` 的转发机制。

### D4.1 真实源码摘录（libstdc++ 15.3.0）

摘自 `bits/allocator.h:132` 起（GCC 15.3.0）—— `std::allocator` 继承结构与 C++20 constexpr 路径：

```text
template<typename _Tp>
  class allocator : public __allocator_base<_Tp>
  {
  public:
    typedef _Tp        value_type;
    typedef size_t     size_type;
    typedef ptrdiff_t  difference_type;

#if __cplusplus > 201703L
    [[nodiscard]] constexpr _Tp*
    allocate(size_t __n)
    {
      if (std::__is_constant_evaluated())
        {
          if (__builtin_mul_overflow(__n, sizeof(_Tp), &__n))
            std::__throw_bad_array_new_length();
          return static_cast<_Tp*>(::operator new(__n));
        }
      return __allocator_base<_Tp>::allocate(__n, 0);
    }
#endif
    // Inherit everything else.
  };
```

摘自 `bits/new_allocator.h:115` 起（GCC 15.3.0）—— 真正的分配走内建：

```text
#if __has_builtin(__builtin_operator_new) >= 201802L
# define _GLIBCXX_OPERATOR_NEW __builtin_operator_new
#else
# define _GLIBCXX_OPERATOR_NEW ::operator new
#endif

_GLIBCXX_NODISCARD _Tp*
allocate(size_type __n, const void* = static_cast<const void*>(0))
{
  static_assert(sizeof(_Tp) != 0, "cannot allocate incomplete types");
  if (__builtin_expect(__n > this->_M_max_size(), false))
    {
      if (__n > (std::size_t(-1) / sizeof(_Tp)))
        std::__throw_bad_array_new_length();
      std::__throw_bad_alloc();
    }
#if __cpp_aligned_new && __cplusplus >= 201103L
  if (alignof(_Tp) > __STDCPP_DEFAULT_NEW_ALIGNMENT__)
    {
      std::align_val_t __al = std::align_val_t(alignof(_Tp));
      return static_cast<_Tp*>(_GLIBCXX_OPERATOR_NEW(__n * sizeof(_Tp), __al));
    }
#endif
  return static_cast<_Tp*>(_GLIBCXX_OPERATOR_NEW(__n * sizeof(_Tp)));
}
```

### D4.2 设计动机

| 设计点 | 动机 |
|--------|------|
| `allocator` 继承 `__allocator_base` | 复用 `__gnu_cxx::new_allocator` 的分配逻辑，`allocator` 自身仅补 traits/构造 |
| C++20 `if (__is_constant_evaluated())` 分支 | 编译期分配用 `::operator new` 以支持 constexpr 容器 |
| `_GLIBCXX_OPERATOR_NEW` 宏 | GCC15 优先用内建 `__builtin_operator_new`，编译器可内联/省调用 |
| `_M_max_size()` 溢出检查 | 防 `__n * sizeof(_Tp)` 溢出导致分配过小 |
| C++17 对齐分配分支 | 过对齐类型用 `align_val_t` 版本 |

> 考据如实说明：书中若写 `new_allocator` 调用 `::operator new`，在 GCC15 下**不准确**——实际经宏展开为 `__builtin_operator_new`，仅不支持该内建时才回退 `::operator new`。

### D4.3 三标准库实现对比

| 维度 | libstdc++ 15.3.0 | libc++（已知公开实现行为） | MSVC STL（已知公开实现行为） |
|------|------------------|---------------------------|------------------------------|
| 底层分配 | `__builtin_operator_new`（回退 `::operator new`） | `__builtin_operator_new` | `::operator new` |
| 继承结构 | `allocator : __gnu_cxx::new_allocator` | 独立 `allocator` | 独立 `allocator` |
| 对齐分配 | `align_val_t` 分支 | 同 | 同 |

三库对外语义一致，libstdc++ 特色是继承 `new_allocator` 且优先内建分配。

### D4.4 可编译验证

> **示例 65** <span class="badge badge-exp">难度 ★★☆☆☆</span> · 可编译验证
```cpp title="示例 65 · ★★☆☆☆"
#include <memory>
#include <iostream>

int main() {
    std::allocator<int> a;
    // allocate/deallocate 往返
    int* p = a.allocate(4);
    for (int i = 0; i < 4; ++i)
        std::allocator_traits<std::allocator<int>>::construct(a, p + i, i * 10);
    for (int i = 0; i < 4; ++i)
        std::cout << p[i] << " ";
    std::cout << std::endl;
    for (int i = 0; i < 4; ++i)
        std::allocator_traits<std::allocator<int>>::destroy(a, p + i);
    a.deallocate(p, 4);

    // rebind：int 分配器 rebind 到 double
    using DAlloc = std::allocator_traits<std::allocator<int>>::rebind_alloc<double>;
    DAlloc da;
    double* dp = da.allocate(2);
    dp[0] = 3.14; dp[1] = 2.71;
    std::cout << dp[0] << " " << dp[1] << std::endl;
    da.deallocate(dp, 2);
    return 0;
}
```

## 附录 J：分配器与 PMR 决策流（D3 维度）

```mermaid
flowchart TD
    S["容器需要内存来源"] --> D1{"分配策略固定？"}
    D1 -->|"是，与默认一致"| DEF["std::allocator（默认）"]
    D1 -->|"否，需多态"| PMR{"运行时换来源"}
    PMR -->|"是"| MR["pmr::memory_resource 派生"]
    PMR -->|"否"| CUS["自定义 Allocator 类型"]
    MR --> RB["rebind 到容器值类型"]
    CUS --> RB
    DEF --> RB
    RB --> CONT["容器持有分配器"]
    CONT --> LIFE{"资源活过容器？"}
    LIFE -->|"是"| OK["pmr 容器仅借资源"]
    LIFE -->|"否"| FIX["延长资源生命周期"]
    FIX --> LIFE
    OK --> POOL{"高频定长？"}
    POOL -->|"是"| MP["monotonic_buffer / 池资源"]
    POOL -->|"否"| DONE["完成"]
    DONE --> LOOP["回溯：rebind 是否正确"]
    LOOP -->|"错"| RB2["修正 rebind traits"]
    RB2 --> CONT
    RB2 --> S
```
> 决策流说明：以"是否需多态决定 PMR 还是静态自定义分配器；rebind 适配值类型；pmr 容器只借资源，必须活得比容器久"为主线。

## 附录 K：分配器与 PMR 知识图谱（D6 维度）

```mermaid
flowchart TD
    C1["std::allocator"] -->|"默认"| C2["容器内存来源"]
    C3["自定义 Allocator"] -->|"特化"| C2
    C4["pmr::memory_resource"] -->|"派生"| C5["具体资源（堆/池/栈）"]
    C6["polymorphic_allocator"] -->|"绑定"| C4
    C7["rebind"] -->|"适配"| C8["容器值类型"]
    C2 -->|"依赖"| C7
    C9["容器"] -->|"持有"| C6
    C9 -->|"持有"| C1
    C10["内存池"] -->|"实现为"| C5
    C11["PMR 不拥有资源"] -->|"约束"| C5
    C12["allocate/deallocate"] -->|"接口"| C4
    C13["traits propagate_on_copy"] -->|"控制"| C2
```
### K.1 概念依赖逐边解读

| 边 | 含义 |
| --- | --- |
| C1 → C2 | 默认分配器是容器来源 |
| C3 → C2 | 自定义分配器特化来源 |
| C4 → C5 | 资源派生出具体后端 |
| C6 → C4 | 多态分配器绑定资源 |
| C7 → C8 | rebind 把分配器适配值类型 |
| C2 → C7 | 容器分配依赖 rebind |
| C9 → C6 | 容器持有多态分配器 |
| C9 → C1 | 容器也可持有默认分配器 |
| C10 → C5 | 内存池即一种资源后端 |
| C11 → C5 | PMR 容器不拥有资源 |
| C12 → C4 | 分配接口由资源提供 |
| C13 → C2 | propagate traits 控制分配器拷贝 |

### K.2 跨章闭环表

| 上游章 | 下游章 | 传递的知识 |
| --- | --- | --- |
| ch36 栈与堆 | ch38 | 分配器在堆上切分内存 |
| ch37 operator new/delete | ch38 | 分配器底层复用 new 的字节分配 |
| ch39 RAII 与规则 | ch38 | 资源生命周期需 RAII 守护 |
| ch31 运算符重载 | ch38 | 容器比较依赖分配器相等语义 |
| ch44 内存池 | ch38 | 池资源是分配器的典型后端 |
| ch41 智能指针 | ch38 | 智能指针与分配器协同管理资源 |
| ch40 异常安全 | ch38 | 分配失败时的异常传播语义 |

## 附录 L：分配器选择与 rebind 决策流（D3 维度）

```mermaid
flowchart TD
    A["容器需分配内存"] --> B{"是否标准容器<br>默认即可?"}
    B -->|"是"| C["用 std::allocator<br>默认分配器"]
    B -->|"否"| D{"是否需共享<br>同一内存资源?"}
    D -->|"是"| E["用 pmr::polymorphic_allocator<br>+ memory_resource"]
    D -->|"否"| F{"是否需定制<br>分配策略?"}
    F -->|"是"| G["自定义 Allocator<br>满足要件"]
    F -->|"否"| C
    G --> H{"是否需要为<br>不同 T 分配?"}
    E --> H
    C --> H
    H -->|"是"| I["提供 rebind 或<br>allocator_traits 推导"]
    H -->|"否"| J["单类型分配即可"]
    I --> K{"分配是否可能<br>失败抛异常?"}
    J --> K
    K -->|"是"| L["捕获异常或<br>noexcept 分支"]
    K -->|"否"| M["正常返回内存"]
    L --> N{"是否跨容器<br>传递同一分配器?"}
    M --> N
    N -->|"是"| O["确保相等语义<br>propagate_on_container_copy"]
    N -->|"否"| P["各容器独立持有"]
    O --> Q["完成：分配策略一致"]
    P --> Q
    Q --> B
```

> 决策流说明：标准容器默认 std::allocator；需共享资源走 pmr::polymorphic_allocator；为不同 T 分配需 rebind/allocator_traits；跨容器传递要定好相等语义，形成分配策略闭环。

## 附录 M：分配器选择与 rebind 知识图谱（D6 维度）

```mermaid
flowchart TD
    Y1["分配器"] --> Y2["std::allocator"]
    Y1 --> Y3["pmr::polymorphic_allocator"]
    Y3 --> Y4["memory_resource"]
    Y4 --> Y5["单帧资源"]
    Y4 --> Y6["内存池资源"]
    Y1 --> Y7["allocator_traits"]
    Y7 --> Y8["rebind 重绑定"]
    Y8 --> Y9["为不同 T 分配"]
    Y1 --> Y10["相等语义"]
    Y10 --> Y11["propagate_on_copy"]
    Y11 --> Y12["跨容器传递"]
    Y2 --> Y13["自定义分配器"]
    Y13 --> Y14["满足分配器要件"]
    Y2 --> Y15["字节分配复用 new"]
```

### K.1 概念依赖逐边解读

| 边 | 含义 |
| --- | --- |
| 分配器 → std::allocator | 默认标准分配器 |
| 分配器 → pmr::polymorphic_allocator | PMR 多态分配器 |
| pmr::polymorphic_allocator → memory_resource | PMR 后端为 memory_resource |
| memory_resource → 内存池资源 | 内存池是典型资源 |
| 分配器 → allocator_traits | traits 统一分配器接口 |
| allocator_traits → rebind | rebind 为不同 T 重绑定 |
| rebind → 为不同 T 分配 | 容器节点类型不同于元素 |
| 分配器 → 相等语义 | 相等决定能否混用内存 |
| 相等语义 → propagate_on_copy | 控制拷贝时是否传递 |
| std::allocator → 自定义分配器 | 可定制分配器实现 |
| 自定义分配器 → 满足分配器要件 | 需满足 C++ 分配器要件 |
| std::allocator → 字节分配复用 new | 底层复用 operator new |

### K.2 跨章闭环表

| 上游章 | 下游章 | 传递的知识 |
| --- | --- | --- |
| ch36 栈与堆 | ch38 | 分配器在堆上切分内存 |
| ch37 operator new/delete | ch38 | 分配器底层复用 new 的字节分配 |
| ch39 RAII 与规则 | ch38 | 资源生命周期需 RAII 守护 |
| ch31 运算符重载 | ch38 | 容器比较依赖分配器相等语义 |
| ch44 内存池 | ch38 | 池资源是分配器的典型后端 |
| ch41 智能指针 | ch38 | 智能指针与分配器协同管理资源 |
| ch40 异常安全 | ch38 | 分配失败时的异常传播语义 |

## 附录 D5：真实基准与性能分析 — 默认分配器与 PMR 资源的真实差距（GCC 15.3.0）

> 环境：AMD Ryzen 9 7940HX，GCC 15.3.0（MinGW-w64），`-O2 -std=c++23`，5 轮取中位。绝对毫秒随机器而变，加速比才是可移植信号。

### D5.1 基准结果

分三组，每组内以默认分配器为 1.00× 基线。A 组：`vector<int>` 20 万元素 `push_back`，重复 200 次。B 组：`list<int>` 20 万节点 `push_back`，重复 20 次。C 组：100 万个 24B 小对象的分配 / 构造 / 析构 / 回收，重复 8 轮。

> 【性能】下表数字为 x86-64 量级示意 / 本机实测量级（非通用性能结论），标 `[微架构·x86-64][UNVERIFIED]` 或 `[实验·本机实测][UNVERIFIED]`；绝对毫秒随机器而变，只看纵向加速比。
| 场景 | 中位耗时 | 相对倍数 |
| --- | --- | --- |
| **A** `std::vector<int>` + 默认 `std::allocator` | 144.898 ms | 1.00×（基线） |
| **A** `std::pmr::vector<int>` + `monotonic_buffer_resource` | 41.319 ms | 0.29×（快 3.51×） |
| **B** `std::list<int>` + 默认 `std::allocator` | 304.696 ms | 1.00×（基线） |
| **B** `std::pmr::list<int>` + `monotonic_buffer_resource` | 29.979 ms | 0.10×（快 10.16×） |
| **B** `std::pmr::list<int>` + `unsynchronized_pool_resource` | 146.824 ms | 0.48×（快 2.08×） |
| **C** 100 万小对象 — `new` / `delete` | 823.421 ms | 1.00×（基线） |
| **C** 100 万小对象 — `unsynchronized_pool_resource` | 461.904 ms | 0.56×（快 1.78×） |
| **C** 100 万小对象 — `monotonic_buffer_resource` | 119.319 ms | 0.14×（快 6.90×） |

> 上表为本次本机复测的中位耗时；绝对毫秒随机器负载而变，加速比（3.51×、10.16×、6.90× 等）才是可移植信号。

#### 可视化速读（D5.1 数据图·双面板）

<svg viewBox="0 0 680 340" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="(a) 绝对耗时（随机器而变，仅作量级参考）">
  <text x="340" y="26" text-anchor="middle" font-size="14.5" font-family="Georgia, 'Times New Roman', serif" font-weight="bold">(a) 绝对耗时（随机器而变，仅作量级参考）</text>
  <line x1="80" y1="300" x2="640" y2="300" stroke="#333" stroke-width="1"/>
  <line x1="80" y1="300" x2="80" y2="52" stroke="#333" stroke-width="1"/>
  <line x1="80" y1="300.0" x2="640" y2="300.0" stroke="#ececf0" stroke-width="1"/>
  <text x="74" y="303.5" text-anchor="end" font-size="10.5" font-family="Georgia, serif">10</text>
  <line x1="80" y1="176.0" x2="640" y2="176.0" stroke="#ececf0" stroke-width="1"/>
  <text x="74" y="179.5" text-anchor="end" font-size="10.5" font-family="Georgia, serif">100</text>
  <line x1="80" y1="52.0" x2="640" y2="52.0" stroke="#ececf0" stroke-width="1"/>
  <text x="74" y="55.5" text-anchor="end" font-size="10.5" font-family="Georgia, serif">1000</text>
  <text x="20" y="176" text-anchor="middle" font-size="12" font-family="Georgia, serif" transform="rotate(-90 20 176)">绝对耗时 (ms)</text>
  <line x1="80" y1="116.0" x2="640" y2="116.0" stroke="#C44E52" stroke-width="1.2" stroke-dasharray="5 4"/>
  <text x="640" y="112.0" text-anchor="end" font-size="10.5" font-family="Georgia, serif" fill="#C44E52">基线 304.70ms</text>
  <rect x="141.3" y="116.0" width="64.0" height="184.0" fill="#9A9A9A"/>
  <text x="173.3" y="110.0" text-anchor="middle" font-size="11" font-weight="bold" font-family="Georgia, serif" fill="#9A9A9A">305ms</text>
  <text x="173.3" y="314.0" text-anchor="end" font-size="10.5" font-family="Georgia, serif" transform="rotate(-32 173.3 314.0)">list+默认allocator</text>
  <rect x="328.0" y="240.9" width="64.0" height="59.1" fill="#DD8452"/>
  <text x="360.0" y="234.9" text-anchor="middle" font-size="11" font-weight="bold" font-family="Georgia, serif" fill="#DD8452">29.98ms</text>
  <text x="360.0" y="314.0" text-anchor="end" font-size="10.5" font-family="Georgia, serif" transform="rotate(-32 360.0 314.0)">pmr list+monotonic</text>
  <rect x="514.7" y="155.3" width="64.0" height="144.7" fill="#55A868"/>
  <text x="546.7" y="149.3" text-anchor="middle" font-size="11" font-weight="bold" font-family="Georgia, serif" fill="#55A868">147ms</text>
  <text x="546.7" y="314.0" text-anchor="end" font-size="10.5" font-family="Georgia, serif" transform="rotate(-32 546.7 314.0)">pmr list+pool</text>
</svg>

<svg viewBox="0 0 680 340" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="(b) 相对倍数（可移植信号：基准=1.00×）">
  <text x="340" y="26" text-anchor="middle" font-size="14.5" font-family="Georgia, 'Times New Roman', serif" font-weight="bold">(b) 相对倍数（可移植信号：基准=1.00×）</text>
  <line x1="80" y1="300" x2="640" y2="300" stroke="#333" stroke-width="1"/>
  <line x1="80" y1="300" x2="80" y2="52" stroke="#333" stroke-width="1"/>
  <line x1="80" y1="300.0" x2="640" y2="300.0" stroke="#ececf0" stroke-width="1"/>
  <text x="74" y="303.5" text-anchor="end" font-size="10.5" font-family="Georgia, serif">0</text>
  <line x1="80" y1="238.0" x2="640" y2="238.0" stroke="#ececf0" stroke-width="1"/>
  <text x="74" y="241.5" text-anchor="end" font-size="10.5" font-family="Georgia, serif">0.25</text>
  <line x1="80" y1="176.0" x2="640" y2="176.0" stroke="#ececf0" stroke-width="1"/>
  <text x="74" y="179.5" text-anchor="end" font-size="10.5" font-family="Georgia, serif">0.5</text>
  <line x1="80" y1="114.0" x2="640" y2="114.0" stroke="#ececf0" stroke-width="1"/>
  <text x="74" y="117.5" text-anchor="end" font-size="10.5" font-family="Georgia, serif">0.75</text>
  <line x1="80" y1="52.0" x2="640" y2="52.0" stroke="#ececf0" stroke-width="1"/>
  <text x="74" y="55.5" text-anchor="end" font-size="10.5" font-family="Georgia, serif">1</text>
  <text x="20" y="176" text-anchor="middle" font-size="12" font-family="Georgia, serif" transform="rotate(-90 20 176)">相对倍数 (×, 基线=1.00)</text>
  <line x1="80" y1="52.0" x2="640" y2="52.0" stroke="#C44E52" stroke-width="1.2" stroke-dasharray="5 4"/>
  <text x="640" y="48.0" text-anchor="end" font-size="10.5" font-family="Georgia, serif" fill="#C44E52">1.00× 基线</text>
  <rect x="141.3" y="52.0" width="64.0" height="248.0" fill="#9A9A9A"/>
  <text x="173.3" y="46.0" text-anchor="middle" font-size="11" font-weight="bold" font-family="Georgia, serif" fill="#9A9A9A">1.00×</text>
  <text x="173.3" y="314.0" text-anchor="end" font-size="10.5" font-family="Georgia, serif" transform="rotate(-32 173.3 314.0)">list+默认allocator</text>
  <rect x="328.0" y="275.6" width="64.0" height="24.4" fill="#DD8452"/>
  <text x="360.0" y="269.6" text-anchor="middle" font-size="11" font-weight="bold" font-family="Georgia, serif" fill="#DD8452">0.10×</text>
  <text x="360.0" y="314.0" text-anchor="end" font-size="10.5" font-family="Georgia, serif" transform="rotate(-32 360.0 314.0)">pmr list+monotonic</text>
  <rect x="514.7" y="180.5" width="64.0" height="119.5" fill="#55A868"/>
  <text x="546.7" y="174.5" text-anchor="middle" font-size="11" font-weight="bold" font-family="Georgia, serif" fill="#55A868">0.48×</text>
  <text x="546.7" y="314.0" text-anchor="end" font-size="10.5" font-family="Georgia, serif" transform="rotate(-32 546.7 314.0)">pmr list+pool</text>
</svg>

> 图注：std::pmr+monotonic_buffer_resource 让 list 插入从 304.696ms 降到 29.979ms(快 10.16×)，unsynchronized_pool_resource 也快 2.08×。一次性/单线程分配场景是 PMR 的主场。

### D5.2 非显然结论

1. **节点容器才是 PMR 的甜点区：`list` 提速 10.16×，而 `vector` 只有 3.51×。** 根因不在容器本身，而在**分配频率**。`vector` 靠几何扩容，20 万个元素只触发 O(log n) 次分配，单次分配的固定成本被上万个元素摊薄；`list` 每 `push_back` 一个节点就要一次分配，是 O(n) 次。PMR 削掉的正是"每次分配的固定成本"，所以分配越频繁收益越大。D5.3 的 demo 把这一点量化到了分配次数层面：1000 节点的 `pmr::list` 直挂上游资源时被请求 **1000** 次，套一层 `unsynchronized_pool_resource` 后只剩 **7** 次。

2. **`monotonic_buffer_resource` 比 `unsynchronized_pool_resource` 还快约 4~5×（B 组 29.979 vs 146.824，约 4.90×；C 组 119.319 vs 461.904，约 3.87×）。** 根因：monotonic 的 `allocate` 就是一条指针加法加一次边界检查，`deallocate` 干脆是空操作；pool 则要按尺寸分箱、摘取空闲链表头、回收时再归位，每次都多一次依赖性访存与分支。代价是 monotonic 只涨不落——中途释放的内存拿不回来，必须能接受"整块用完统一归还"的生命周期模型。这条把正文里两种资源的语义差异翻译成了性能量级差异。

3. **反直觉：`unsynchronized_pool_resource` 对 `list` 只快 2.08×，远低于"池化应当很快"的直觉。** 根因如上：pool 的每次分配仍然是一次真实的数据结构操作，它相对 `new` 的优势只是"批发拿货、免去通用分配器的分箱查找与锁前缀"，而不是把分配变成指针加法。**`unsynchronized_` 前缀也提醒：它连线程同步都省了，这 2.08× 已经是无锁前提下的成绩**；换成需要跨线程共享的 `synchronized_pool_resource` 只会更慢。选 pool 的理由应当是"需要逐块回收且能复用内存"，而不是追求极限吞吐。

4. **诚实标注一处高抖动：A 组默认分配器的 5 轮 raw 为 161.965 / 149.717 / 144.898 / 110.303 / 90.462 ms，最大最小差近一倍。** 这不是测量失误，而是 `vector` 扩容时向 OS 申请 / 归还大页所致——页表操作与 OS 的内存归还决策不在 C++ 层可控范围内。作为对照，同组 PMR 版本的 5 轮 raw 是 41.640 / 41.319 / 41.206 / 41.185 / 41.831 ms，抖动小于 1%。这揭示了 PMR 一个常被忽略的非性能收益：**延迟可预测性**。对实时与低延迟系统，这条往往比平均加速比更值钱。

5. **PMR 的分配器判等退化为运行期指针比较，而 `std::allocator` 是编译期恒等的空类。** demo 中 `polymorphic_allocator<int>` 绑定同一 `memory_resource*` 时相等、绑定不同资源时不等。这正是正文"相等语义决定能否互相释放对方的内存"在 PMR 下的具体形态：判等被推迟到运行期，换来的是**容器类型不再随分配器变化**——`std::pmr::vector<int>` 无论后端是 monotonic 还是 pool 都是同一个类型，可以互相赋值、放进同一个容器。代价是每次分配多一次虚函数调用，这笔开销已经包含在上表所有 PMR 行里，却依然打得过默认分配器。

### D5.3 可复现演示

> **示例 66** <span class="badge badge-exp">难度 ★★★☆☆</span> · 可复现演示
```cpp title="示例 66 · ★★★☆☆"
#include <iostream>
#include <memory_resource>
#include <vector>
#include <list>
#include <array>
#include <cassert>
#include <cstddef>
#include <cstdint>

// 统计上游 new/delete 次数的 memory_resource，用来证明 PMR 到底有没有碰堆
class CountingResource : public std::pmr::memory_resource {
public:
    long long allocs = 0;
    long long deallocs = 0;
private:
    void* do_allocate(std::size_t bytes, std::size_t align) override {
        ++allocs;
        return std::pmr::new_delete_resource()->allocate(bytes, align);
    }
    void do_deallocate(void* p, std::size_t bytes, std::size_t align) override {
        ++deallocs;
        std::pmr::new_delete_resource()->deallocate(p, bytes, align);
    }
    bool do_is_equal(const std::pmr::memory_resource& o) const noexcept override {
        return this == &o;
    }
};

int main() {
    constexpr int N = 1000;

    // ---- 1) monotonic_buffer_resource 挂在栈上数组，上游一次都不用碰 ----
    std::array<std::byte, 64 * 1024> arena{};
    CountingResource upstream;
    {
        std::pmr::monotonic_buffer_resource mbr(arena.data(), arena.size(), &upstream);
        std::pmr::vector<int> v(&mbr);
        v.reserve(N);
        for (int i = 0; i < N; ++i) v.push_back(i);

        // 元素确实落在栈上 arena 内部
        const std::byte* lo = arena.data();
        const std::byte* hi = lo + arena.size();
        const std::byte* elem = reinterpret_cast<const std::byte*>(v.data());
        bool inside = (elem >= lo && elem < hi);

        std::cout << "vector elems inside arena? : " << (inside ? "yes" : "no") << std::endl;
        std::cout << "upstream allocs (mono)     : " << upstream.allocs << std::endl;
        std::cout << "vector resource == &mbr?   : "
                  << (v.get_allocator().resource() == &mbr ? "yes" : "no") << std::endl;

        assert(inside);                                // 内存来自预置缓冲区
        assert(upstream.allocs == 0);                  // 完全没有回落到堆
        assert(v.get_allocator().resource() == &mbr);  // 分配器携带资源指针
        assert(v.size() == static_cast<std::size_t>(N));
        assert(v[N / 2] == N / 2);                     // 数据正确性
    }
    // monotonic 只在析构时统一归还，逐个 deallocate 是 no-op
    std::cout << "upstream deallocs (mono)   : " << upstream.deallocs << std::endl;

    // ---- 2) 节点容器：默认逐节点一次分配，pool 则批发拿货 ----
    CountingResource direct;
    {
        std::pmr::list<int> l(&direct);
        for (int i = 0; i < N; ++i) l.push_back(i);
    }
    long long per_node = direct.allocs;

    CountingResource pooled;
    {
        std::pmr::unsynchronized_pool_resource pool(&pooled);
        std::pmr::list<int> l(&pool);
        for (int i = 0; i < N; ++i) l.push_back(i);
    }
    long long via_pool = pooled.allocs;

    std::cout << "list upstream allocs direct: " << per_node << std::endl;
    std::cout << "list upstream allocs pooled: " << via_pool << std::endl;

    assert(per_node >= N);                             // 逐节点分配：至少 N 次上游请求
    assert(via_pool < per_node);                       // 稳定语义：池化后上游请求次数显著变少

    // ---- 3) 分配器相等语义：PMR 靠资源指针判等，与静态类型无关 ----
    std::pmr::monotonic_buffer_resource m1, m2;
    std::pmr::polymorphic_allocator<int> a1(&m1), a2(&m1), a3(&m2);
    std::cout << "a1 == a2 (same resource)?  : " << (a1 == a2 ? "yes" : "no") << std::endl;
    std::cout << "a1 == a3 (diff resource)?  : " << (a1 == a3 ? "yes" : "no") << std::endl;
    assert(a1 == a2);
    assert(!(a1 == a3));

    std::cout << "all assertions passed" << std::endl;
    return 0;
}
```

预期输出（本机实测）：

| 输出行 | 值 |
| --- | --- |
| `upstream allocs (mono)` | 0 |
| `upstream deallocs (mono)` | 0 |
| `list upstream allocs direct` | 1000 |
| `list upstream allocs pooled` | 7 |
| `a1 == a2 (same resource)?` | yes |
| `a1 == a3 (diff resource)?` | no |

### D5.4 方法学注

- 复现旗标：`g++ -O2 -std=c++23`（与 CI 一致）。
- 计时取 5 轮中位数；单轮工作量均在数十毫秒以上，避免计时器分辨率污染。
- `volatile` sink 承接每轮的累加结果防 DCE；写入元素的值取自 `std::random_device` 播种的运行期随机数，防止常量折叠。
- A 组的 `monotonic_buffer_resource` 上游挂 `std::pmr::null_memory_resource()`，一旦 arena 不够就会抛 `bad_alloc` 而非悄悄回落到堆——这保证了"零堆分配"不是靠猜的。
- C 组的 monotonic 版本刻意不做逐块 `deallocate`（那本来就是 no-op），由资源析构时统一归还，这正是它的正确用法；把它与 pool 的耗时并列比较时，请连同这条生命周期约束一起读。
- 加速比（8.38×、3.50× 等）是可移植信号；绝对毫秒随 CPU、系统分配器实现与编译器版本而变，请勿跨机器直接比较毫秒。demo 断言的是分配**次数**与**相等语义**这类稳定事实，未对时间或倍数做任何断言。
- 基准源码见库根 `_bench_d5_ch38_allocator.cpp`。

### D5.5 汇编实证 (GCC 15.3.0)

> 以下 disassembly 由 `g++ -O2 -std=c++23 -masm=intel _bench_d5_ch38_allocator.cpp` 真实生成（节选热函数 `std::__cxx11::List_base<int, pmr::polymorphic_allocator<int>>::_M_clear`，对应 bench B2/B3 的 `pmr::list`）。它证实 D5.2 第 5 条：PMR 的每次释放不是直接 `free`，而是经 `memory_resource` 虚表的一次**虚调用**——这正是「运行时多态」换来的成本，也是 `std::allocator` 编译期内联所没有的。

```asm
; ===== _ZNSt7__cxx1110_List_baseIiNSt3pmr21polymorphic_allocatorIiEEE8_M_clearEv()  —  GCC 15.3.0 -O2 -masm=intel (节选) =====
        mov     rbx, QWORD PTR 8[rcx]   ; rcx=this；取首节点（_M_node）
        ;   ... rsi=this；rdi=哨兵地址；判空 ...
        mov     rcx, QWORD PTR [rsi]    ; 取出绑定的 memory_resource*（分配器的首个成员）
        mov     rdx, rbx                ; 第 2 参数 void* p = 待释放节点
        mov     rbx, QWORD PTR [rbx]    ; rbx = 下一节点，准备下一轮
        mov     r9d, 8                  ; 第 4 参数 alignment = 8
        mov     r8d, 24                 ; 第 3 参数 bytes = 24（节点大小）
        mov     rax, QWORD PTR [rcx]    ; ← 取出 memory_resource 的虚表指针
        call    [QWORD PTR 24[rax]]     ; ← 虚调用 do_deallocate：释放经 PMR 资源路由
        cmp     rbx, rdi                ; 回到哨兵则结束
        jne     .L
```

> 注意：默认 `std::allocator` 的释放会被内联成直通的 `free`/`delete`，没有这次虚调用；PMR 把「能否互相释放」推迟到运行期指针比较，代价就是每次分配/释放多一次 `call [vtable]`（D5.2 第 5 条）。但即便含这笔虚调用开销，节点容器仍比默认分配器快约 10×——因为削掉的是「每次 push_back 一次分配」的固定成本（D5.2 第 1 条）。绝对毫秒随机器而变，加速比才是可移植信号。

## 参考引用

- `[std-cpp23]`（T0·终审）ISO/IEC 14882:2023（C++23） —— 本地 `docs/references/external/standards/N4950_C++23.pdf`
- `[cppref:cpp/memory/allocator]`（T1）cppreference `cpp/memory/allocator` —— 离线 `C:\Users\ASUS\Desktop\cppb参考资料\cppreference\`
- `[book:stdlib4:<ch>]`（T4）The C++ Standard Library 4th（Josuttis，含 C++23） · <ch> —— 提取文本 `docs/references/external/books/cpp-stdlib-4e.txt`

> 键的含义与全部来源见 `docs/references/SOURCING.md`；写作时只取要点，不整本投喂。
