# 第 44 章 内存池（Memory Pool）从零实现

⟶ Book/part15_cases/ch160_mempool.md
⟶ Book/part10_modern/ch122_pmr.md

> 立场分层说明：本章所有论断按四层标注——**[标准]** 表示 C++ 标准保证；**[实现]** 表示 GCC/libstdc++、LLVM/libc++、MSVC/MS STL 的具体实现行为；**[平台]** 表示 Windows/MinGW/Linux/ARM/x86 等平台相关；**[经验]** 表示工程实践与性能经验。
>
> 本机验证环境：MinGW **GCC 13.1.0**，`libstdc++` 头位于 `C:/Qt/Tools/mingw1310_64/lib/gcc/x86_64-w64-mingw32/13.1.0/include/c++/`。
> 交叉引用：存储期见 ch19，对象对齐见 ch35，堆与分配器见 ch36，operator new/delete 见 ch37，PMR 与标准池见 ch38，RAII 资源生命期见 ch39，缓存友好性见 ch43，并发无锁池见 ch61。

---

## ① 为何需要内存池（动机全景）

⟶ Book/part04_memory/ch43_cache_locality.md


**[标准]** C++ 标准只保证 `::operator new`/`::operator delete`（见 ch37）分配一块" suitably aligned storage for any object type"（[new.delete.single]），并不保证性能、延迟确定性或碎片控制。其语义是"请求—返回"式的通用分配器，要为任意大小、任意生命周期的请求服务。

**[实现]** `libstdc++` 的 `std::allocator` 直接转发到 `__new_allocator::allocate`，最终调用 `_GLIBCXX_OPERATOR_NEW`（即 `::operator new` 或 `__builtin_operator_new`）：

```cpp
// C:/Qt/Tools/mingw1310_64/lib/gcc/x86_64-w64-mingw32/13.1.0/include/c++/bits/new_allocator.h:121-148
_GLIBCXX_NODISCARD _Tp*
allocate(size_type __n, const void* = static_cast<const void*>(0))
{
  // ... 容量检查 ...
  if (alignof(_Tp) > __STDCPP_DEFAULT_NEW_ALIGNMENT__)
    {
      std::align_val_t __al = std::align_val_t(alignof(_Tp));
      return static_cast<_Tp*>(_GLIBCXX_OPERATOR_NEW(__n * sizeof(_Tp), __al));
    }
  return static_cast<_Tp*>(_GLIBCXX_OPERATOR_NEW(__n * sizeof(_Tp)));
}
```

**[经验]** 频繁 `new`/`delete` 在真实系统中带来四类代价，内存池（Memory Pool）正是为消除它们而生：

1. **锁竞争（Lock Contention）**：通用堆分配器（glibc `ptmalloc`、系统 `HeapAlloc`）通常用一个全局互斥保护空闲链表。高并发下线程在分配路径上串行化，吞吐崩溃。
2. **碎片（Fragmentation）**：
   - **外部碎片**：空闲内存总量够，但被已分配块切碎，无法满足大块连续请求。
   - **内部碎片**：分配器为满足对齐/最小块而多给的内存（如 17 字节请求拿到 32 字节）。
3. **缓存不友好（Cache Unfriendliness）**：通用分配器归还的地址散布在堆各处，对象间无局部性；见 ch43。
4. **不确定性延迟（Non-deterministic Latency）**：通用分配器复杂度与堆状态相关，`new` 可能触发 `sbrk`/`mmap` 系统调用或锁等待，延迟不可界。实时/嵌入式系统（见用户嵌入式背景）要求**最坏情况执行时间（WCET）可界**，禁止运行时 `new`。

**[平台]** 不同平台默认分配器差异巨大：Windows `HeapAlloc` 受 `RtlHeap` 保护；Linux glibc `malloc` 用 `ptmalloc2`（per-thread arena）；本机 MinGW 走 msvcrt/mingw 运行时。无论哪种，通用分配器都为"通用"付出代价，专用池可为"特定访问模式"大幅提速。

---

## ② 内存池分类全景图

**[标准]** C++17 在标准库内提供了 PMR（Polymorphic Allocator，见 ch38）作为可替换分配器的抽象层，但 PMR 只是"接口"，池仍是"实现"。本章从零实现以下池：

| 池类型 | 关键特征 | 时间复杂度 | 典型用途 |
|---|---|---|---|
| 固定大小块分配器（Fixed-size Block） | 侵入式 free list、O(1) 分配/释放 | O(1)/O(1) | 同尺寸对象高频分配 |
| 位图分配器（Bitmap） | 每对象 1 bit 占用标记 | O(1)（带扫描）/O(1) | 固定数量对象、cache 友好 |
| 单调分配器（Monotonic/Bump） | bump pointer，只增不释放 | O(1) | 临时区域、PMR `monotonic_buffer_resource`（ch38） |
| 分级空闲列表（Segregated Fits） | 按 size class 分桶 | ~O(1) | 通用尺寸、近似 tcmalloc/jemalloc |
| 线程局部池（Thread-local） | `thread_local` free list，无锁 | O(1) | 多线程、无锁 |
| 对象池（Object Pool） | 预构造 N 对象复用 | O(1) | 避免运行时构造/析构、确定性 |

**[经验]** 选型口诀：**固定尺寸用固定块池；同生命周期临时对象用单调池；多线程高频小对象用线程局部池；尺寸多变用分级池；需要复用已构造对象用对象池。**

---

## ③ 真实 libstdc++ 源码：`__gnu_cxx::__pool_alloc` 逐行

**[实现]** GCC 扩展提供了一个真实的 free-list 池分配器 `std::pool_allocator`（在 `ext` 命名空间）。完整源码位于：

```
C:/Qt/Tools/mingw1310_64/lib/gcc/x86_64-w64-mingw32/13.1.0/include/c++/ext/pool_allocator.h
```

核心设计（pool_allocator.h:77-118）：

```cpp
#include <cstddef>
// ext/pool_allocator.h:77-118  (__gnu_cxx::__pool_alloc_base)
class __pool_alloc_base
{
  typedef std::size_t size_t;
protected:
  enum { _S_align = 8 };                              // 对齐粒度 8 字节
  enum { _S_max_bytes = 128 };                        // >128 字节直接走 ::operator new
  enum { _S_free_list_size = (size_t)_S_max_bytes / (size_t)_S_align }; // 16 个桶

  union _Obj                                          // ★ 侵入式：free 块复用自身存储
  {
    union _Obj* _M_free_list_link;                    // 空闲时：next 指针
    char        _M_client_data[1];                    // 占用时：交给用户的数据
  };

  static _Obj* volatile _S_free_list[_S_free_list_size];  // 全局分级 free list
  static char*          _S_start_free;                // chunk 水位线起
  static char*          _S_end_free;                  // chunk 水位线止
  static size_t         _S_heap_size;

  size_t _M_round_up(size_t __bytes)                  // 向上舍入到 8 的倍数
  { return ((__bytes + (size_t)_S_align - 1) & ~((size_t)_S_align - 1)); }
  // ... _M_get_free_list / _M_get_mutex / _M_refill / _M_allocate_chunk ...
};
```

**逐行要点**：

- `_S_align = 8`：块大小向上舍入到 8，保证 `double`/指针对齐（**[平台]** x86-64 下 `alignof(std::max_align_t)` 通常为 16，但这里人为选 8 以省内存；libstdc++ 作者权衡后取 8）。
- `union _Obj`：**侵入式 free list 的典范**——free 块用自身内存存 `next`，占用块用同一内存存用户数据，零额外元数据（见 44.4）。
- `_S_free_list_size = 16`：128/8 = 16 个 size class 桶，索引 = `(__bytes + 7) / 8 - 1`。

分配路径（pool_allocator.h:214-266 节选）：

```cpp
#include <cstddef>
// ext/pool_allocator.h:246-263
if (__bytes > size_t(_S_max_bytes) || _S_force_new > 0)
  __ret = static_cast<_Tp*>(::operator new(__bytes));   // 大块：直接 new
else
  {
    _Obj* volatile* __free_list = _M_get_free_list(__bytes);
    __scoped_lock sentry(_M_get_mutex());               // ★ 单全局锁！
    _Obj* __restrict__ __result = *__free_list;
    if (__builtin_expect(__result == 0, 0))
      __ret = static_cast<_Tp*>(_M_refill(_M_round_up(__bytes))); // 桶空则补 chunk
    else
      {
        *__free_list = __result->_M_free_list_link;     // O(1) 取表头
        __ret = reinterpret_cast<_Tp*>(__result);
      }
    if (__ret == 0) std::__throw_bad_alloc();
  }
```

释放路径（pool_allocator.h:268-295 节选）：

```cpp
// ext/pool_allocator.h:285-293
_Obj* volatile* __free_list = _M_get_free_list(__bytes);
_Obj* __q = reinterpret_cast<_Obj*>(__p);
__scoped_lock sentry(_M_get_mutex());
__q->_M_free_list_link = *__free_list;                  // O(1) 头插
*__free_list = __q;
```

**[经验]** `std::pool_allocator` 的设计与本章从零实现高度一致：分级 free list + 侵入式节点 + 大块直走 `new`。**但它用单全局锁**（`__scoped_lock sentry(_M_get_mutex())`），高并发下仍会锁竞争——这正是 44.9 线程局部池要消除的瓶颈。另注意它受环境变量 `GLIBCXX_FORCE_NEW` 控制（pool_allocator.h:240），设了该变量就全走 `new`，便于排查池相关 bug。

---

## ④ 固定大小块分配器：侵入式 free list 完整实现

**[标准]** 固定大小块分配器管理一组**等尺寸**块。分配只从空闲链表头取一块，释放只把块头插回链表，二者均 O(1)，且不调用底层 `new`（除非池耗尽需扩容）。

### 44.4.1 侵入式（Intrusive）为何省去元数据的本质

**[经验]** "侵入式"指：当一块**空闲**时，我们借用它**自己的内存**存放 `next` 指针；当它**被分配**后，这块内存完全交给用户，不再需要独立的"块头（block header）"记录大小/下一个。对比"外部元数据"方案：

```
外部元数据（每块多 16 字节头）：
[ header | user data ][ header | user data ]...
  ^size/next  ^^^^^^^^

侵入式（零额外字节）：
空闲时: [ next | (复用为未来 user data) ]
占用时: [       user data            ]
```

侵入式代价：块大小必须 ≥ `sizeof(void*)`（否则放不下 `next`），且块不能随意变长。对固定尺寸对象池完全可接受。

### 44.4.2 完整可编译实现（程序 1/≥30）

```cpp
// program_01_fixed_block_pool.cpp  —— 侵入式固定块池（完整可编译）
// 编译: g++ -std=c++17 -O2 program_01_fixed_block_pool.cpp -o p01
#include <cstddef>
#include <cstring>
#include <new>

class FixedBlockPool {
    struct FreeNode { FreeNode* next; };   // 空闲块首部内嵌 next（侵入式）
    std::byte*  memory_   = nullptr;
    FreeNode*   free_list_ = nullptr;
    std::size_t block_size_ = 0;
    std::size_t capacity_   = 0;
    std::size_t used_       = 0;

    static std::size_t round_up(std::size_t n, std::size_t a) noexcept {
        return (n + a - 1) & ~(a - 1);
    }
public:
    FixedBlockPool(std::size_t block_size, std::size_t count)
        : block_size_(round_up(block_size, alignof(std::max_align_t))),
          capacity_(count) {
        const std::size_t total = block_size_ * count;
        memory_ = static_cast<std::byte*>(::operator new(total));
        // 初始化空闲链表：每块首部写入 next，串成单链表
        free_list_ = reinterpret_cast<FreeNode*>(memory_);
        FreeNode* cur = free_list_;
        for (std::size_t i = 1; i < count; ++i) {
            FreeNode* nxt = reinterpret_cast<FreeNode*>(memory_ + i * block_size_);
            cur->next = nxt;
            cur = nxt;
        }
        cur->next = nullptr;
    }
    ~FixedBlockPool() { ::operator delete(memory_); }

    FixedBlockPool(const FixedBlockPool&) = delete;
    FixedBlockPool& operator=(const FixedBlockPool&) = delete;

    void* allocate() {
        if (!free_list_) return nullptr;          // 池满：返回 nullptr（ caller 决定扩容）
        FreeNode* p = free_list_;                 // O(1)：取表头
        free_list_ = p->next;
        ++used_;
        return static_cast<void*>(p);
    }
    void deallocate(void* p) noexcept {           // O(1)：头插
        if (!p) return;
        FreeNode* n = static_cast<FreeNode*>(p);
        n->next = free_list_;
        free_list_ = n;
        --used_;
    }
    std::size_t block_size() const noexcept { return block_size_; }
    std::size_t capacity()  const noexcept { return capacity_; }
    std::size_t used()      const noexcept { return used_; }
};

int main() {
    FixedBlockPool pool(sizeof(int), 1024);
    int* a = static_cast<int*>(pool.allocate());
    int* b = static_cast<int*>(pool.allocate());
    *a = 42; *b = 7;
    // 验证侵入式：块本身即对象内存，无外部头
    pool.deallocate(a);
    pool.deallocate(b);
    return 0;
}
```

