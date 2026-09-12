// Examples/_atom_alloc_basic.cpp
// 服务 ATOM-MEM-ALLOC-001：std::allocator 的基本接口与"分配/构造"两层分离。
// 论断：allocator::allocate 只分配不构造（C++17 后 std::allocator 连 construct/destroy 都移除了，
//       统一经 std::allocator_traits::construct/destroy）——分配层与对象生命周期是两个独立动作。
// 计数纪律：volatile 计数器 + x = x + 1 拆写。
#include <memory>
#include <iostream>
#include <new>
#include <cstdlib>

volatile long g_allocs = 0;
volatile long g_frees = 0;
volatile long g_ctors = 0;
volatile long g_dtors = 0;
void* operator new(size_t n) { g_allocs = g_allocs + 1; return std::malloc(n); }
void operator delete(void* p) noexcept { if (p) { g_frees = g_frees + 1; std::free(p); } }
void operator delete(void* p, size_t) noexcept { if (p) { g_frees = g_frees + 1; std::free(p); } }

struct Widget {
    int v;
    explicit Widget(int v) : v(v) { g_ctors = g_ctors + 1; }
    ~Widget() { g_dtors = g_dtors + 1; }
};

int main() {
    using Alloc = std::allocator<Widget>;
    using Traits = std::allocator_traits<Alloc>;
    Alloc al;

    long a0 = g_allocs, c0 = g_ctors, f0 = g_frees;
    Widget* p = al.allocate(2);                     // 第 1 层：只分配，不构造
    long allocs = g_allocs - a0;
    long ctors_after_alloc = g_ctors - c0;

    Traits::construct(al, p, 7);                    // 第 2 层：显式构造（placement new 的封装）
    Traits::construct(al, p + 1, 9);
    long ctors_total = g_ctors - c0;

    Traits::destroy(al, p);                         // 显式析构（对偶动作）
    Traits::destroy(al, p + 1);
    long dtors_total = g_dtors;

    al.deallocate(p, 2);                            // 第 1 层的释放
    long frees = g_frees - f0;

    std::cout << "allocate: allocs=" << allocs << " ctors=" << ctors_after_alloc << " (allocation only)\n";
    std::cout << "construct: ctors=" << (ctors_total - ctors_after_alloc) << "\n";
    std::cout << "destroy: dtors=" << dtors_total << "\n";
    std::cout << "deallocate: frees=" << frees << "\n";
    return 0;
}
