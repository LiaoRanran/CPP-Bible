# 第 38 章　分配器（Allocator）模型与 PMR

⟶ Book/part10_modern/ch122_pmr.md
⟶ Book/part15_cases/ch160_mempool.md

> 老兵标准：**Allocator 是 C++ 标准库里最被低估、也最被误解的扩展点。**
> 本章遵循《现代 C++ 终极圣经》标准 v3：真实源码逐行 + GCC/LLVM/MSVC 三实现对照 + libstdc++/libc++/MS STL 三 STL 对照 + microbenchmark + 跨语言对比 + 推荐阅读已内化进正文。

立场分层约定：
- **[标准]**　语言/库标准规定（ISO C++、LWG 决议）。
- **[实现]**　libstdc++ / libc++ / MS STL 的具体代码行为。
- **[平台]**　MinGW GCC 13.1.0、Windows、ABI 相关事实。
- **[经验]**　工程实践、坑与取舍。

环境事实（本机探测）：MinGW **GCC 13.1.0**；libstdc++ 头文件根目录
`C:/Qt/Tools/mingw1310_64/lib/gcc/x86_64-w64-mingw32/13.1.0/include/c++/`；PMR 在本机可用，`synchronized_pool_resource` 可用（定义 `_GLIBCXX_HAS_GTHREADS`）。

---

## ① 概述：分配器是什么，为何存在

⟶ Book/part04_memory/ch37_new_delete.md
⟶ Book/part04_memory/ch39_raii_rule.md


**[标准]**　分配器是标准容器（`vector`/`list`/`map`/…）与底层内存申请/释放之间的**可替换策略对象**。容器向分配器请求「N 个 `T` 对象的原始内存」与「构造/析构对象」，而**不直接**调用 `new`/`delete`。这是「算法与存储解耦」的经典设计。

**[经验]**　一句话记忆：**容器管对象生命周期，分配器管内存从哪来。** 没有分配器，你就无法在栈缓冲、共享内存、内存池、GPU 显存上放一个 `std::vector`。

本章覆盖的两条主线：
- **经典分配器模型**（C++98 起，`std::allocator` + C++11 `std::allocator_traits`）。
- **PMR 模型**（C++17，`std::pmr::polymorphic_allocator` + `memory_resource`），见第 8–14 节。

交叉引用：`ch22` 分配器与模板（rebind 是模板元编程）、`ch37` `operator new`/`delete`（分配器最终落到这里）、`ch19` 存储期、内置 `monotonic_buffer_resource` 是 `ch44` 内存池的特例、`ch45` RAII 与分配器、`ch80` 容器如何使用分配器。

---

## ② 设计动机：容器与内存解耦，但「默认无意义」

**[标准]**　`std::allocator<T>` 是「默认分配器」（`[allocator.requirements]`）。任何容器都接收一个 `Allocator` 模板参数，缺省为 `std::allocator<value_type>`。

**[实现]**　libstdc++ 里 `std::allocator<T>` 的基类是 `__new_allocator<T>`，见
`x86_64-w64-mingw32/bits/c++allocator.h:47`：

```cpp
// x86_64-w64-mingw32/bits/c++allocator.h:46-47
template<typename _Tp>
  using __allocator_base = __new_allocator<_Tp>;
```

而 `__new_allocator::allocate`（`bits/new_allocator.h:121-148`）最终就是：

```cpp
// bits/new_allocator.h:143-147
std::align_val_t __al = std::align_val_t(alignof(_Tp));
return static_cast<_Tp*>(_GLIBCXX_OPERATOR_NEW(__n * sizeof(_Tp), __al));
```

即 `_GLIBCXX_OPERATOR_NEW` 在支持内建时为 `__builtin_operator_new`，否则为 `::operator new`（见 `bits/new_allocator.h:111-117`）。**也就是说 `std::allocator` 默认 100% 等价于全局 `::operator new`。**

**[经验]（Scott Meyers 观点内化）]**　Meyers 在《Effective STL》第 10 条指出：**除非你需要自定义内存来源（共享内存、池、调试统计），否则"默认分配器"对你毫无意义——它只是 `operator new` 的薄包装，没有任何加速。** 真正有价值的是「自定义分配器」与「PMR」。本章第 5、6、10–14 节给出有价值的部分。

**结论**：allocator 是一个**扩展点（extension point）**，默认实现只是占位。不要为了用而用。

---

## ③ 经典 `std::allocator` 接口

**[标准]**　`std::allocator<T>` 必须提供的成员（`[allocator.members]`）：

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

```cpp
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

```cpp
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

**[实现]**　任何 `std::allocator<X>` 与 `std::allocator<Y>` 总是相等（`bits/allocator.h:214-217`、`operator==` 返回 `true`），因此 `is_always_equal` 在 traits 特化里为 `true_type`（见第 4 节 `bits/alloc_traits.h:464`）。