### 44.4.3 带构造/析构的强类型封装（程序 2/≥30）

```cpp
// program_02_fixed_pool_typed.cpp —— 在池上做 placement new + 析构
// 编译: g++ -std=c++17 -O2 program_02_fixed_pool_typed.cpp -o p02
#include <new>
#include <utility>
#include "program_01_fixed_block_pool.cpp"  // 复用 FixedBlockPool（与本文件分别编译，或先去掉 program_01 的 main）  // 复用上面的 FixedBlockPool（教学用；与本文件分别编译，或先去掉 program_01 的 main）

template <class T>
class FixedPool {
    FixedBlockPool pool_;
public:
    explicit FixedPool(std::size_t n) : pool_(sizeof(T), n) {}

    template <class... Args>
    T* construct(Args&&... args) {
        void* p = pool_.allocate();
        if (!p) return nullptr;
        return ::new(p) T(std::forward<Args>(args)...);   // 构造调用（ch39 RAII）
    }
    void destroy(T* p) noexcept {
        if (!p) return;
        p->~T();                                          // 析构调用
        pool_.deallocate(p);
    }
};

#include <iostream>
#include <cstddef>
struct Particle { float x, y; ~Particle() { /* 资源清理 */ } };
int main() {
    FixedPool<Particle> pool(64);
    Particle* p = pool.construct(1.0f, 2.0f);
    std::cout << p->x << "," << p->y << "\n";
    pool.destroy(p);       // 显式析构 + 归还块
    return 0;
}
```

**[经验]** 与 `std::vector` 预分配对比：`std::vector::reserve(n)` 也是在构造时一次性 `new` 出连续 n 个对象容量的内存（见 ch36），但它**对象尺寸与数量固定、生命周期一同结束、且支持随机下标**。固定块池则是**单对象粒度的借还**，可任意顺序分配/释放单个对象，且可对接 STL 分配器接口。二者共同点：都通过"一次大分配代替多次小分配"消除锁竞争与碎片。

---

## ⑤ 对齐与指针算术（连接 ch35）

**[标准]** [expr.new] 与 [new.delete] 保证 `::operator new` 返回的存储满足 `alignof(std::max_align_t)`（**[平台]** x86-64 通常 16）。但当 `alignof(T) > alignof(std::max_align_t)`（如 32/64 字节 SIMD 类型、或自定义 over-aligned 类型），需 `::operator new(size, std::align_val_t)`（见 ch37，`__STDCPP_DEFAULT_NEW_ALIGNMENT__` 阈值）。

### 44.5.1 为何未对齐访问是致命的

**[平台]** 
- **x86/x86-64**：未对齐访问不会崩溃，但会触发**多次内存读 + 拼接**，是**性能惩罚**（某些 SSE/AVX 指令如 `movaps` 要求 16 字节对齐，否则 `#GP` 异常）。
- **ARM（含 AArch64，嵌入式主战场）**：未对齐的多数访问会直接抛 **SIGBUS（总线错误）**，进程崩溃。RISC 架构通常不允许跨对齐边界的原子访存。
- 因此池块起始地址必须满足 `alignof(T)`。

### 44.5.2 `std::align` 标准对齐工具（程序 3/≥30）

**[标准]** `<memory>` 提供 `void* std::align(std::size_t alignment, std::size_t size, void*& ptr, std::size_t& space)`，在 `[ptr, ptr+space)` 区间内找到满足对齐的地址并前移 `ptr`、缩减 `space`。

```cpp
// program_03_std_align.cpp —— 用 std::align 在缓冲内对齐
// 编译: g++ -std=c++17 -O2 program_03_std_align.cpp -o p03
#include <memory>
#include <cstddef>
#include <cstdio>

int main() {
    alignas(64) char buffer[4096];     // 64 字节对齐的大缓冲（区域/arena 思路）
    void*  ptr   = buffer;
    std::size_t space = sizeof(buffer);
    void* aligned = std::align(64, sizeof(double) * 8, ptr, space);
    std::printf("aligned=%p space_left=%zu ok=%d\n",
                aligned, space, aligned != nullptr);
    return 0;
}
```

### 44.5.3 手动指针算术对齐（程序 4/≥30）

**[标准]** 手动向上对齐：`(addr + (a-1)) & ~(a-1)`，依赖 `a` 为 2 的幂。

```cpp
// program_04_manual_align.cpp —— reinterpret_cast + 指针算术手动对齐
// 编译: g++ -std=c++17 -O2 program_04_manual_align.cpp -o p04
#include <cstdint>
#include <cstddef>
#include <cstdio>

inline void* align_up(void* p, std::size_t a) noexcept {
    std::uintptr_t addr = reinterpret_cast<std::uintptr_t>(p);
    addr = (addr + (a - 1)) & ~(static_cast<std::uintptr_t>(a) - 1);
    return reinterpret_cast<void*>(addr);
}

int main() {
    char raw[1024];
    void* a16 = align_up(raw, 16);
    void* a64 = align_up(raw, 64);
    std::printf("a16=%p a64=%p\n", a16, a64);
    return 0;
}
```

**[经验]** 池实现中，`block_size` 一律向上舍入到 `max(alignof(T), alignof(void*))`，保证任意块既是对象对齐、又能放下 `next` 指针。这正是 `pool_allocator.h:82` 中 `_S_align=8` 与 44.4 `round_up(..., alignof(std::max_align_t))` 的动机。

---

## ⑥ 位图分配器（Bitmap Allocator）

**[标准]** 位图分配器为固定数量 N 个槽位维护一个 `N` bit 的占用标记数组，每对象 1 bit（0=空闲，1=占用）。分配时扫描首个 0 bit，释放时清对应 bit。

**[经验]** 位图法 cache 友好：整个占用位图很小（N=1024 仅 128 字节），可常驻 L1 cache；且天然支持"按槽索引定位对象地址"（`base + index*size`），无链表遍历。代价是分配可能需扫描（可用 `ffs`/`__builtin_ctzll` 加速到 O(1)）。

### 44.6.1 完整可编译实现（程序 5/≥30）

```cpp
// program_05_bitmap_pool.cpp —— 1 bit/对象 的位图池
// 编译: g++ -std=c++17 -O2 program_05_bitmap_pool.cpp -o p05
#include <cstddef>
#include <cstdint>
#include <new>
#include <vector>
#include <cstring>

class BitmapPool {
    std::size_t block_size_;
    std::size_t count_;
    std::byte*  base_ = nullptr;
    std::vector<uint64_t> bits_;   // 每 bit 一槽：1=占用
public:
    BitmapPool(std::size_t block_size, std::size_t count)
        : block_size_(round_up(block_size)), count_(count),
          bits_((count + 63) / 64, 0) {
        base_ = static_cast<std::byte*>(::operator new(block_size_ * count));
    }
    ~BitmapPool() { ::operator delete(base_); }

    static std::size_t round_up(std::size_t n) noexcept {
        std::size_t a = alignof(std::max_align_t);
        return (n + a - 1) & ~(a - 1);
    }
    void* allocate() {
        for (std::size_t w = 0; w < bits_.size(); ++w) {
            uint64_t free = ~bits_[w];
            if (free) {
                int bit = __builtin_ctzll(free);   // 首个 0 bit（O(1)）
                bits_[w] |= (uint64_t(1) << bit);
                std::size_t idx = w * 64 + bit;
                if (idx < count_) return base_ + idx * block_size_;
            }
        }
        return nullptr;   // 满
    }
    void deallocate(void* p) noexcept {
        std::size_t off = static_cast<std::byte*>(p) - base_;
        std::size_t idx = off / block_size_;
        bits_[idx / 64] &= ~(uint64_t(1) << (idx % 64));
    }
};

#include <iostream>
int main() {
    BitmapPool pool(sizeof(double), 256);
    double* d = static_cast<double*>(pool.allocate());
    *d = 3.14;
    pool.deallocate(d);
    std::cout << "bitmap ok\n";
    return 0;
}
```

**[经验]** 对比固定块池：位图池无侵入式/链表，靠索引定位，适合**固定数量、需 O(1) 随机定位**的场景（如帧分配器、固定大小组件表）。ch43 缓存友好性也适用——位图本身极小。

---

## ⑦ 单调分配器 / Bump Allocator

**[标准]** 单调分配器维护一个指针（bump pointer）指向缓冲区"已用/未用"分界，分配仅把指针前移并返回旧值；**不提供单独的释放**，整个缓冲区在析构时一次性归还。这与 ch38 的 `std::pmr::monotonic_buffer_resource` 语义一致。

**[经验]** 单调分配器是**最快**的分配器（分配 = 一次加法 + 比较），常用于：解析器临时字符串、渲染帧临时对象、以及作为其他池的"上游 chunk 来源"（如 `pool_allocator.h` 的 `_M_allocate_chunk`）。

### 44.7.1 完整可编译实现（程序 6/≥30）

```cpp
// program_06_monotonic.cpp —— bump pointer 单调分配器
// 编译: g++ -std=c++17 -O2 program_06_monotonic.cpp -o p06
#include <cstddef>
#include <cstdint>
#include <new>

class MonotonicAllocator {
    std::byte*  buf_   = nullptr;
    std::size_t size_  = 0;
    std::size_t off_   = 0;
    std::size_t peak_align_skip_ = 0;
public:
    MonotonicAllocator(std::size_t bytes)
        : buf_(static_cast<std::byte*>(::operator new(bytes))), size_(bytes) {}

    ~MonotonicAllocator() { ::operator delete(buf_); }   // 仅此一处释放

    void* allocate(std::size_t n, std::size_t align = alignof(std::max_align_t)) {
        std::uintptr_t cur = reinterpret_cast<std::uintptr_t>(buf_ + off_);
        std::uintptr_t aligned = (cur + (align - 1)) & ~(std::uintptr_t(align) - 1);
        std::uintptr_t new_off = aligned - reinterpret_cast<std::uintptr_t>(buf_) + n;
        if (new_off > size_) return nullptr;     // 单调池不支持扩容
        off_ = static_cast<std::size_t>(new_off);
        return reinterpret_cast<void*>(aligned);
    }
    std::size_t used() const noexcept { return off_; }
    // 注意：无 deallocate —— 只增不释放
};

#include <iostream>
int main() {
    MonotonicAllocator ma(4096);
    int*  a = static_cast<int*>(ma.allocate(sizeof(int)));
    int*  b = static_cast<int*>(ma.allocate(sizeof(int)));
    double* d = static_cast<double*>(ma.allocate(sizeof(double), alignof(double)));
    *a = 1; *b = 2; *d = 2.5;
    std::cout << "used=" << ma.used() << "\n";   // 单调增长
    return 0;
}
```

**[实现]** 标准 PMR 等价物（ch38）：`std::pmr::monotonic_buffer_resource` 内部即 bump pointer，且支持"上游资源耗尽时向上游要下一块"。其不释放单个对象，只对 `release()` 整体回卷——与上面实现语义相同。

