// Examples/_atom_alloc_arena.cpp
// 服务 ATOM-MEM-ALLOC-001：自定义有状态 arena 分配器。
// 论断：allocator 是容器的内存**策略**抽象——容器只经 allocator_traits 要内存，不关心策略；
//       arena 策略（预分配一块、线性推进、不逐次释放）可无缝接入 std::vector，且堆分配为 0。
// 对照组：同长度的 std::vector<int>（默认策略），扩容全部走堆。
// 计数纪律：volatile 计数器 + 拆写复合赋值。
#include <vector>
#include <iostream>
#include <new>
#include <cstdlib>
#include <stdexcept>
#include <cstddef>

volatile long g_heap_new = 0;
volatile long g_arena_calls = 0;
volatile long long g_arena_bytes = 0;
void* operator new(size_t n) { g_heap_new = g_heap_new + 1; return std::malloc(n); }
void operator delete(void* p) noexcept { std::free(p); }
void operator delete(void* p, size_t) noexcept { std::free(p); }

template <class T>
struct Arena {
    using value_type = T;
    char* buf; std::size_t cap; std::size_t* off;   // off 用指针共享：rebind 出的副本同一游标
    Arena(char* b, std::size_t c, std::size_t* o) : buf(b), cap(c), off(o) {}
    template <class U> Arena(const Arena<U>& o) : buf(o.buf), cap(o.cap), off(o.off) {}
    template <class U> struct rebind { using other = Arena<U>; };

    T* allocate(std::size_t n) {
        if (*off + n * sizeof(T) > cap) throw std::bad_alloc();
        T* p = reinterpret_cast<T*>(buf + *off);
        *off += n * sizeof(T);
        g_arena_calls = g_arena_calls + 1;
        g_arena_bytes = g_arena_bytes + (long long)(n * sizeof(T));
        return p;
    }
    void deallocate(T*, std::size_t) noexcept {}    // arena 策略：不逐次释放，整体随 buf 回收

    friend bool operator==(const Arena& a, const Arena& b) { return a.buf == b.buf; }
    friend bool operator!=(const Arena& a, const Arena& b) { return !(a == b); }
};

int main() {
    alignas(16) static char buf[1024];
    std::size_t off = 0;

    long h0 = g_heap_new;
    {
        std::vector<int, Arena<int>> v((Arena<int>(buf, sizeof buf, &off)));
        for (int i = 0; i < 16; ++i) v.push_back(i);   // 扩容全部从 arena 出，堆 0 分配
    }                                                  // 析构不调 deallocate；buf 是栈内存，无泄漏
    long heap_arena = g_heap_new - h0;

    long h1 = g_heap_new;
    {
        std::vector<int> w;                            // 对照：默认 std::allocator 策略
        for (int i = 0; i < 16; ++i) w.push_back(i);   // 扩容全部走堆
    }
    long heap_std = g_heap_new - h1;

    std::cout << "arena: calls=" << g_arena_calls << " bytes=" << g_arena_bytes
              << " heap_new=" << heap_arena << "\n";
    std::cout << "std  : heap_new=" << heap_std << " (growth reallocations)\n";
    return 0;
}