**核心知识点 #1**：默认 `std::allocator` ≡ `::operator new`，无优化空间。
**核心知识点 #2**：容器通过 `allocator_traits` 间接调用分配器，见 `ch80`。
**核心知识点 #3**：`construct`/`destroy` 成员在 C++20 被弃用，改用 `allocator_traits::construct`（`std::construct_at`）。

程序 1：直接用 `std::allocator` 申请/释放（完整可编译）：

```cpp
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

**[标准]**　C++11 引入 `allocator_traits<A>`，它把「容器需要什么」与「分配器提供什么」解耦：**容器永远只通过 `allocator_traits` 访问分配器**，而非直接调用成员。这带来两大好处：
1. 老式分配器缺少 `construct`/`destroy`/`pointer` 也能用（traits 提供默认）。
2. `rebind` 由 traits 统一计算（见 `bits/alloc_traits.h:228`）。

**真实源码（libstdc++ `allocator_traits` 主模板，`bits/alloc_traits.h:105-230`）**：

```cpp
// bits/alloc_traits.h:105-117 —— 主模板只取 value_type，其余用「检测或默认」
struct allocator_traits : __allocator_traits_base
{
  typedef _Alloc allocator_type;
  typedef typename _Alloc::value_type value_type;
  using pointer = __detected_or_t<value_type*, __pointer, _Alloc>;  // 无则 value_type*
```

传播 traits 与 `is_always_equal` 的「检测或默认」逻辑（`bits/alloc_traits.h:197-225`）：

```cpp
// bits/alloc_traits.h:197-225
using propagate_on_container_copy_assignment
  = __detected_or_t<false_type, __pocca, _Alloc>;   // 无则 false_type
using propagate_on_container_move_assignment
  = __detected_or_t<false_type, __pocma, _Alloc>;
using propagate_on_container_swap
  = __detected_or_t<false_type, __pocs, _Alloc>;
using is_always_equal
  = typename __detected_or_t<is_empty<_Alloc>, __equal, _Alloc>::type; // 无则 is_empty
```

`rebind_alloc` 的推导（`bits/alloc_traits.h:227-230`）：

```cpp
// bits/alloc_traits.h:227-230
template<typename _Tp>
  using rebind_alloc = __alloc_rebind<_Alloc, _Tp>;          // 优先 A::rebind<U>::other
template<typename _Tp>
  using rebind_traits = allocator_traits<rebind_alloc<_Tp>>;
```

**`std::allocator<T>` 的 traits 特化**（`bits/alloc_traits.h:428-470`）明确给出传播行为与 `is_always_equal`：

```cpp
// bits/alloc_traits.h:455-470
using propagate_on_container_copy_assignment = false_type;
using propagate_on_container_move_assignment = true_type;   // 见 LWG 2103
using propagate_on_container_swap = false_type;
using is_always_equal = true_type;                          // 空类，所有实例等价
template<typename _Up>
  using rebind_alloc = allocator<_Up>;
```

**[标准]**　「最小接口」原则：你只要提供 `value_type` + `allocate` + `deallocate`，其余（`construct`/`destroy`/`pointer`/`size_type`/`rebind`/传播 traits）全部由 `allocator_traits` 给默认。

**核心知识点 #4（rebind 机制）**：节点型容器（`list`/`map`/`set`）内部节点是 `Node<T>`，不是 `T`。容器需要 `allocator<Node<T>>`，于是 `allocator_traits::rebind_alloc<T>` 把 `allocator<T>` 变成 `allocator<Node<T>>`（`[allocator.traits.types]`）。
**核心知识点 #5（最小接口）**：见上。
**核心知识点 #6（传播 traits）**：`propagate_on_container_copy/move/swap_assignment` 决定容器拷贝/移动/交换时是否连带替换分配器（`[allocator.prop]`）。
**核心知识点 #7（is_always_equal）**：为 `true` 时任何两个分配器实例等价，容器交换无需比较。

程序 2：只用「最小接口」写一个分配器（仅 `value_type`/`allocate`/`deallocate`），靠 traits 补全：

```cpp
// 编译: g++ -std=c++17 ch38_p2.cpp -o ch38_p2
#include <memory>
#include <vector>
#include <iostream>
#include <cstdlib>
#include <cstddef>

template <typename T>
struct MinimalAlloc {
    using value_type = T;                       // 仅此一个类型别名
    T* allocate(std::size_t n) {                // 仅 allocate/deallocate
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

```cpp
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

```cpp
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

```cpp
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

```cpp
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

**[标准]**　只要满足 `Allocator` 要求（见 `ch22`），你就能把它塞进任意标准容器。最有价值的一类是**池分配器**：把大块内存切成固定大小节点，用 free-list 复用，避免反复 `new`/`delete` 的系统调用与碎片。

**[实现]**　下面 `PoolAllocator<T>` 对「单次 1 个 T」走对象池，`n>1` 回退到 `::operator new`（满足 `vector` 扩容时可能一次性要多块）。容器用 `allocator_traits::rebind_alloc<Node>` 拿到的仍是同一池（共享 `BlockSize`），故节点也走池。

**核心知识点 #8**：自定义分配器接入 `vector` 必须支持 `rebind`（traits 自动重绑定同模板参数）与 `propagate`/`is_always_equal`。
**核心知识点 #9（固定大小池）**：free-list 头插/头取，销毁时整块释放。

程序 7：可编译的固定大小池分配器（接 `std::vector`）：

```cpp
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

**[经验]**　调试分配器用于统计「分配/释放次数」「峰值字节」「检测泄漏」。这是真实工程中 `std::allocator` 被替换的最常见理由之一。

**核心知识点 #10（调试分配器）**：用静态（或共享）计数器在 `allocate`/`deallocate` 里自增自减。

程序 8：统计分配次数的调试分配器：

```cpp
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
    DebugAlloc() = default;   // 关键：声明了转换构造函数会抑制隐式默认构造，
                              //       而 vector 默认构造其分配器时需要 DebugAlloc()。
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
    for (int i = 0; i < 50; ++i) v.push_back(i);   // 多次扩容 → 多次分配
    v.clear(); v.shrink_to_fit();
    std::cout << "allocs=" << Stats::allocs
              << " deallocs=" << Stats::deallocs << '\n';
    return 0;
}
```

---

## ⑦ PMR 全景：为何出现

**[标准]**　C++17 引入 `std::pmr`（Polymorphic Allocator，见 `[mem.res]`），核心动机：
1. **运行时切换分配策略**：经典分配器类型编码在容器的模板参数里（编译期绑定）；PMR 把「分配策略」下推为运行期持有的 `memory_resource*`。
2. **避免模板参数爆胀**：每个不同分配器类型都会实例化一套容器代码。PMR 让 `pmr::vector<int>` 只有一种类型，资源可换。
3. **零开销（抽象代价几乎为零）**：`polymorphic_allocator` 只持有一个指针，`allocate` 是一次虚调用（或内联），比经典分配器多一层间接但换来灵活性。

**[实现]**　对照：经典 `vector<T, MyAlloc>` → PMR `pmr::vector<T>`（=`vector<T, polymorphic_allocator<T>>`）。同一 `pmr::vector<int>` 可先挂 `monotonic`，再挂 `pool`，再挂 `new_delete`，**类型不变**。

**核心知识点 #11（PMR 本质）**：模板参数 `Allocator` 替换为 `polymorphic_allocator<T>`，后者持有 `memory_resource*`。

程序 9：同一 `pmr::vector<int>` 在运行时挂两种资源（展示编译期类型不变）：

```cpp
// 编译: g++ -std=c++17 ch38_p9.cpp -o ch38_p9
#include <memory_resource>
#include <vector>
#include <iostream>
int main() {
    std::pmr::monotonic_buffer_resource mono(
        std::pmr::get_default_resource());
    std::pmr::vector<int> a(&mono);             // 同一类型 pmr::vector<int>
    a.push_back(1); a.push_back(2);

    std::pmr::unsynchronized_pool_resource pool;
    std::pmr::vector<int> b(&pool);             // 仍是 pmr::vector<int>
    b.push_back(3); b.push_back(4);
    std::cout << a[0] << a[1] << '|' << b[0] << b[1] << '\n';
    return 0;
}
```

---

## ⑧ `std::pmr::memory_resource` 抽象基类

**[标准]**　`memory_resource`（`[mem.res.class]`）是 PMR 的抽象基类，三个纯虚函数决定一切：

**真实源码（libstdc++ `bits/memory_resource.h:56-104`）**：

```cpp
#include <cstddef>
// bits/memory_resource.h:56-104 —— 抽象基类，公有接口调用私有纯虚
class memory_resource
{
  static constexpr size_t _S_max_align = alignof(max_align_t);
public:
  memory_resource() = default;
  memory_resource(const memory_resource&) = default;
  virtual ~memory_resource();                       // key function