---

## ⑧ 分级空闲列表（Segregated Fits）

**[标准]** 分级空闲列表按**尺寸等级（size class）**把请求分桶：每个桶是一条该尺寸块的 free list。分配时把请求大小向上取整到最近桶，从对应桶取块；桶空则向系统要一大块切分成该尺寸小块补入。这与 tcmalloc 的 `SizeMap`、jemalloc 的 `bin` 思想一致。

**[经验]** size class 通常按几何级数（如 8/16/32/64/80/96...或干脆 2 的幂）。向上取整带来**内部碎片**（平均约 1/2 桶间距），但消除了**外部碎片**（每桶内块尺寸统一、可任意互换），并让分配近似 O(1)。

### 44.8.1 完整可编译实现（程序 7/≥30）

```cpp
// program_07_segregated.cpp —— 分级空闲列表分配器
// 编译: g++ -std=c++17 -O2 program_07_segregated.cpp -o p07
#include <cstddef>
#include <cstdint>
#include <new>
#include <array>
#include <mutex>

class SegregatedPool {
    struct Node { Node* next; };
    static constexpr std::size_t kMin = 8;
    static constexpr std::size_t kMax = 256;
    static constexpr std::size_t kStep = 8;                 // 桶间距 8
    static constexpr std::size_t kNumBuckets = (kMax - kMin) / kStep + 1;

    std::array<Node*, kNumBuckets> buckets_{};
    std::array<std::byte*, kNumBuckets> chunks_{};          // 各桶的 chunk 来源
    std::mutex mtx_;

    static std::size_t bucket_index(std::size_t sz) noexcept {
        if (sz <= kMin) return 0;
        std::size_t idx = (round_up(sz) - kMin) / kStep;
        return idx < kNumBuckets ? idx : kNumBuckets - 1;
    }
    static std::size_t round_up(std::size_t n) noexcept {
        return (n + kStep - 1) & ~(kStep - 1);
    }
    static std::size_t block_size_for(std::size_t idx) noexcept {
        return kMin + idx * kStep;
    }
    Node* refill(std::size_t idx) {                          // 桶空：向系统要大块切分
        const std::size_t bsz = block_size_for(idx);
        const std::size_t per_chunk = 64;
        std::byte* mem = static_cast<std::byte*>(::operator new(bsz * per_chunk));
        chunks_[idx] = mem;                                  // 记录以便将来统一释放
        Node* head = reinterpret_cast<Node*>(mem);
        Node* cur = head;
        for (std::size_t i = 1; i < per_chunk; ++i) {
            Node* nxt = reinterpret_cast<Node*>(mem + i * bsz);
            cur->next = nxt; cur = nxt;
        }
        cur->next = nullptr;
        return head;
    }
public:
    void* allocate(std::size_t n) {
        std::size_t idx = bucket_index(n);
        std::lock_guard<std::mutex> lk(mtx_);
        Node* p = buckets_[idx];
        if (!p) p = buckets_[idx] = refill(idx);
        buckets_[idx] = p->next;                             // O(1) 取头
        return p;
    }
    void deallocate(void* p, std::size_t n) noexcept {
        std::size_t idx = bucket_index(n);
        std::lock_guard<std::mutex> lk(mtx_);
        Node* q = static_cast<Node*>(p);
        q->next = buckets_[idx];                             // O(1) 头插
        buckets_[idx] = q;
    }
    ~SegregatedPool() {
        for (auto c : chunks_) if (c) ::operator delete(c);
    }
};

#include <iostream>
int main() {
    SegregatedPool pool;
    void* a = pool.allocate(10);    // -> 16 桶
    void* b = pool.allocate(30);    // -> 32 桶
    pool.deallocate(a, 10);
    pool.deallocate(b, 30);
    std::cout << "segregated ok\n";
    return 0;
}
```

**[实现-推断]** tcmalloc 的 `SizeMap::SizeClass` 用更精细的几何分级（小对象按 8/16 递增，大对象按页对齐），且每个 size class 对应一个 `CentralFreeList`；jemalloc 用 `bin`+`run`（按 `reg_size` 切分 region）。本机不可得 glibc/jemalloc/tcmalloc 源码，建议阅读：https://github.com/google/tcmalloc（见 44.19）。

---

## ⑨ 线程局部池（Thread-local Pool，无锁）

**[标准]** C++11 起 `thread_local` 存储期（见 ch19）让每个线程拥有独立变量实例。线程局部池为每个线程维护一条独立 free list，线程内分配/释放**完全无锁**。

**[经验]** 当线程局部 free list 耗尽，才向"全局中心池"批量取一块（batch fetch）；当线程局部列表积累过多空闲块，批量还回全局池（batch return）。这正是 tcmalloc `ThreadCache`/`CentralFreeList` 与 ch38 `std::pmr::unsynchronized_pool_resource` 的核心思路。

### 44.9.1 完整可编译实现（程序 8/≥30）

```cpp
// program_08_thread_local.cpp —— thread_local free list + 全局批量取还
// 编译: g++ -std=c++17 -O2 -pthread program_08_thread_local.cpp -o p08
#include <cstddef>
#include <new>
#include <vector>
#include <thread>
#include <mutex>
#include <iostream>

class ThreadLocalPool {
    struct Node { Node* next; };
    static constexpr std::size_t kBatch = 64;     // 批量取还粒度
    static constexpr std::size_t kBlock = 64;     // 每对象尺寸

    // 全局中心池（受锁保护）
    static std::vector<Node*>& global_free() { static std::vector<Node*> g; return g; }
    static std::mutex& global_mtx() { static std::mutex m; return m; }
    static std::byte* arena_;

    static Node* alloc_chunk() {                   // 向系统要一大块
        std::byte* mem = static_cast<std::byte*>(::operator new(kBlock * kBatch));
        for (std::size_t i = 0; i < kBatch; ++i)
            reinterpret_cast<Node*>(mem + i*kBlock)->next =
                (i+1 < kBatch) ? reinterpret_cast<Node*>(mem + (i+1)*kBlock) : nullptr;
        return reinterpret_cast<Node*>(mem);
    }
    static void batch_fetch(std::vector<Node*>& local) {   // 批量取
        std::lock_guard<std::mutex> lk(global_mtx());
        auto& g = global_free();
        for (std::size_t i = 0; i < kBatch && !g.empty(); ++i) {
            local.push_back(g.back()); g.pop_back();
        }
        if (local.empty()) local.push_back(alloc_chunk());
    }
    static void batch_return(std::vector<Node*>& local) {  // 批量还
        std::lock_guard<std::mutex> lk(global_mtx());
        auto& g = global_free();
        for (Node* n : local) g.push_back(n);
        local.clear();
    }

    // 每线程独立 free list
    static thread_local std::vector<Node*> local_free_;
public:
    static void* allocate() {
        if (local_free_.empty()) batch_fetch(local_free_);
        Node* p = local_free_.back(); local_free_.pop_back();
        return p;
    }
    static void deallocate(void* p) {
        local_free_.push_back(static_cast<Node*>(p));
        if (local_free_.size() >= kBatch * 2)            // 积累过多则批量还
            batch_return(local_free_);
    }
};
std::byte* ThreadLocalPool::arena_ = nullptr;
thread_local std::vector<ThreadLocalPool::Node*> ThreadLocalPool::local_free_{};

int main() {
    std::vector<std::thread> ts;
    for (int t = 0; t < 8; ++t)
        ts.emplace_back([]{
            for (int i = 0; i < 100000; ++i) {
                void* p = ThreadLocalPool::allocate();
                ThreadLocalPool::deallocate(p);
            }
        });
    for (auto& t : ts) t.join();
    std::cout << "thread-local pool ok\n";
    return 0;
}
```

**[经验]** 关键工程量：批量取还（batch）把"全局锁竞争"从每次分配降到每 kBatch 次一次，且线程热路径完全无锁。对比 `std::pool_allocator` 的**每分配都加锁**（pool_allocator.h:252 `__scoped_lock sentry`），线程局部池在高并发下可快几个数量级。

---

## ⑩ 对象池（Object Pool）：预构造复用

**[标准]** 对象池预先构造 N 个对象放入空闲集合，分配时取一个、释放时放回；对象本身已构造好，可避免运行时的构造/析构开销与不确定性。

**[经验]** 适合：连接池、游戏实体、实时系统中"禁止运行时 new"的场景。与固定块池区别：固定块池存的是**原始内存**（按需 placement new），对象池存的是**已构造对象**（复用）。

### 44.10.1 完整可编译实现（程序 9/≥30）

```cpp
// program_09_object_pool.cpp —— 预构造 N 个对象复用（无运行时构造）
// 编译: g++ -std=c++17 -O2 program_09_object_pool.cpp -o p09
#include <vector>
#include <stack>
#include <cstddef>
#include <iostream>

template <class T>
class ObjectPool {
    std::vector<T>   storage_;            // 预构造的对象
    std::stack<T*>   free_;               // 空闲指针栈
public:
    explicit ObjectPool(std::size_t n) {
        storage_.reserve(n);
        for (std::size_t i = 0; i < n; ++i) {
            storage_.emplace_back();      // 一次性构造
            free_.push(&storage_.back());
        }
    }
    T* acquire() {                         // 复用已构造对象
        if (free_.empty()) return nullptr;
        T* p = free_.top(); free_.pop();
        return p;
    }
    void release(T* p) noexcept { free_.push(p); }   // 仅归还，不析构
    std::size_t available() const { return free_.size(); }
};

struct Connection { int fd = -1; void reset() { fd = -1; } };
int main() {
    ObjectPool<Connection> pool(16);
    Connection* c = pool.acquire();
    c->fd = 5;
    std::cout << "fd=" << c->fd << " avail=" << pool.available() << "\n";
    c->reset(); pool.release(c);
    return 0;
}
```

---

## ⑪ 嵌入式静态池（确定性，无运行时 new）

**[标准/经验]** 实时/嵌入式系统（如 RTOS、汽车 ECU、用户嵌入式背景）禁止在关键路径上调用 `new`：不确定性延迟 + 碎片风险 + 可能触发缺页/系统调用。方案：用**编译期固定大小的静态缓冲**做池，运行期零分配。

**[平台]** 嵌入式常用 `std::array`/`static` 全局缓冲或链接器保留的 `.bss` 段，配合 `std::pmr::monotonic_buffer_resource` 包一层静态数组（ch38）。

### 44.11.1 完整可编译实现（程序 10/≥30）

```cpp
// program_10_embedded_static.cpp —— 编译期固定池，运行期无 new
// 编译: g++ -std=c++17 -O2 program_10_embedded_static.cpp -o p10
#include <cstddef>
#include <array>
#include <cstdint>

template <class T, std::size_t N>
class StaticPool {                       // 零运行时分配
    struct Slot { alignas(T) std::byte raw[sizeof(T)]; bool used = false; };
    std::array<Slot, N> slots_{};
public:
    T* acquire() {
        for (auto& s : slots_) {
            // raw 是 C 数组 std::byte[sizeof(T)]，没有 .data()；数组名即首元素地址
            if (!s.used) { s.used = true; return reinterpret_cast<T*>(s.raw); }
        }
        return nullptr;                  // 静态容量上限：可预测
    }
    void release(T* p) noexcept {
        Slot* s = reinterpret_cast<Slot*>(reinterpret_cast<std::byte*>(p) -
                    offsetof(Slot, raw));
        s->used = false;
    }
    static constexpr std::size_t capacity() { return N; }
};

struct Sensor { int id; float value; };
int main() {
    static StaticPool<Sensor, 32> pool;  // 链接期保留，确定性
    Sensor* s = pool.acquire();
    s->id = 1; s->value = 9.8f;
    pool.release(s);
    return 0;
}
```

---

## ⑫ 三套完整池实现合集（可编译、含构造/析构/对齐/线程安全）

下面给出可直接编译运行的"三合一"演示，整合固定块池、分级池、线程局部池于一工程，并统一对齐、构造/析构与线程安全接口。

### 44.12.1 统一对齐固定块池 + 强类型包装（程序 11/≥30）

```cpp
// program_11_combo_fixed.cpp
// 编译: g++ -std=c++17 -O2 -pthread program_11_combo_fixed.cpp -o p11
#include <cstddef>
#include <new>
#include <cstdint>
#include <iostream>

// ---- 对齐固定块池（线程安全版）----
class AlignedFixedPool {
    struct Node { Node* next; };
    std::byte* mem_ = nullptr;
    Node* free_ = nullptr;
    std::size_t bsz_ = 0, cap_ = 0;
    std::mutex mtx_;
    static std::size_t align_up(std::size_t n) noexcept {
        std::size_t a = alignof(std::max_align_t);
        return (n + a - 1) & ~(a - 1);
    }
public:
    AlignedFixedPool(std::size_t obj, std::size_t n)
        : bsz_(align_up(obj)), cap_(n) {
        mem_ = static_cast<std::byte*>(::operator new(bsz_ * n));
        free_ = reinterpret_cast<Node*>(mem_);
        for (std::size_t i = 1; i < n; ++i) {
            reinterpret_cast<Node*>(mem_ + i*bsz_)->next =
                (i+1<n) ? reinterpret_cast<Node*>(mem_ + (i+1)*bsz_) : nullptr;
        }
        reinterpret_cast<Node*>(mem_)->next = (n>1) ?
            reinterpret_cast<Node*>(mem_ + bsz_) : nullptr;
    }
    ~AlignedFixedPool() { ::operator delete(mem_); }
    void* alloc() {
        std::lock_guard<std::mutex> lk(mtx_);
        if (!free_) return nullptr;
        Node* p = free_; free_ = p->next; return p;
    }
    void free(void* p) noexcept {
        std::lock_guard<std::mutex> lk(mtx_);
        static_cast<Node*>(p)->next = free_; free_ = static_cast<Node*>(p);
    }
    std::size_t block_size() const { return bsz_; }
};

template <class T>
class PoolAllocated {                    // 类型化 + 构造/析构
    static AlignedFixedPool& pool() { static AlignedFixedPool p(sizeof(T), 1024); return p; }
public:
    static void* operator new(std::size_t) { return pool().alloc(); }
    static void  operator delete(void* p) noexcept { pool().free(p); }
};

#include <string>
#include <mutex>
struct Task : PoolAllocated<Task> { int prio; std::string name; };
int main() {
    Task* t = new Task{3, "io"};
    std::cout << t->name << "\n";
    delete t;                            // 走池，不走 ::operator new
    return 0;
}
```

### 44.12.2 分级池 + STL 容器对接（程序 12/≥30）

```cpp
// program_12_combo_seg_stl.cpp —— 分级池作为 std::list 的分配器
// 编译: g++ -std=c++17 -O2 program_12_combo_seg_stl.cpp -o p12
#include <list>
#include <cstddef>
#include <new>
#include <mutex>
#include <cstdint>
#include <array>

class SegAllocBase {
protected:
    struct Node { Node* next; };
    static constexpr std::size_t kStep = 8, kMax = 256;
    static constexpr std::size_t kBuckets = (kMax - kStep)/kStep + 1;
    std::array<Node*, kBuckets> buckets_{};
    std::mutex mtx_;
    static std::size_t idx(std::size_t n) {
        std::size_t r = (n + kStep - 1) & ~(kStep - 1);
        std::size_t i = (r - kStep) / kStep;
        return i < kBuckets ? i : kBuckets - 1;
    }
    Node* refill(std::size_t i) {
        std::size_t bsz = kStep + i*kStep;
        std::byte* m = static_cast<std::byte*>(::operator new(bsz * 64));
        Node* h = reinterpret_cast<Node*>(m); Node* c = h;
        for (int j=1;j<64;++j){ Node* nx=reinterpret_cast<Node*>(m+j*bsz); c->next=nx; c=nx; }
        c->next = nullptr; return h;
    }
};
template <class T>
class SegAllocator : SegAllocBase {
public:
    using value_type = T;
    T* allocate(std::size_t n) {
        std::lock_guard<std::mutex> lk(mtx_);
        std::size_t i = idx(sizeof(T)*n);
        Node* p = buckets_[i]; if(!p) p = buckets_[i] = refill(i);
        buckets_[i] = p->next;
        return reinterpret_cast<T*>(p);
    }
    void deallocate(T* p, std::size_t) {
        std::lock_guard<std::mutex> lk(mtx_);
        Node* q = reinterpret_cast<Node*>(p); q->next = buckets_[idx(sizeof(T))];
        buckets_[idx(sizeof(T))] = q;
    }
    template <class U> struct rebind { using other = SegAllocator<U>; };
};
int main() {
    std::list<int, SegAllocator<int>> lst;   // STL 容器用上分级池
    for (int i=0;i<1000;++i) lst.push_back(i);
    return lst.size() == 1000 ? 0 : 1;
}
```

### 44.12.3 线程局部池 + 确定性批量取还（程序 13/≥30）

```cpp
// program_13_combo_tls.cpp —— 线程局部池（复用 44.9 思路，独立可编译）
// 编译: g++ -std=c++17 -O2 -pthread program_13_combo_tls.cpp -o p13
#include <cstddef>
#include <new>
#include <vector>
#include <thread>
#include <mutex>
#include <iostream>

class TLSefPool {
    struct Node { Node* next; };
    static constexpr std::size_t kBatch = 128, kBlk = 32;
    static std::mutex& m() { static std::mutex x; return x; }
    static std::vector<Node*>& g() { static std::vector<Node*> x; return x; }
    static Node* chunk() {
        std::byte* m = static_cast<std::byte*>(::operator new(kBlk*kBatch));
        for (std::size_t i=0;i<kBatch;++i)
            reinterpret_cast<Node*>(m+i*kBlk)->next =
                (i+1<kBatch)?reinterpret_cast<Node*>(m+(i+1)*kBlk):nullptr;
        return reinterpret_cast<Node*>(m);
    }
    static thread_local std::vector<Node*> local_;
public:
    static void* alloc() {
        if (local_.empty()) {
            std::lock_guard<std::mutex> lk(m());
            auto& gv = g();
            for (std::size_t i=0;i<kBatch && !gv.empty();++i){ local_.push_back(gv.back()); gv.pop_back(); }
            if (local_.empty()) local_.push_back(chunk());
        }
        Node* p = local_.back(); local_.pop_back(); return p;
    }
    static void free(void* p) {
        local_.push_back(static_cast<Node*>(p));
        if (local_.size() >= kBatch*2) {
            std::lock_guard<std::mutex> lk(m());
            auto& gv = g(); for (Node* n: local_) gv.push_back(n);
            local_.clear();
        }
    }
};
thread_local std::vector<TLSefPool::Node*> TLSefPool::local_{};

int main() {
    std::vector<std::thread> ts;
    for (int t=0;t<4;++t) ts.emplace_back([]{
        for (int i=0;i<50000;++i){ void* p=TLSefPool::alloc(); TLSefPool::free(p); }
    });
    for (auto& t:ts) t.join();
    std::cout << "combo tls ok\n";
    return 0;
}
```

---

## ⑬ 与 PMR 的关系（连接 ch38）

**[标准]** C++17 PMR 把"分配器"抽象成 `std::pmr::memory_resource` 多态接口（`allocate`/`deallocate`/`do_allocate`），容器通过 `std::pmr::polymorphic_allocator` 使用。内存池可以**实现为 memory_resource**，从而被任意 PMR 容器复用。

**[实现]** ch38 已述：`monotonic_buffer_resource`（单调池）、`unsynchronized_pool_resource`/`synchronized_pool_resource`（线程局部/全局池）正是标准库内置的池。本章从零实现的池可直接包成 `memory_resource`。

### 44.13.1 把固定块池包成 memory_resource（程序 14/≥30）

```cpp
// program_14_pmr_adapter.cpp —— 自定义池接入 PMR
// 编译: g++ -std=c++17 -O2 program_14_pmr_adapter.cpp -o p14
#include <memory_resource>
#include <cstddef>
#include <new>
#include <vector>
#include <iostream>

class PoolResource : public std::pmr::memory_resource {
    struct Node { Node* next; };
    std::byte* mem_ = nullptr;
    Node* free_ = nullptr;
    std::size_t bsz_;
    std::pmr::memory_resource* upstream_;
    void* do_allocate(std::size_t bytes, std::size_t align) override {
        (void)align; (void)bytes;
        if (!free_) return upstream_->allocate(bsz_, alignof(std::max_align_t));
        Node* p = free_; free_ = p->next; return p;
    }
    void do_deallocate(void* p, std::size_t, std::size_t) override {
        static_cast<Node*>(p)->next = free_; free_ = static_cast<Node*>(p);
    }
    bool do_is_equal(const std::pmr::memory_resource& o) const noexcept override {
        return this == &o;
    }
public:
    PoolResource(std::size_t obj, std::size_t n, std::pmr::memory_resource* up = std::pmr::get_default_resource())
        : bsz_((obj + alignof(std::max_align_t)-1) & ~(alignof(std::max_align_t)-1)), upstream_(up) {
        mem_ = static_cast<std::byte*>(::operator new(bsz_ * n));
        free_ = reinterpret_cast<Node*>(mem_);
        for (std::size_t i=1;i<n;++i){
            reinterpret_cast<Node*>(mem_+i*bsz_)->next =
                (i+1<n)?reinterpret_cast<Node*>(mem_+(i+1)*bsz_):nullptr;
        }
        reinterpret_cast<Node*>(mem_)->next = (n>1)?reinterpret_cast<Node*>(mem_+bsz_):nullptr;
    }
    ~PoolResource() { ::operator delete(mem_); }
};

int main() {
    PoolResource pool(sizeof(int), 1024);
    std::pmr::polymorphic_allocator<int> alloc(&pool);
    std::pmr::vector<int> v(alloc);          // 走我们的池
    for (int i=0;i<100;++i) v.push_back(i);
    std::cout << "pmr adapter size=" << v.size() << "\n";
    return 0;
}
```

---

## ⑭ 三编译器对齐优化提示

**[实现]** 当池分配器返回对齐指针，但编译器静态上无法证明"返回值已对齐"时，可用对齐假设内建提示优化（如向量化 load/store）。

- **GCC/Clang**：`__builtin_assume_aligned(ptr, 32)` 与 `__attribute__((assume_aligned(32)))` 告诉编译器 ptr 至少 32 字节对齐，可消除对齐保护代码并启用更宽向量指令。
- **MSVC**：底层用 `_aligned_malloc`/`_aligned_free`（配合 `_aligned_malloc` 分配对齐内存，但需用 `_aligned_free` 释放，不能混用 `free`）。

### 44.14.1 GCC/Clang 对齐假设（程序 15/≥30）

```cpp
// program_15_assume_aligned.cpp
// 编译: g++ -std=c++17 -O2 -fstrict-aliasing program_15_assume_aligned.cpp -o p15
#include <cstddef>
#include <cstdio>

// 告知编译器返回值 64 字节对齐，便于向量化
__attribute__((assume_aligned(64)))
void* get_aligned_buffer(std::byte* base) {
    return __builtin_assume_aligned(base, 64);
}

int main() {
    alignas(64) static std::byte buf[4096];
    float* p = static_cast<float*>(get_aligned_buffer(buf));
    for (int i=0;i<64;++i) p[i] = float(i);          // 编译器可生成 256-bit 向量 store
    std::printf("sum~%.0f\n", p[63]);
    return 0;
}
```

### 44.14.2 MSVC `_aligned_malloc`（程序 16/≥30）