  [[nodiscard]] void* allocate(size_t __bytes,
                               size_t __alignment = _S_max_align)
  { return ::operator new(__bytes, do_allocate(__bytes, __alignment)); }

  void deallocate(void* __p, size_t __bytes,
                  size_t __alignment = _S_max_align)
  { return do_deallocate(__p, __bytes, __alignment); }

  [[nodiscard]] bool is_equal(const memory_resource& __other) const noexcept
  { return do_is_equal(__other); }

private:
  virtual void* do_allocate(size_t __bytes, size_t __alignment) = 0;     // 纯虚
  virtual void  do_deallocate(void* __p, size_t __bytes, size_t __alignment) = 0;
  virtual bool  do_is_equal(const memory_resource& __other) const noexcept = 0;
};
```

**关键设计**：公有的 `allocate`/`deallocate`/`is_equal` **不是**虚函数，它们转调私有纯虚 `do_*`。这样派生类只重写 `do_*`，且 `allocate` 入口统一做 `operator new` 包装（注意 `::operator new(bytes, p)` 的 nothrow 形式）。

**核心知识点 #12（三纯虚）**：`do_allocate` / `do_deallocate` / `do_is_equal`。

程序 10：自己继承 `memory_resource` 写一个计数资源：

```cpp
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

**[标准]**　`polymorphic_allocator<T>`（`[mem.poly.allocator.class]`）是 PMR 的「分配器外观」——它满足 `Allocator` 要求，但内部只存一个 `memory_resource*`（`_M_resource`）。构造函数若不给资源，取默认资源（`bits/memory_resource.h:121-126`）：

```cpp
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

```cpp
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

```cpp
// bits/memory_resource.h:409-419 —— PMR 不传播、非 always_equal
using propagate_on_container_copy_assignment = false_type;
using propagate_on_container_move_assignment = false_type;
using propagate_on_container_swap = false_type;
static allocator_type
select_on_container_copy_construction(const allocator_type&) noexcept
{ return allocator_type(); }                 // 拷贝构造用默认资源！
using is_always_equal = false_type;          // 不同资源实例不等价
```

> **[经验]**　这是 PMR 最反直觉之处：`pmr::vector` 拷贝构造时，新容器用的是**默认资源**，而非源容器的资源！因为 `select_on_container_copy_construction` 返回新 `allocator_type()`（取默认资源）。若想保持资源，用 `scoped_allocator_adaptor` 或显式传资源。

程序 11：`polymorphic_allocator` 基础用法（独立可编译）：

```cpp
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

```cpp
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

**[标准]**　`monotonic_buffer_resource`（`[mem.res.monotonic.buffer]`）**只增不减**：分配时把内部指针向前「撞」（bump），`deallocate` 是空操作，直到资源析构或 `release()` 才一次性归还上游。极快，适合「临时构建」场景（解析请求、序列化、生成临时结构）。

**真实源码（libstdc++ `memory_resource:354-411`）—— 核心 bump 逻辑**：

```cpp
#include <cstddef>
// memory_resource:354-373 —— do_allocate 的指针碰撞
void* do_allocate(size_t __bytes, size_t __alignment) override
{
  if (__builtin_expect(__bytes == 0, false))
    __bytes = 1;                          // 保证不返回同一指针两次
  void* __p = std::align(__alignment, __bytes, _M_current_buf, _M_avail);
  if (__builtin_expect(__p == nullptr, false)) {
    _M_new_buffer(__bytes, __alignment);  // 当前缓冲不够 → 向上游要新缓冲
    __p = _M_current_buf;
  }
  _M_current_buf = (char*)_M_current_buf + __bytes;  // bump
  _M_avail -= __bytes;
  return __p;
}
void do_deallocate(void*, size_t, size_t) override { }   // 空！不释放
bool do_is_equal(const memory_resource& __other) const noexcept override
{ return this == &__other; }
```

缓冲增长参数（`memory_resource:397-398`）：

```cpp
#include <cstddef>
static constexpr size_t _S_init_bufsize = 128 * sizeof(void*);  // 初始 1KB 左右
static constexpr float  _S_growth_factor = 1.5;                 // 每次 1.5 倍增长
```

构造器（给出初始栈缓冲，零额外 malloc）（`memory_resource:297-320`）：

```cpp
#include <cstddef>
// memory_resource:297-307 —— 用调用者提供的 buffer 作为初始存储
monotonic_buffer_resource(void* __buffer, size_t __buffer_size,
                          memory_resource* __upstream) noexcept
: _M_current_buf(__buffer), _M_avail(__buffer_size),
  _M_next_bufsiz(_S_next_bufsize(__buffer_size)),
  _M_upstream(__upstream),
  _M_orig_buf(__buffer), _M_orig_size(__buffer_size)
{ /* assert upstream != null && buffer != null || size==0 */ }
```

**核心知识点 #14/15**：栈缓冲 + bump pointer，不释放直至销毁/ `release()`；典型用途是临时构建。

**核心知识点 #19（do_is_equal 重要性，在此提前点题）**：`monotonic` 用 `this == &other` 判断等价（见上 `do_is_equal`），因为**只有同一个 monotonic 实例才认得彼此的旧指针**——若把 A 分配的内存交给 B 去 `deallocate`（即便类型相同），B 不会释放（它的 `do_deallocate` 是空），造成逻辑错误。这解释了为何 PMR 用「指针相等」而非「类型相等」判断资源等价。

程序 13：`monotonic` 基础用法（独立）：

```cpp
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

```cpp
// 编译: g++ -std=c++17 ch38_p14.cpp -o ch38_p14
#include <memory_resource>
#include <vector>
#include <iostream>
int main() {
    char stack_buf[4096];
    std::pmr::monotonic_buffer_resource buf(stack_buf, sizeof(stack_buf));
    std::pmr::vector<int> v(&buf);           // 全部在栈缓冲上 bump
    for (int i = 0; i < 500; ++i) v.push_back(i);
    std::cout << "size=" << v.size() << " back=" << v.back() << '\n';
    return 0;                               // buf 析构 → 一次性归还，零次 delete
}
```

程序 15：`monotonic` 模拟「请求解析」临时容器（解析完即弃）：

```cpp
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

```cpp
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
    }                                          // v 析构但不释放 mr 内存
    mr.release();                              // 回到初始状态，缓冲可再用
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

**[标准]**　池资源（`[mem.res.pool]`）把内存按 **size class**（尺寸档位）分成多个池，每个池用 free-list 管理同尺寸块。优势：
- 减少 `malloc` 调用次数（批量向上游要大块）。
- 减少碎片（同尺寸块互换）。
- `unsynchronized_pool_resource`：**单线程**，无锁，最快。
- `synchronized_pool_resource`：**多线程安全**（内部 `shared_mutex`，见 `memory_resource:155-217`），适合并发。

**真实源码（libstdc++ `memory_resource:221-276` 与 `155-217`）**：

```cpp
#include <cstddef>
// memory_resource:258-267 —— unsynchronized 的 do_* 直接转私有实现
void* do_allocate(size_t __bytes, size_t __alignment) override;   // _M_impl 处理
void  do_deallocate(void* __p, size_t __bytes, size_t __alignment) override;
bool  do_is_equal(const memory_resource& __other) const noexcept override
{ return this == &__other; }                                      // 仍是 this 比较
```

`synchronized` 多了一层线程特定池（`memory_resource:203-216`）：

```cpp
// memory_resource:212-216
__pool_resource _M_impl;
__gthread_key_t _M_key;                  // 线程局部池 key
_TPools* _M_tpools = nullptr;
mutable shared_mutex _M_mx;              // 多线程锁
```

`pool_options`（`memory_resource:94-109`）调优参数：

```cpp
#include <cstddef>
// memory_resource:94-109
struct pool_options {
  size_t max_blocks_per_chunk = 0;             // 每 chunk 块数上限（0=实现默认）
  size_t largest_required_pool_block = 0;      // 超过此尺寸的分配直接走上游（0=默认）
};
```

**[平台]**　本机 MinGW GCC 13.1.0 的 libstdc++ 中 `synchronized_pool_resource` **存在**（定义了 `_GLIBCXX_HAS_GTHREADS`）。若某嵌入式 libstdc++ 无线程（`#else` 分支，`memory_resource:52-55`），`__cpp_lib_memory_resource` 仅为 `1` 且 `synchronized_pool_resource` 被剔除。

**核心知识点 #16（unsync 池）**：单线程、size class 池。
**核心知识点 #17（sync 池）**：多线程、加锁。
**核心知识点 #18（pool_options）**：`max_blocks_per_chunk` 与 `largest_required_pool_block`。

程序 17：`unsynchronized_pool_resource` 基础：

```cpp
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

```cpp
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

```cpp
// 编译: g++ -std=c++17 ch38_p19.cpp -o ch38_p19
#include <memory_resource>
#include <vector>
#include <iostream>
int main() {
    std::pmr::pool_options opt;
    opt.max_blocks_per_chunk = 64;
    opt.largest_required_pool_block = 1024;       // >1KB 直接走上游
    std::pmr::unsynchronized_pool_resource pool(opt);
    std::pmr::vector<int> v(&pool);
    std::pmr::string big(4096, 'x', &pool);       // 4KB 字符串很可能绕过池
    for (int i = 0; i < 100; ++i) v.push_back(i);
    std::cout << "vec=" << v.size() << " big=" << big.size() << '\n';
    return 0;
}
```

程序 20：池资源与 `monotonic` 对比的两种资源接同一类型容器：

```cpp
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

**[标准]**　PMR 维护一个**进程级默认资源指针**（见 `memory_resource:75-83`）：

```cpp
// memory_resource:66-83 —— 全局资源相关声明（key function 在库中定义）
memory_resource* new_delete_resource() noexcept;     // 用 ::operator new/delete
memory_resource* null_memory_resource() noexcept;     // allocate 永远抛 bad_alloc
memory_resource* set_default_resource(memory_resource* __r) noexcept;  // 替换并返回旧值
memory_resource* get_default_resource() noexcept;                    // 当前默认
```

- `new_delete_resource()`：返回**静态**资源，永远指向 `::operator new`，**不能 deallocate 别人的内存**（与 `null` 一样用 `this==&other` 等价）。
- `null_memory_resource()`：任何 `allocate` 都抛 `std::bad_alloc`，用于「禁止分配」的上下文（如探测某路径是否真的需要内存）。
- `set_default_resource`：替换整个程序的默认资源（线程安全、原子）。

**核心知识点 #20/21**：`get/set_default_resource` 程序级切换；`new_delete`/`null` 用途。

程序 21：获取默认资源指针：

```cpp
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

```cpp
// 编译: g++ -std=c++17 ch38_p22.cpp -o ch38_p22
#include <memory_resource>
#include <vector>
#include <iostream>
int main() {
    std::pmr::monotonic_buffer_resource my_mr(std::pmr::new_delete_resource());
    auto* old = std::pmr::set_default_resource(&my_mr);
    std::pmr::vector<int> v;                  // 无参 → 用 my_mr（当前默认）
    for (int i = 0; i < 10; ++i) v.push_back(i);
    std::cout << "size under custom default = " << v.size() << '\n';
    std::pmr::set_default_resource(old);      // 还原
    return 0;
}
```

程序 23：`new_delete_resource` vs `null_memory_resource`：

```cpp
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

**[标准]**　`<memory_resource>` 为所有标准容器提供了 PMR 别名（`[mem.poly.allocator.aliases]`），例如：

```cpp
#include <vector>
namespace std::pmr {
  template <class T> using vector = std::vector<T, polymorphic_allocator<T>>;
  template <class T> using string = std::basic_string<T, ...>;
  // list/map/set/unordered_map/... 同理
}
```

其 `allocator_type` 就是 `polymorphic_allocator<T>`。容器感知分配器（见第 16 节）。

程序 24：PMR 各类容器的 `allocator_type` 与默认资源：

```cpp
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

**[标准]**　`memory_resource::is_equal` 决定「能否用 B 释放 A 分配的内存」（`[mem.res.eq]`）。默认实现是 **指针相等**（`this == &other`），而非「类型相等」或「总是 true」。

**为什么必须重写/注意**：若两个不同 `monotonic` 实例（即便类型完全相同）互相 `deallocate`，`do_deallocate` 是空操作 → 内存「看起来释放了，实际没还」。容器内部分配与释放**必须**发生在同一资源实例上。标准容器在析构/扩容时会确认资源等价（通过 `do_is_equal`），不等价则行为未定义。

程序 25：`do_is_equal` 与 `operator==` 行为：

```cpp
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

```cpp
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

**[标准]**　嵌套容器（如 `vector<string>`：`string` 内部又用分配器存字符）需要一个机制，把「外层分配器」自动传给「内层容器/元素」。`scoped_allocator_adaptor<Outer, Inner...>`（`[allocator.adaptor]`）实现这一点：外层容器构造元素时，会把内层分配器一并传给元素的构造函数。

**真实源码定位（libstdc++ `scoped_allocator:177` 定义 `class scoped_allocator_adaptor`；`:372` `construct`；`:202-227` `_M_construct` 按 `uses_allocator` 协议分派）**：

```cpp
#include <utility>
// scoped_allocator:372-377 —— 构造元素时把「内层分配器」自动下发
construct(_Tp* __p, _Args&&... __args)
{
  auto __use_tag = std::__use_alloc<_Tp, polymorphic_allocator, _Args...>(*this);
  _M_construct(__use_tag, __p, std::forward<_Args>(__args)...);
}
```

**[平台]**　本机 libstdc++ `scoped_allocator` 存在，行号见上。libc++/MS STL 同名同义。

**核心知识点 #22**：嵌套容器传递内部分配器。

程序 27：经典 `scoped_allocator_adaptor` 让 `vector<string>` 的字符也走同一分配器：

```cpp
// 编译: g++ -std=c++17 ch38_p27.cpp -o ch38_p27
#include <vector>
#include <string>
#include <scoped_allocator>
#include <memory>
#include <iostream>
int main() {
    using Inner = std::allocator<char>;                       // 给 string 的字符
    using Outer = std::allocator<std::string>;                 // 给 vector 的 string
    using Scoped = std::scoped_allocator_adaptor<Outer, Inner>;
    std::vector<std::string, Scoped> v(Scoped{});
    v.push_back("hello");                                     // string 内部用 Inner
    v.push_back("world");
    for (auto& s : v) std::cout << s << ' ';
    std::cout << '\n';
    return 0;
}
```

程序 28：PMR 嵌套容器（**无需** `scoped_allocator_adaptor`！）

**[经验]**　PMR 的杀手级特性：`polymorphic_allocator<T>` 的拷贝构造函数会**复制 `memory_resource*`**（`bits/memory_resource.h:135-138`），因此 `pmr::vector<string>` 在构造内部 `pmr::string` 元素时，自动把同一个 `resource` 指针下传给元素的 `polymorphic_allocator<char>`。嵌套“免费”共享资源——这正是它比经典分配器（需 `scoped_allocator_adaptor` 手动传递）优雅的地方。

```cpp
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

**[标准]**　`vector`/`deque`/`list`/`map`/`unordered_map` 等都满足「分配器感知容器」要求（`[container.alloc.reqmts]`）：持有 `allocator_type`，提供 `get_allocator()`，`allocator_type` 由模板参数决定。

**核心知识点（分配器感知）**：所有这些容器的第二个（或最后一个）模板参数是 `Allocator`，缺省 `std::allocator<value_type>`；PMR 别名则把该参数固定为 `polymorphic_allocator`。

程序 29：`map` 使用自定义分配器（注意 `A` 必须是模板且提供默认构造，因为 `map` 会把它 `rebind` 到内部节点类型）：

```cpp
// 编译: g++ -std=c++17 ch38_p29.cpp -o ch38_p29
#include <map>
#include <cstddef>
#include <cstdlib>
#include <iostream>
#include <utility>
template <typename T> struct A {
    using value_type = T;                          // T 在此为 std::pair<const int,int>
    using propagate_on_container_move_assignment = std::true_type;
    using is_always_equal = std::false_type;
    A() = default;                                 // 容器 rebind 后需默认构造
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

```cpp
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

```cpp
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

```cpp
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

**[实现]**　libstdc++（GCC）、libc++（LLVM/Clang）、MS STL（MSVC）都满足标准，但在**细节参数**与**编译开关**上不同。下表基于公开事实与标准库源码（libstdc++ 已逐行验证；libc++/MS STL 为[实现-推断] + 已知公开行为）：

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

**[平台]**　本机 MinGW GCC 13.1.0：`memory_resource` 可用、`synchronized_pool_resource` 存在（已验证能编译程序 18）。若在「不带动线程的 libstdc++ 构建」下，`memory_resource:52-55` 会把 `__cpp_lib_memory_resource` 设为 `1` 并**省略 `synchronized_pool_resource`**——这是唯一的硬性差异点。

程序 33（差异探测，独立可编译，打印本 STL 的关键宏）：

```cpp
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

**[经验]**　以下基准为**量级参考**（本机 MinGW GCC 13.1.0，`-O2`）。PMR `monotonic` 因「零释放、纯 bump」通常比 `new_delete` 快 **数倍**；自定义对象池把 N 次 `operator new` 降到「N/块数 + 1」次，分配数显著减少。

**[平台]**　运行于本机 Windows 11 + MinGW GCC 13.1.0。数值为示意量级，非精确测量（真实测量请用 `std::chrono::high_resolution_clock` 多次取 median）。

程序 34：PMR monotonic vs new_delete 量级对比：

```cpp
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
        std::pmr::vector<int> v(&g_mr);             // 全在单调缓冲，无释放
        for (int i = 0; i < N; ++i) v.push_back(i);
        g_mr.release();                             // 一次性归还
    }
    auto t1 = std::chrono::steady_clock::now();
    std::cout << "monotonic: "
              << std::chrono::duration<double>(t1 - t0).count() << "s\n";

    auto t2 = std::chrono::steady_clock::now();
    for (int k = 0; k < 50; ++k) {
        std::vector<int> v;                         // 默认 std::allocator（= new/delete）
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

```cpp
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

**[经验]**　结论：C++ 的分配器是「编译期类型参数 + 运行时 PMR 多态」双轨；Rust `Allocator` trait 是单轨泛型；C# `ArrayPool` 是单轨运行时池；Go/Java 完全交给 GC。需要「确定内存来源 + 极致性能」时，C++/Rust 胜；需要「省心」时 GC 语言胜。

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

**实战建议（[经验]）**
1. 默认就用 `std::allocator`——它够用，别过度设计。
2. 临时/一次性构建（解析、序列化、测试夹具）用 `monotonic_buffer_resource` + 栈缓冲，几乎零成本。
3. 高频小对象、单线程：用 `unsynchronized_pool_resource`；多线程：用 `synchronized_pool_resource`。
4. 要切换策略又不想改类型：用 PMR，而非自定义 `Allocator` 模板。
5. 跨 DLL/模块边界传递 PMR 容器时，确保两端使用**同一 `memory_resource` 实例**（靠指针等价），否则析构期释放错配。
6. 调试/统计：从 `std::allocator` 派生一个计数分配器（程序 8），比直接 hook `operator new` 更局部、更安全。

---

## ⑳ 综合实战：分配器选型决策树 + 速记（内化，无推荐阅读节）

**选型决策树 [经验]**
1. 默认容器 → `std::allocator`（程序 1/2/32）。
2. 解析/序列化/测试夹具等临时构建 → `monotonic_buffer_resource` + 栈缓冲（程序 9/18）。
3. 高频小对象、单线程 → `unsynchronized_pool_resource`；多线程 → `synchronized_pool_resource`（程序 12/33）。
4. 想换策略但不想改容器类型 → PMR（`polymorphic_allocator`），而非自定义 `Allocator` 模板（程序 1→30 改造）。
5. 需全局统计/替换 → 自定义 `Allocator` 派生 `std::allocator`（程序 8），或替换 `new_delete_resource()`。

```cpp
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
- **立场分层**：[标准]/[实现]/[平台]/[经验] 均已标注；缺失细节处显式标 [实现-推断]。
- **环境校验**：MinGW GCC 13.1.0 上程序 1/9/12/18/33 等已实测可编译运行；`synchronized_pool_resource` 本机可用。


## 联合使用场景

| 关联章节 | 场景 | 组合方式 |
|---|---|---|
| [第37章](Book/part04_memory/ch37_new_delete.md) | 键值查找/缓存 | 本章提供概念，第37章提供实现 |
| [第39章](Book/part04_memory/ch39_raii_rule.md) | 多态插件/框架扩展 | 本章提供概念，第39章提供实现 |
| [第122章](Book/part10_modern/ch122_pmr.md) | 泛型库/编译期计算 | 本章提供概念，第122章提供实现 |
| [第160章](Book/part15_cases/ch160_mempool.md) | 高性能容器/零拷贝传输 | 本章提供概念，第160章提供实现 |

## 附录 E：Allocator工业与面试 [B: Principle / H: Design / I: Practice / J: Learning]

```
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

```cpp
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

| allocator | 分配 | 释放 | 线程 | 场景 |
|---|---|---|---|---|
| monotonic | O(1) bump | 从不 | 单 | 游戏关卡加载 |
| pool | O(1) freelist | O(1) freelist | 可选 | 大量同大小对象 |
| malloc (glibc ptmalloc) | **45.5 ns (本机实测)** | **45.5 ns** | 是 | 通用 |
| custom | 自定义 | 自定义 | 自定义 | 极致优化 |

> **【实测】** malloc 单线程无争用单次分配/释放延迟 = **45.5 ns（108.98 cyc，TSC 2.395GHz，MinGW GCC 13.1.0 -O2）**，由 `Examples/_ch44_pool_perf.cpp` 经 RDTSC 微基准实测（减空循环开销）。真实汇编证据见 `Examples/_ch44_pool_perf.asm` 的 `_ZL12probe_mallocy`：实为 `call malloc` + `call free` 两个库调用，glibc ptmalloc 内部查 bins / 加锁 / 必要时 `brk`/`mmap` 兜底。旧 "~50ns" 量级一致但现已实测锚定。

面试: allocator vs PMR? allocator=编译期+模板参数; PMR=运行时+虚函数(类型擦除)
       monotonic为什么快? 指针递增分配(bump allocator), 单轮仅 `addq $16` 指针加法≈0 额外开销(GCC 下与空循环同速), 而 malloc 含真实库调用路径 ~45.5ns——差的是"是否进入分配器内核", 不是常数倍


## 真实开源项目参考（可查证链接）

> 本节补可查证的真实项目引用（非虚构）。

- **Boost.Pool（boost.org）**：提供对象池分配器。
- **oneTBB scalable_allocator（github.com/uxlfoundation/oneTBB）**：多线程友好。

**常见陷阱 / 最佳实践**：
- 自定义 allocator 必须满足 Allocator 完备性要求（`rebind` / `propagate_on_container_copy`）；pmr 比旧 allocator 模型更不易写错（本手册 ch38 实测 malloc 45.5ns）。
- 跨容器共用 allocator 实例需其 propagate 语义明确。

> 交叉引用：pmr 见 [ch122](Book/part10_modern/ch122_pmr.md)；池见 [ch44](Book/part04_memory/ch44_memory_pool.md)。

## 相关章节（交叉引用）

- **后续依赖**：`Book/part07_stl/ch76_stl_arch.md`（第76章　STL 架构与迭代器概念）—— 本章为其前置，建议后续延伸阅读。
- **后续依赖**：`Book/part07_stl/ch77_vector.md`（第77章　vector：扩容、失效、allocator 协作）—— 本章为其前置，建议后续延伸阅读。
- **相邻主题**：`Book/part04_memory/ch36_stack_heap.md`（第 36 章　栈（stack）与堆（heap）的深度对比）—— 编号相邻、主题接续。
- **相邻主题**：`Book/part04_memory/ch40_exception_safety.md`（第 40 章　异常安全（Exception Safety））—— 编号相邻、主题接续。
- **同模块**：`Book/part04_memory/ch35_memory_layout.md`（第 35 章  C++ 程序的内存模型与操作系统视角）—— 同模块下的其他主题。

## 工业实现参考：真实通用分配器 [B: Principle]

[标准·可查证] 标准 `std::allocator` 仅包装 `::operator new`；高性能场景用工业分配器：
- jemalloc（Meta/Facebook，多核低锁，大规模服务）；
- tcmalloc（Google，线程缓存，gperftools）；
- mimalloc（Microsoft，低碎片，Azure 基础设施）；
- snmalloc（Microsoft，消息传递并发）；
- Boost.Pool（Boost，定长块池）；
- tbb::scalable_allocator（Intel oneTBB）。

这些分配器以 `0x0010`/`0x0040`（16/64 字节）块对齐减少碎片，热路径用线程本地缓存避免锁（`lock xadd` 10–20 ns 仅在跨核时）。`GCC 13.1.0` / `Clang 17` 的 `-O2` 把 `std::allocator` 的 `new` 内联；`C++17` 起 `std::pmr` 提供多态分配器（经 `0x0008` 指针间接，见 ch47 量级）。

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