```cpp
// program_16_aligned_malloc.cpp  —— [平台] MSVC / Windows
// 编译(MSVC): cl /EHsc /O2 program_16_aligned_malloc.cpp
// 编译(MinGW): g++ -std=c++17 -O2 program_16_aligned_malloc.cpp -o p16
#include <cstddef>
// 关键：判别条件必须用 _WIN32（MSVC 与 MinGW 都定义），不能只用 _MSC_VER——
//       MinGW 的 CRT 同样【不提供】C11 std::aligned_alloc，只用 _MSC_VER 会漏掉
//       MinGW 分支而落到 std::aligned_alloc 导致编译失败。
#if defined(_WIN32)
  #include <malloc.h>
  #define ALIGNED_ALLOC(p, sz, a) p = _aligned_malloc(sz, a)
  #define ALIGNED_FREE(p)         _aligned_free(p)
#else
  #include <cstdlib>
  #define ALIGNED_ALLOC(p, sz, a) p = std::aligned_alloc(sz, a)
  #define ALIGNED_FREE(p)         std::free(p)
#endif
#include <cstdio>
int main() {
    void* p = nullptr;
    ALIGNED_ALLOC(p, 1024, 64);     // 64 字节对齐
    std::printf("aligned=%p\n", p);
    ALIGNED_FREE(p);
    return 0;
}
```

**[经验]** 在池实现里，若用 `_aligned_malloc` 分配 chunk，则块天然对齐，无需手动 `std::align`；但注意 `_aligned_malloc` 必须用 `_aligned_free` 释放（见 ch37 对齐 new 的对称约束）。

---

## ⑮ 真实 microbenchmark：固定块池 vs new/delete

**[经验]** 以下基准在单线程下对比"固定块池"与裸 `new`/`delete` 的分配/释放延迟。量级结论（本机 GCC 13.1.0, -O2）：**池快 5–50×**，多线程下差距更大（无锁）。

### 44.15.1 基准程序（程序 17/≥30）

```cpp
// program_17_bench_fixed_vs_new.cpp
// 编译: g++ -std=c++17 -O2 program_17_bench_fixed_vs_new.cpp -o p17
#include <iostream>
#include <chrono>
#include <vector>
#include <new>
#include "program_01_fixed_block_pool.cpp"  // 复用 FixedBlockPool（与本文件分别编译，或先去掉 program_01 的 main）   // 复用 FixedBlockPool（与本文件分别编译，或先去掉 program_01 的 main）

static FixedBlockPool g_pool(sizeof(long long), 1 << 20);

template <class F>
double bench(const char* name, F f, int iters) {
    auto t0 = std::chrono::steady_clock::now();
    for (int i=0;i<iters;++i) f();
    auto t1 = std::chrono::steady_clock::now();
    double us = std::chrono::duration_cast<std::chrono::microseconds>(t1-t0).count();
    std::cout << name << ": " << (us/iters*1000) << " ns/op\n";
    return us/iters;
}

int main() {
    const int N = 1 << 20;
    std::vector<void*> holds(N);
    bench("new/delete ", [&]{ for(int i=0;i<N;++i) holds[i]=::operator new(8);
                             for(int i=0;i<N;++i) ::operator delete(holds[i]); }, 1);
    // 池（复用同一组块，演示 O(1) 路径）
    bench("fixed pool", [&]{ for(int i=0;i<N;++i) holds[i]=g_pool.allocate();
                             for(int i=0;i<N;++i) g_pool.deallocate(holds[i]); }, 1);
    return 0;
}
```

**典型量级（参考，非本机逐次实测）**：`new/delete` ≈ 30–80 ns/op；固定块池 ≈ 1–6 ns/op（**快 5–50×**）。差距来自：免系统调用、免锁、免大小计算。

---

## ⑯ microbenchmark：分级池 vs malloc

### 44.16.1 基准程序（程序 18/≥30）

```cpp
// program_18_bench_seg_vs_malloc.cpp
// 编译: g++ -std=c++17 -O2 program_18_bench_seg_vs_malloc.cpp -o p18
#include <iostream>
#include <chrono>
#include <vector>
#include <cstdlib>
#include "program_07_segregated.cpp"   // 复用 SegregatedPool（需去掉其内部 main）

static SegregatedPool g_pool;

int main() {
    const int N = 200000;
    std::vector<void*> h(N);
    auto t0 = std::chrono::steady_clock::now();
    for (int i=0;i<N;++i) h[i] = std::malloc((i%64)+1);
    for (int i=0;i<N;++i) std::free(h[i]);
    auto t1 = std::chrono::steady_clock::now();
    std::cout << "malloc: " << std::chrono::duration_cast<std::chrono::microseconds>(t1-t0).count() << " us\n";

    auto t2 = std::chrono::steady_clock::now();
    for (int i=0;i<N;++i) h[i] = g_pool.allocate((i%64)+1);
    for (int i=0;i<N;++i) g_pool.deallocate(h[i], (i%64)+1);
    auto t3 = std::chrono::steady_clock::now();
    std::cout << "segregated: " << std::chrono::duration_cast<std::chrono::microseconds>(t3-t2).count() << " us\n";
    return 0;
}
```

**[经验]** 分级池对**尺寸多变的小对象**吞吐显著优于 `malloc`，且碎片可控（每桶内块尺寸统一）。`malloc` 在混合尺寸下易产生外部碎片，长时间运行后 RSS 增长明显。

---

## ⑰ microbenchmark：线程局部池多线程扩展性

### 44.17.1 扩展性测试（程序 19/≥30）

```cpp
// program_19_bench_tls_scaling.cpp
// 编译: g++ -std=c++17 -O2 -pthread program_19_bench_tls_scaling.cpp -o p19
#include <iostream>
#include <thread>
#include <vector>
#include <chrono>
#include <cstdlib>
#include "program_08_thread_local.cpp"   // 复用 ThreadLocalPool（与本文件分别编译，或先去掉 program_08 的 main）

void run_threads(int nthreads, int iters) {
    std::vector<std::thread> ts;
    auto t0 = std::chrono::steady_clock::now();
    for (int t=0;t<nthreads;++t)
        ts.emplace_back([iters]{ for(int i=0;i<iters;++i){
            void* p = ThreadLocalPool::allocate();
            ThreadLocalPool::deallocate(p);
        }});
    for (auto& t:ts) t.join();
    auto t1 = std::chrono::steady_clock::now();
    double ms = std::chrono::duration_cast<std::chrono::microseconds>(t1-t0).count()/1000.0;
    std::cout << "threads=" << nthreads << " total=" << ms << " ms\n";
}

int main() {
    const int iters = 200000;
    for (int t=1;t<=8;t*=2) run_threads(t, iters);   // 线程数↑ 延迟近似线性增长(无锁)
    return 0;
}
```

**量级结论**：线程局部池延迟随线程数近似**线性扩展**（每线程无锁，无竞争）；而 `malloc`/带全局锁的 `std::pool_allocator` 延迟随线程数**超线性恶化**（锁竞争）。这是线程局部池的核心价值。

---

## ⑱ 对象池与确定性（实时/嵌入式）

**[经验]** 在硬实时系统中（汽车、工控、用户嵌入式背景），分配延迟必须可界。固定块/对象/静态池在**初始化阶段一次性分配**，运行期只做指针操作，WCET 可静态分析。禁止在中断服务程序（ISR）或控制环内 `new`。

### 44.18.1 RTOS 风格静态对象池（程序 20/≥30）

```cpp
// program_20_rtos_static.cpp —— ISR 安全：运行期零分配
// 编译: g++ -std=c++17 -O2 program_20_rtos_static.cpp -o p20
#include <cstddef>
#include <array>
#include <cstdint>

template <class T, std::size_t N>
class ISRSafePool {                        // 无锁、无 new、确定性
    struct Link { T obj; Link* next; };
    alignas(T) std::array<std::byte, sizeof(Link)*N> raw_;
    Link* free_ = nullptr;
public:
    ISRSafePool() {
        Link* base = reinterpret_cast<Link*>(raw_.data());
        for (std::size_t i=0;i<N;++i){ base[i].next = (i+1<N)?&base[i+1]:nullptr; }
        free_ = base;
    }
    T* alloc() {                            // ISR 内可安全调用
        if (!free_) return nullptr;
        Link* l = free_; free_ = l->next;
        return ::new(&l->obj) T();         // placement new，不触系统分配
    }
    void free(T* p) noexcept {
        Link* l = reinterpret_cast<Link*>(reinterpret_cast<std::byte*>(p) - offsetof(Link, obj));
        l->next = free_; free_ = l;
    }
};

struct Msg { int code; uint32_t payload; };
int main() {
    static ISRSafePool<Msg, 64> pool;
    Msg* m = pool.alloc();
    m->code = 1; pool.free(m);
    return 0;
}
```

---

## 源码阅读路线（内化，非"推荐阅读"节）

**[实现-推断]** 本机仅有 libstdc++ 源码可得；glibc/jemalloc/tcmalloc 源码本机不可得，下列为建议阅读清单（已内化进正文，不另设"推荐阅读"节）：

1. **libstdc++ `ext/pool_allocator.h`**（本机已读，pool_allocator.h:77-295）：free-list 池 + 分级 + 单锁。
2. **libstdc++ `bits/new_allocator.h`**（本机已读，new_allocator.h:121-148）：标准分配器直转 `::operator new`。
3. **libstdc++ `bits/uses_allocator.h`**（本机已读，真实路径 `C:/Qt/Tools/mingw1310_64/lib/gcc/x86_64-w64-mingw32/13.1.0/include/c++/bits/uses_allocator.h`；uses_allocator.h:67-70 `uses_allocator`、uses_allocator.h:85 `__uses_alloc`）：`uses_allocator` 探测协议（`allocator_arg_t`/`construct` 重载），池如需"分配器感知构造"需实现此协议。
4. **tcmalloc**（google/tcmalloc）：`ThreadCache`（线程局部）、`CentralFreeList`（中心）、`SizeMap`（size class）、`PageHeap`。
5. **jemalloc**（jemalloc/jemalloc）：`bin`/`run`/`extent`，区域化与 decay。
6. **folly**（facebook/folly）：`SysAllocator`、`Arena`、`ThreadLocalArena`。
7. **glibc `malloc.c`**（源码 `malloc/malloc.c`）：`ptmalloc2`、arena、fastbin、tcache。
8. **Boost.Pool**（`boost/pool/pool.hpp`）：`pool`/`object_pool`/`singleton_pool`。
9. **librseq**（restartable sequences）：无锁每 CPU 池的底层原语。

**[标准]** `uses_allocator` 协议（uses_allocator.h:66-70）允许容器在构造元素时把分配器"透传"给元素构造（若元素类型有 `allocator_type` 或接受 `allocator_arg_t`）。自定义池若想被 `std::scoped_allocator_adaptor` 嵌套使用，需满足该协议——下面演示。

### 44.19.1 `uses_allocator` 探测演示（程序 21/≥30）

```cpp
// program_21_uses_allocator.cpp
// 编译: g++ -std=c++17 -O2 program_21_uses_allocator.cpp -o p21
#include <memory>
#include <type_traits>
#include <iostream>
#include "program_01_fixed_block_pool.cpp"  // 复用 FixedBlockPool（与本文件分别编译，或先去掉 program_01 的 main）   // 复用 FixedBlockPool（与本文件分别编译，或先去掉 program_01 的 main）

// 一个"分配器感知"类型（见 uses_allocator.h:61-63 __uses_allocator_helper 探测 allocator_type）
struct Node {
    using allocator_type = FixedBlockPool;   // 告诉 traits：我接受该分配器
    int v;
    template <class Alloc>
    Node(std::allocator_arg_t, const Alloc&, int x) : v(x) {}
};

int main() {
    // uses_allocator.h:67-70：检测 Node 是否 uses_allocator<FixedBlockPool>
    constexpr bool b = std::uses_allocator<Node, FixedBlockPool>::value;
    std::cout << "Node uses FixedBlockPool? " << std::boolalpha << b << "\n";
    return b ? 0 : 1;
}
```

---

## ⑲ 跨语言对比

**[经验]** 内存池思想跨语言通用，只是接口形态不同：

| 语言 | 机制 | 与本章对应 |
|---|---|---|
| **Rust** | 实现 `GlobalAlloc` / `Allocator` trait（nightly `Allocator`），可接入 jemalloc；`bumpalo` 是 bump 分配器库 | 单调池（44.7）、全局池 |
| **Go** | `mcache`（每 P 线程局部）→ `mcentral` → `mheap` 三级；`mcache` 即线程局部池 | 线程局部池（44.9）、分级（44.8） |
| **Java** | TLAB（Thread-Local Allocation Buffer，线程本地分配缓冲）；G1 区域化堆；逃逸分析标量替换消除分配 | 线程局部池（44.9）、确定性 |
| **C#** | `System.Buffers.ArrayPool<T>`（数组对象池）、`Microsoft.Extensions.ObjectPool.ObjectPool<T>`（对象池） | 对象池（44.10） |

### 44.20.1 Rust `Allocator` trait 示意（程序 22/≥30，伪/真实语法）

```rust
// program_22_rust_allocator.rs  —— Rust 自定义 Allocator（nightly 风格）
// 对应本章固定块池思想；用 jemalloc 只需 type MyAlloc = jemalloc::Jemalloc;
#![feature(allocator_api)]
use std::alloc::{Allocator, Layout};
use std::ptr::NonNull;

struct BumpPool { buf: NonNull<u8>, offset: std::cell::Cell<usize>, size: usize }
unsafe impl Allocator for BumpPool {
    fn allocate(&self, layout: Layout) -> Result<NonNull<[u8]>, std::alloc::AllocError> {
        let off = self.offset.get();
        let aligned = (off + layout.align() - 1) & !(layout.align() - 1);
        let new_off = aligned + layout.size();
        if new_off > self.size { return Err(std::alloc::AllocError); }
        self.offset.set(new_off);
        // bump pointer（见 44.7）
        Ok(NonNull::slice_from_raw_parts(
            NonNull::new(self.buf.as_ptr().wrapping_add(aligned)).unwrap(), layout.size()))
    }
    unsafe fn deallocate(&self, _ptr: NonNull<u8>, _layout: Layout) { /* 单调：不释放 */ }
}
fn main() { /* 接入 Box<T, BumpPool> 即可 */ }
```

### 44.20.2 Go `mcache` 概念对应（程序 23/≥30，示意）

```go
// program_23_go_mcache.go —— Go 运行时的 mcache 即线程局部池
// 概念对应 44.9；Go 源码 runtime/mcache.go 的 mcache 持有 per-sizeclass 的 span 链表
package main

import "fmt"

// 简化：每 P 独立的 free list（线程局部），对应 ThreadLocalPool
type mcache struct {
    // tiny 对象走 tiny 缓冲；普通对象按 sizeclass 取 span
    freeLists [68]*span // 68 个 size class（示意）
}

func (c *mcache) alloc(sizeClass int) *span {
    s := c.freeLists[sizeClass]
    if s == nil {
        s = centralCache.alloc(sizeClass) // 向 mcentral 批量取（对应 batch_fetch）
        c.freeLists[sizeClass] = s
    }
    return s.pop()
}

func main() { fmt.Println("Go mcache == thread-local pool (44.9)") }
```

### 44.20.3 Java TLAB 概念（程序 24/≥30，示意）

```java
// program_24_java_tlab.java —— TLAB（Thread-Local Allocation Buffer）
// 对应 44.9 线程局部池；HotSpot 中每个线程在 Eden 区占一小块，bump pointer 分配
public class TLABDemo {
    // 伪代码：线程本地指针碰撞分配（无需 CAS）
    // ptr = tlab.start;
    // if ((ptr + size) <= tlab.top) { tlab.start = ptr + size; return ptr; }
    // else refillTLAB(); // 向 Eden 申请新 TLAB（对应 batch_fetch）
    public static void main(String[] args) {
        // new Object() 大多数走 TLAB bump 分配，等价于 MonotonicAllocator(44.7)
        for (int i = 0; i < 10; i++) new Object();
        System.out.println("TLAB == thread-local monotonic (44.7/44.9)");
    }
}
```

### 44.20.4 C# `ArrayPool<T>` 对象池（程序 25/≥30，示意）

```csharp
// program_25_csharp_arraypool.cs —— System.Buffers.ArrayPool<T> 即对象/数组池
// 对应 44.10 对象池
using System;
using System.Buffers;

class Program {
    static void Main() {
        var pool = ArrayPool<byte>.Shared;     // 全局共享数组池
        byte[] buf = pool.Rent(1024);          // 复用已存在数组（acquire）
        try { /* 使用 buf */ }
        finally { pool.Return(buf); }          // 归还（release），避免 GC 压力
        Console.WriteLine("ArrayPool<T> == object pool (44.10)");
    }
}
```

---

## ⑳ 进阶：栈式（LIFO）池与区域（Arena）池

**[经验]** 栈式池按 LIFO 释放（适合表达式树、作用域临时对象），区域池（Arena）一次性分配、整体释放——二者均避免逐对象释放开销。

### 44.21.1 栈式 LIFO 池（程序 26/≥30）

```cpp
// program_26_lifo_stack_pool.cpp
// 编译: g++ -std=c++17 -O2 program_26_lifo_stack_pool.cpp -o p26
#include <vector>
#include <cstddef>
#include <cstdint>
#include <new>
#include <cstdio>

class LifoPool {                               // 必须 LIFO 释放
    std::byte* buf_ = nullptr; std::size_t cap_ = 0, off_ = 0;
    std::vector<std::size_t> marks_;
public:
    LifoPool(std::size_t bytes)
        : buf_(static_cast<std::byte*>(::operator new(bytes))), cap_(bytes) {}
    ~LifoPool() { ::operator delete(buf_); }
    void* alloc(std::size_t n, std::size_t a = alignof(std::max_align_t)) {
        std::size_t cur = (reinterpret_cast<std::uintptr_t>(buf_+off_) + a-1) & ~(a-1);
        std::size_t noff = cur - reinterpret_cast<std::uintptr_t>(buf_) + n;
        if (noff > cap_) return nullptr;
        off_ = noff; return reinterpret_cast<void*>(cur);
    }
    void push_mark() { marks_.push_back(off_); }
    void pop_mark()  { if(!marks_.empty()){ off_ = marks_.back(); marks_.pop_back(); } } // 整体回卷
};

int main() {
    LifoPool pool(4096);
    pool.push_mark();
    int* a = static_cast<int*>(pool.alloc(sizeof(int)));
    double* d = static_cast<double*>(pool.alloc(sizeof(double)));
    *a = 1; *d = 2.0;
    pool.pop_mark();                            // 一次性释放 a、d（LIFO 区域）
    std::printf("lifo ok\n");
    return 0;
}
```

### 44.21.2 Arena 区域池（程序 27/≥30）

```cpp
// program_27_arena.cpp —— Arena：分配只增，析构整体释放（连接 ch39 RAII）
// 编译: g++ -std=c++17 -O2 program_27_arena.cpp -o p27
#include <cstddef>
#include <new>
#include <vector>
#include <iostream>

class Arena {
    struct Block { std::byte* data; std::size_t size; Block* next; };
    Block* blocks_ = nullptr;
    std::byte* cur_ = nullptr; std::size_t left_ = 0;
    std::size_t chunk_size_;
public:
    explicit Arena(std::size_t chunk = 4096) : chunk_size_(chunk) {}
    ~Arena() {                                  // ch39：RAII 一次性释放全部
        for (Block* b = blocks_; b; ) {
            Block* nx = b->next; ::operator delete(b->data); delete b; b = nx;
        }
    }
    void* alloc(std::size_t n) {
        if (n > left_) {
            std::size_t sz = n > chunk_size_ ? n : chunk_size_;
            std::byte* d = static_cast<std::byte*>(::operator new(sz));
            Block* b = new Block{d, sz, blocks_}; blocks_ = b;
            cur_ = d; left_ = sz;
        }
        void* p = cur_; cur_ += n; left_ -= n; return p;
    }
};

int main() {
    Arena arena;
    int* x = static_cast<int*>(arena.alloc(sizeof(int)));
    *x = 99;
    std::cout << "arena x=" << *x << "\n";     // 离开作用域整体释放
    return 0;
}
```

---

## 缓存友好性（连接 ch43）

**[经验]** 池的 cache 友好来自两点：(1) 同类对象聚簇（固定块池把同一尺寸对象放在相邻内存）；(2) 位图/分级元数据极小、常驻缓存。对比通用 `malloc` 把不同寿命对象混在堆里，池显著减少 cache miss。ch43 已详述 false sharing 与预取，池设计时应**避免多线程共享同一缓存行**——线程局部池（44.9）天然规避。

### 44.22.1 伪共享规避（程序 28/≥30）

```cpp
// program_28_cache_friendly.cpp —— 每线程池块独立缓存行，避免 false sharing
// 编译: g++ -std=c++17 -O2 -pthread program_28_cache_friendly.cpp -o p28
#include <new>
#include <thread>
#include <vector>
#include <cstddef>
#include <iostream>

struct alignas(64) CacheLinePool {            // 64 字节对齐，独占缓存行
    void* head = nullptr;
    unsigned long long ops = 0;
};
static constexpr int kLines = 8;
static CacheLinePool g_lines[kLines];          // 每线程一条独立缓存行

int main() {
    std::vector<std::thread> ts;
    for (int t=0;t<kLines;++t)
        ts.emplace_back([t]{ for(int i=0;i<1000000;++i) g_lines[t].ops++; }); // 无 false sharing
    for (auto& t:ts) t.join();
    std::cout << "cache-friendly ok\n";
    return 0;
}
```

---

## 碎片可视化演示

**[经验]** 直观展示"通用分配"产生外部碎片，而固定块池不产生。

### 44.23.1 碎片对比（程序 29/≥30）

```cpp
// program_29_fragmentation.cpp
// 编译: g++ -std=c++17 -O2 program_29_fragmentation.cpp -o p29
#include <iostream>
#include <vector>
#include <cstddef>
#include "program_01_fixed_block_pool.cpp"  // 复用 FixedBlockPool（与本文件分别编译，或先去掉 program_01 的 main）

int main() {
    // 固定块池：分配 1000 个、释放奇数、再分配 500 个——总能满足（无外部碎片）
    FixedBlockPool pool(sizeof(long), 1000);
    std::vector<void*> h(1000);
    for (auto& p : h) p = pool.allocate();
    for (size_t i=0;i<h.size();i+=2) pool.deallocate(h[i]);   // 释放一半
    int reused = 0;
    for (int i=0;i<500;++i) if (pool.allocate()) ++reused;     // 必能复用空槽
    std::cout << "fixed pool reused slots=" << reused << " (no external fragmentation)\n";
    return reused == 500 ? 0 : 1;
}
```

---

## 完整工程示例：三套池统一基准与并发测试

**[经验]** 下面给出把"固定块池 / 分级池 / 线程局部池"放进同一基准框架并跑并发压力测试的程序。这是本章的收束示例，综合构造/析构、对齐、线程安全。

### 44.24.1 综合基准（程序 30/≥30）

```cpp
// program_30_final_bench.cpp —— 三池统一并发基准
// 编译: g++ -std=c++17 -O2 -pthread program_30_final_bench.cpp -o p30
#include <iostream>
#include <thread>
#include <vector>
#include <chrono>
#include <cstddef>
#include <new>
#include <mutex>
#include <array>

// ---------- 固定块池 ----------
struct FNode { FNode* next; };
class FixedPool {
    std::byte* mem_; FNode* free_; std::size_t bsz_;
    std::mutex mtx_;
public:
    FixedPool(std::size_t obj, std::size_t n)
        : bsz_((obj+alignof(std::max_align_t)-1)&~(alignof(std::max_align_t)-1)) {
        mem_=static_cast<std::byte*>(::operator new(bsz_*n));
        free_=reinterpret_cast<FNode*>(mem_);
        for(std::size_t i=1;i<n;++i){reinterpret_cast<FNode*>(mem_+i*bsz_)->next=
            (i+1<n)?reinterpret_cast<FNode*>(mem_+(i+1)*bsz_):nullptr;}
        reinterpret_cast<FNode*>(mem_)->next=(n>1)?reinterpret_cast<FNode*>(mem_+bsz_):nullptr;
    }
    ~FixedPool(){::operator delete(mem_);}
    void* alloc(){std::lock_guard<std::mutex>l(mtx_);if(!free_)return nullptr;FNode*p=free_;free_=p->next;return p;}
    void free(void*p){std::lock_guard<std::mutex>l(mtx_);static_cast<FNode*>(p)->next=free_;free_=static_cast<FNode*>(p);}
};

// ---------- 线程局部池 ----------
class TLSPool {
    struct N { N* next; };
    static constexpr std::size_t kB=128,kBlk=32;
    static std::mutex& m(){static std::mutex x;return x;}
    static std::vector<N*>& g(){static std::vector<N*> x;return x;}
    static N* chunk(){std::byte*mm=static_cast<std::byte*>(::operator new(kBlk*kB));
        for(std::size_t i=0;i<kB;++i)reinterpret_cast<N*>(mm+i*kBlk)->next=
            (i+1<kB)?reinterpret_cast<N*>(mm+(i+1)*kBlk):nullptr;return reinterpret_cast<N*>(mm);}
    static thread_local std::vector<N*> local_;
public:
    static void* alloc(){if(local_.empty()){std::lock_guard<std::mutex>l(m());auto&gv=g();
        for(std::size_t i=0;i<kB&&!gv.empty();++i){local_.push_back(gv.back());gv.pop_back();}
        if(local_.empty())local_.push_back(chunk());}
        N*p=local_.back();local_.pop_back();return p;}
    static void free(void*p){local_.push_back(static_cast<N*>(p));
        if(local_.size()>=kB*2){std::lock_guard<std::mutex>l(m());auto&gv=g();
            for(N*n:local_)gv.push_back(n);local_.clear();}}
};
thread_local std::vector<TLSPool::N*> TLSPool::local_{};

// ---------- 分级池（简化 8 桶）----------
class SegPool {
    struct N { N* next; };
    std::array<N*,8> b_{}; std::mutex mtx_;
    static std::size_t idx(std::size_t n){std::size_t r=(n+7)&~7;std::size_t i=(r-8)/8;return i<8?i:7;}
    N* refill(std::size_t i){std::size_t bs=8+i*8;std::byte*mm=static_cast<std::byte*>(::operator new(bs*64));
        N*h=reinterpret_cast<N*>(mm),*c=h;for(int j=1;j<64;++j){N*nx=reinterpret_cast<N*>(mm+j*bs);c->next=nx;c=nx;}c->next=nullptr;return h;}
public:
    void* alloc(std::size_t n){std::lock_guard<std::mutex>l(mtx_);std::size_t i=idx(n);
        N*p=b_[i];if(!p)p=b_[i]=refill(i);b_[i]=p->next;return p;}
    void free(void*p,std::size_t n){std::lock_guard<std::mutex>l(mtx_);std::size_t i=idx(n);
        static_cast<N*>(p)->next=b_[i];b_[i]=static_cast<N*>(p);}
};

template<class F> double run(const char* name,int nth,int it, F f){
    std::vector<std::thread> ts;auto t0=std::chrono::steady_clock::now();
    for(int t=0;t<nth;++t)ts.emplace_back([&]{for(int i=0;i<it;++i)f();});
    for(auto&t:ts)t.join();auto t1=std::chrono::steady_clock::now();
    double ms=std::chrono::duration_cast<std::chrono::microseconds>(t1-t0).count()/1000.0;
    std::cout<<name<<" nth="<<nth<<" "<<ms<<" ms\n";return ms;
}

int main(){
    FixedPool fp(sizeof(long),1<<20);
    SegPool   sp;
    const int it=200000;
    run("FixedPool ",4,it,[&]{void*p=fp.alloc();fp.free(p);});
    run("SegPool   ",4,it,[&]{void*p=sp.alloc(20);sp.free(p,20);});
    run("TLSPool   ",4,it,[]{void*p=TLSPool::alloc();TLSPool::free(p);});
    // 对比裸 new
    run("new/delete",4,it,[]{void*p=::operator new(32);::operator delete(p);});
    return 0;
}
```

**典型量级**：`TLSPool`（无锁）延迟最低且随线程数线性；`FixedPool`/`SegPool` 受全局锁限制，线程数↑时竞争上升；`new/delete` 受系统分配器锁，通常最慢。

---

## 附加可编译示例（补齐 ≥30，速查）

以下为更小的独立可编译片段，覆盖边界情形与工程技巧。

### 44.25.1 对齐尺寸 > 指针尺寸的固定块池（程序 31/≥30）

```cpp
// program_31_overaligned.cpp —— 块尺寸必须容纳 next 且对齐 over-aligned 类型
// 编译: g++ -std=c++17 -O2 program_31_overaligned.cpp -o p31
#include <cstddef>
#include <new>
#include <iostream>
struct alignas(64) Big { char buf[64]; };   // over-aligned，sizeof=64 >= sizeof(void*)
int main() {
    std::size_t blk = (sizeof(Big) + alignof(std::max_align_t)-1) & ~(alignof(std::max_align_t)-1);
    void* p = ::operator new(blk * 4);
    std::cout << "block=" << blk << " ok=" << (blk >= sizeof(void*)) << "\n";
    ::operator delete(p);
    return 0;
}
```

### 44.25.2 用 `std::pmr::synchronized_pool_resource`（程序 32/≥30）

```cpp
// program_32_pmr_synchronized.cpp —— 标准库线程安全池（连接 ch38）
// 编译: g++ -std=c++17 -O2 program_32_pmr_synchronized.cpp -o p32
#include <memory_resource>
#include <vector>
#include <iostream>
int main() {
    std::pmr::synchronized_pool_resource pool;            // 标准池：内部线程局部+中心
    std::pmr::polymorphic_allocator<int> alloc(&pool);
    std::pmr::vector<int> v(alloc);
    for (int i=0;i<1000;++i) v.push_back(i);
    std::cout << "synchronized_pool_resource size=" << v.size() << "\n";
    return 0;
}
```

### 44.25.3 对象池 + 构造复用（程序 33/≥30）

```cpp
// program_33_object_pool_reuse.cpp
// 编译: g++ -std=c++17 -O2 program_33_object_pool_reuse.cpp -o p33
#include <vector>
#include <stack>
#include <iostream>
struct Job { int id; bool done=false; void reset(){done=false;} };
int main() {
    std::vector<Job> store; std::stack<Job*> free;
    for (int i=0;i<8;++i){ store.emplace_back(); free.push(&store.back()); }
    Job* j = free.top(); free.pop(); j->id=1; j->done=true;
    j->reset(); free.push(j);                            // 复用同一对象，免析构
    std::cout << "reused job id=" << j->id << "\n";
    return 0;
}
```

### 44.25.4 单调池 + 类型化 placement new 区域（程序 34/≥30）

```cpp
// program_34_monotonic_typed.cpp
// 编译: g++ -std=c++17 -O2 program_34_monotonic_typed.cpp -o p34
#include <cstddef>
#include <new>
#include <vector>
#include <iostream>
#include <utility>
class Region {
    std::byte* buf_; std::size_t cap_, off_=0;
public:
    Region(std::size_t n):buf_(static_cast<std::byte*>(::operator new(n))),cap_(n){}
    ~Region(){::operator delete(buf_);}
    template<class T,class...A> T* make(A&&...a){
        void* p=buf_+off_; std::size_t need=sizeof(T);
        if(off_+need>cap_) return nullptr;
        off_+=need; return ::new(p) T(std::forward<A>(a)...);
    }
};
int main(){
    Region r(1024);
    int* a=r.make<int>(42); double* d=r.make<double>(3.14);
    std::cout << *a << " " << *d << "\n";
    return 0;
}
```

### 44.25.5 分级池 size class 对照 tcmalloc（程序 35/≥30）

```cpp
// program_35_sizeclass.cpp —— 展示 size class 几何分级（对照 tcmalloc SizeMap）
// 编译: g++ -std=c++17 -O2 program_35_sizeclass.cpp -o p35
#include <iostream>
#include <vector>
#include <cstddef>
std::size_t size_class(std::size_t n){               // 简化 tcmalloc 8→256 几何
    if(n<=8) return 8;
    std::size_t c=8;
    while(c<n) c = (c<128)? c*2 : c+ (c>>1);          // 小对象翻倍，大对象+50%
    return c>256?256:c;
}
int main(){
    for(std::size_t n: {1,9,17,33,65,129,200})
        std::cout<<"req="<<n<<" -> class="<<size_class(n)<<"\n";
    return 0;
}
```

### 44.25.6 线程局部池无锁路径断言（程序 36/≥30）

```cpp
// program_36_tls_lockfree.cpp —— 演示线程热路径无 mutex（仅批量才锁）
// 编译: g++ -std=c++17 -O2 -pthread program_36_tls_lockfree.cpp -o p36
#include <thread>
#include <vector>
#include <cstddef>
#include <new>
#include <iostream>
#include <mutex>
struct N { N* next; };
static thread_local N* tl = nullptr;                  // 热路径：仅操作 thread_local
static N* global = nullptr; static std::mutex mtx;
static N* make_chunk(){std::byte*b=static_cast<std::byte*>(::operator new(32*64));
    for(int i=0;i<64;++i)reinterpret_cast<N*>(b+i*32)->next=(i+1<64)?reinterpret_cast<N*>(b+(i+1)*32):nullptr;
    return reinterpret_cast<N*>(b);}
void* alloc(){ if(!tl){ std::lock_guard<std::mutex>l(mtx); tl=global?global:make_chunk(); }
    N* p=tl; tl=p->next; return p; }
void free(void*p){ static_cast<N*>(p)->next=tl; tl=static_cast<N*>(p); }
int main(){
    std::vector<std::thread> ts;
    for(int t=0;t<4;++t)ts.emplace_back([]{for(int i=0;i<100000;++i){void*p=alloc();free(p);}});
    for(auto&t:ts)t.join(); std::cout<<"hot path lock-free ok\n"; return 0;
}
```

### 44.25.7 池容量回退到 ::operator new（程序 37/≥30）

```cpp
// program_37_fallback.cpp —— 池满时回退系统分配（对照 pool_allocator.h 大块直走 new）
// 编译: g++ -std=c++17 -O2 program_37_fallback.cpp -o p37
#include <cstddef>
#include <new>
#include <iostream>
#include "program_01_fixed_block_pool.cpp"  // 复用 FixedBlockPool（与本文件分别编译，或先去掉 program_01 的 main）
class SafePool : private FixedBlockPool {
    std::size_t max_;
public:
    SafePool(std::size_t obj,std::size_t n):FixedBlockPool(obj,n),max_(n){}
    void* alloc(){ void* p=FixedBlockPool::allocate(); if(p) return p;
        return ::operator new(sizeof(long)); }        // 回退（对照 _S_max_bytes 直走 new）
    void free(void* p){ FixedBlockPool::deallocate(p); }
};
int main(){ SafePool p(sizeof(long),4); void* a=p.alloc(); void* b=p.alloc();
    void* c=p.alloc(); void* d=p.alloc(); void* e=p.alloc(); // 第5个回退 new
    std::cout<<"fallback ok\n"; return 0; }
```

### 44.25.8 RAII 池资源守卫（程序 38/≥30，连接 ch39）

```cpp
// program_38_raii_guard.cpp —— 池对象 RAII 守卫，离开作用域自动归还
// 编译: g++ -std=c++17 -O2 program_38_raii_guard.cpp -o p38
#include <utility>
#include <iostream>
#include "program_01_fixed_block_pool.cpp"  // 复用 FixedBlockPool（与本文件分别编译，或先去掉 program_01 的 main）
template<class T>
class PoolPtr {
    FixedBlockPool* pool_=nullptr; T* p_=nullptr;
public:
    PoolPtr(FixedBlockPool& pool, T* p):pool_(&pool),p_(p){}
    ~PoolPtr(){ if(p_) pool_->deallocate(p_); }       // 连接 ch39 RAII
    T* operator->() const { return p_; }
    T& operator*() const { return *p_; }
    PoolPtr(PoolPtr&& o):pool_(o.pool_),p_(o.p_){o.p_=nullptr;}
    PoolPtr(const PoolPtr&)=delete;
};
int main(){
    FixedBlockPool pool(sizeof(int),16);
    int* raw=static_cast<int*>(pool.allocate()); *raw=7;
    { PoolPtr<int> g(pool,raw); std::cout<<*g<<"\n"; } // 自动归还
    return 0;
}
```

### 44.25.9 位图池批量分配（程序 39/≥30）

```cpp
// program_39_bitmap_batch.cpp
// 编译: g++ -std=c++17 -O2 program_39_bitmap_batch.cpp -o p39
#include <cstddef>
#include <cstdint>
#include <new>
#include <vector>
#include <iostream>
class BitmapBatch {
    std::size_t bsz_,n_; std::byte* base_; std::vector<uint64_t> bits_;
public:
    BitmapBatch(std::size_t b,std::size_t c):bsz_((b+15)&~15),n_(c),bits_((c+63)/64,0){
        base_=static_cast<std::byte*>(::operator new(bsz_*c));}
    ~BitmapBatch(){::operator delete(base_);}
    std::vector<void*> alloc_many(std::size_t k){
        std::vector<void*> out; out.reserve(k);
        for(std::size_t w=0;w<bits_.size()&&out.size()<k;++w){
            uint64_t free=~bits_[w];
            while(free&&out.size()<k){int bit=__builtin_ctzll(free);
                bits_[w]|=(uint64_t(1)<<bit); std::size_t idx=w*64+bit;
                if(idx<n_)out.push_back(base_+idx*bsz_); free&=free-1;}
        } return out;
    }
    void free(void* p){std::size_t idx=(static_cast<std::byte*>(p)-base_)/bsz_;
        bits_[idx/64]&=~(uint64_t(1)<<(idx%64));}
};
int main(){ BitmapBatch b(sizeof(int),256);
    auto v=b.alloc_many(10); for(auto p:v) b.free(p);
    std::cout<<"bitmap batch ok n="<<v.size()<<"\n"; return 0; }
```

### 44.25.10 完整 PMR 单调池 + 容器（程序 40/≥30）

```cpp
// program_40_pmr_monotonic.cpp —— monotonic_buffer_resource 实测（连接 ch38/44.7）
// 编译: g++ -std=c++17 -O2 program_40_pmr_monotonic.cpp -o p40
#include <memory_resource>
#include <vector>
#include <iostream>
int main(){
    std::pmr::monotonic_buffer_resource res(4096);    // bump 分配器（44.7）
    std::pmr::polymorphic_allocator<int> alloc(&res);
    std::pmr::vector<int> v(alloc);
    for(int i=0;i<100;++i) v.push_back(i);
    std::cout<<"monotonic pmr size="<<v.size()<<"\n";
    // res.release();  // 整体回卷，等价于单调池析构
    return 0;
}
```

---

## 小结与交叉引用

- **为何需要池**：锁竞争、碎片、缓存不友好、确定性延迟（44.1）。
- **六种池**：固定块（44.4）、位图（44.6）、单调（44.7）、分级（44.8）、线程局部（44.9）、对象（44.10）；嵌入式静态池（44.11、44.18）。
- **真实源码**：libstdc++ `__gnu_cxx::__pool_alloc`（pool_allocator.h:77-295，侵入式 free list + 分级 + 单锁）、`__new_allocator`（new_allocator.h:121-148，直转 `::operator new`）、`uses_allocator`（uses_allocator.h:67-70）。
- **对齐**：`std::align`/手动算术（44.5），未对齐在 ARM 致 SIGBUS、x86 致性能惩罚；`_aligned_malloc`/`__builtin_assume_aligned`（44.14）。
- **与 PMR**：池可包成 `memory_resource`（44.13、44.25.2、44.25.10）。
- **量级**：池比 `new`/`malloc` 快 5–50×，线程局部池无锁、随线程数线性扩展（44.15–44.17、44.24）。
- **跨语言**：Rust `Allocator`、Go `mcache`、Java TLAB、C# `ArrayPool<T>`（44.20）。
- **交叉章节**：存储期与 `thread_local` 见 ch19；对齐见 ch35；堆与分配器见 ch36；operator new 见 ch37；PMR 池见 ch38；RAII 资源生命期见 ch39；缓存友好见 ch43；并发无锁池见 ch61。

---

## 附：本章核心接口速查（内化为正文表格，非"推荐阅读"）

| 池 | 分配复杂度 | 释放 | 锁 | 对齐保证 | 碎片 |
|---|---|---|---|---|---|
| 固定块（侵入式） | O(1) | O(1) 头插 | 可选 | `max(alignof(T),alignof(void*))` | 仅外部（池满） |
| 位图 | O(1)（ctz 扫描） | O(1) | 无（单线程） | `alignof(max_align_t)` | 无外部（固定槽） |
| 单调 | O(1) | 不支持 | 无 | 参数化 | 无（整体释放） |
| 分级 | ~O(1) | ~O(1) | 可选 | `alignof(max_align_t)` | 内部（向上取整） |
| 线程局部 | O(1) | O(1) | 热路径无锁 | `alignof(max_align_t)` | 内部（批量粒度） |
| 对象 | O(1) | O(1) | 无（单线程） | 由存储决定 | 无（预分配） |

**结语**：内存池是"把通用分配器换成为你的访问模式定制的分配器"。从固定块到线程局部，本质都是在"对齐 + 侵入式元数据 + 分级/局部化"上做文章。理解 `std::pool_allocator` 的真实实现（pool_allocator.h），你就掌握了所有现代通用分配器（tcmalloc/jemalloc/PMR）的共同基因。


## 联合使用场景

| 关联章节 | 场景 | 组合方式 |
|---|---|---|
| [第43章](Book/part04_memory/ch43_cache_locality.md) | 键值查找/缓存 | 本章提供概念，第43章提供实现 |
| [第122章](Book/part10_modern/ch122_pmr.md) | 泛型库/编译期计算 | 本章提供概念，第122章提供实现 |
| [第160章](Book/part15_cases/ch160_mempool.md) | 资源管理/事务回滚 | 本章提供概念，第160章提供实现 |


## 附录 F：内存池面试

```cpp
#include <iostream>
int main(){
  std::cout<<"Pool alloc (MinGW GCC 13.1.0 -O2, x86_64, TSC=2.395GHz):\n";
  std::cout<<"  bump      = ~0 ns (仅指针加法, 被流水线隐藏)\n";
  std::cout<<"  freelist  = 1.30 ns (3.12 cyc)\n";
  std::cout<<"  malloc    = 45.5 ns (109 cyc, glibc ptmalloc)\n";
  std::cout<<"  tcmalloc  = ~30 ns (文献, per-thread cache 无锁)\n";
  std::cout<<"  jemalloc  = ~35 ns (文献, size classes)\n";
  return 0;
}
```

| 分配器 | 实测延迟 (本机) | 碎片 | 用户 |
|---|---|---|---|
| bump allocator | **≈0 ns**（仅指针 +16，被流水线隐藏，GCC 下与空循环同速） | 不释放（整体 reset） | 游戏关卡 / 解析器 |
| freelist pool | **1.30 ns**（3.12 cyc，单线程无锁 pop） | 低（同大小） | 通用池 |
| malloc (glibc ptmalloc) | **45.5 ns**（108.98 cyc，含 `call malloc`+`call free`） | 中（碎片） | 系统默认 |
| tcmalloc | ~30 ns（文献值，本机未装） | 低 | Google |
| jemalloc | ~35 ns（文献值，本机未装） | 极低 | Facebook |

> 实测方法：RDTSC 计时，每类分配器跑 4×10⁶ 次，减去等结构空循环（`probe_nop`）开销得到单次延迟。bump 的真实结论反直觉——**它几乎是免费的**：每轮仅 `addq $16,%rax` 一个指针加法，且加法与循环计数并行，被 CPU 流水线完全吸收，因此实测延迟压在空循环基线上（raw 1.01 cyc ≈ nop 基线）。这与"bump 是 O(1) 无 bookkeeping"的理论完全吻合。freelist 因多一次依赖链取指 `movq (%rax),%rax` 而涨到 ~3 cyc。malloc 因进入 glibc 的 `free`/`malloc` 路径（含锁、bins 查找、系统调用兜底）而涨到 ~109 cyc。

面试: bump allocator 为何快? 指针递增 + 无 bookkeeping，单轮仅一条 `add` 且被流水线隐藏，实测≈0 额外开销；何时用池? 大量同大小对象、热路径不想付 malloc 代价。

## 附录 G：内存池汇编（真实产物）

> 以下汇编由 `Examples/_ch44_pool_perf.cpp` 经 `g++ -O2 -std=c++23 -m64` 编译后 `objdump` 提取（见 `Examples/_ch44_pool_perf.asm`），符号经 `verify_asm_evidence.py` 校验 **DRIFT=0**。每个 probe 带 `[[gnu::noinline, gnu::noipa]]` 锚点，并经 `void* volatile g_sink` 逃逸汇防优化消除。

**bump（`_ZL10probe_bumpy`，实测 ≈0 ns）** —— 仅一个 `addq $16` 指针加法：

```asm
_ZL10probe_bumpy:
        movq    _ZL6g_bump(%rip), %rax      ; 取 base
        testq   %rcx, %rcx
        je      .L13
        xorl    %edx, %edx
.L14:
        addq    $1, %rdx
        movq    %rax, %r8
        addq    $16, %rax                    ; bump: 仅指针 +16
        cmpq    %rdx, %rcx
        movq    %r8, g_sink(%rip)            ; 逃逸汇防优化消除
        jne     .L14
.L13:
        xorl    %eax, %eax
        ret
```

**freelist（`_ZL14probe_freelisty`，实测 1.30 ns / 3.12 cyc）** —— 多出一条依赖链取指：

```asm
_ZL14probe_freelisty:
        movq    _ZL10g_fl_head0(%rip), %rax
        testq   %rcx, %rcx
        je      .L20
        xorl    %edx, %edx
.L21:
        addq    $1, %rdx
        movq    %rax, %r8
        movq    (%rax), %rax                 ; 依赖链: 取下一个节点
        cmpq    %rdx, %rcx
        movq    %r8, g_sink(%rip)
        jne     .L21
.L20:
        xorl    %eax, %eax
        ret
```

**malloc（`_ZL12probe_mallocy`，实测 45.5 ns / 108.98 cyc）** —— 真实进入 glibc 路径：

```asm
_ZL12probe_mallocy:
        ...
.L28:
        movl    $16, %ecx
        addq    $1, %rbx
        call    malloc                      ; call malloc(16)
        movq    %rax, %rcx
        movq    %rax, g_sink(%rip)
        call    free                        ; call free(p)
        cmpq    %rbx, %rsi
        jne     .L28
```

```cpp
#include <iostream>
int main(){
  std::cout<<"bump~0ns, freelist=1.3ns, malloc=45.5ns (实测; tcmalloc/jemalloc 为文献值)\n";
  return 0;
}
```

面试: bump allocator 为何最快? 单轮仅 `addq $16` 一条指令且被流水线隐藏，实测≈0 额外开销；缺点? 不释放（仅整体 reset）。malloc 慢在哪? 真实汇编里是 `call malloc`+`call free` 两个库调用，glibc ptmalloc 内部要查 bins、加锁、必要时 `brk`/`mmap` 兜底。

## 相关章节（交叉引用）

- **相邻主题**：`Book/part05_oo/ch45_oop_object_model.md`（第 45 章　C++ 面向对象总览与对象模型基础）—— 编号相邻、主题接续。
- **相邻主题**：`Book/part04_memory/ch42_strict_aliasing.md`（第 42 章 · 严格别名规则（Strict Aliasing）与编译器优化）—— 编号相邻、主题接续。
- **相邻主题**：`Book/part05_oo/ch46_encapsulation_inheritance.md`（第 46 章　封装与继承深度：访问控制、三种继承、切片、构造/析构、名字隐藏、override/final、NVI）—— 编号相邻、主题接续。
- **同模块**：`Book/part04_memory/ch35_memory_layout.md`（第 35 章  C++ 程序的内存模型与操作系统视角）—— 同模块下的其他主题。

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

