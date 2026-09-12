// Examples/_atom_perf_move.cpp
// 服务 ATOM-MEM-PERF-001：移动性能量化。
// 核心论断：移动构造的收益来自"掏空源对象"——只偷指针（8 字节）并置空源；
// 对无动态资源的纯值类型，移动 = 拷贝（搬全部字节），std::move 无收益。
// 纪律（沿用 EV-MEM-002）：计数类 volatile 防折叠；初值由 argc 派生防 -O2 把值类型整组消除。
#include <utility>
#include <iostream>
#include <new>
#include <cstdlib>

volatile long g_allocs = 0;                 // volatile：防 -O2 把分配计数常量折叠（M2 §5）
void* operator new[](std::size_t n) { g_allocs = g_allocs + 1; return std::malloc(n); }
void operator delete[](void* p) noexcept { std::free(p); }

struct Value32 { long long a[4]; };         // 32 字节纯值类型，无动态资源
struct HeapBuf {
    long long* p;
    HeapBuf() : p(new long long[4]) {}
    ~HeapBuf() { delete[] p; }
    HeapBuf(const HeapBuf& o) : p(new long long[4]) { for (int i = 0; i < 4; i++) p[i] = o.p[i]; }
    HeapBuf(HeapBuf&& o) noexcept : p(o.p) { o.p = nullptr; }   // 移动：偷指针并置空源
};

int main(int argc, char** argv) {
    long long seed = argc;                  // 运行时值：防值类型被编译期折叠
    // ---- 纯值类型：移动 == 拷贝（都搬 32 字节，源不被掏空）----
    Value32 x; for (int i = 0; i < 4; i++) x.a[i] = seed + i;
    Value32 yc = x;                          // 拷贝构造
    Value32 ym = std::move(x);               // 移动构造（纯值类型：同样逐字节搬）
    volatile long long sink_v = yc.a[0] + ym.a[0];   // 强制观测，防整组消除
    (void)sink_v;

    // ---- 堆类型：移动只偷指针（0 分配），拷贝要分配 + 搬数据 ----
    HeapBuf h;
    long before = g_allocs;
    HeapBuf hc = h;                          // 拷贝：触发 1 次分配
    long copy_alloc = g_allocs - before;
    before = g_allocs;
    HeapBuf hm = std::move(h);               // 移动：0 分配
    long move_alloc = g_allocs - before;
    volatile long sink_h = (long)(hc.p != hm.p);
    (void)sink_h;

    std::cout << "Value32 sizeof=" << sizeof(Value32) << " move_eq_copy_bytes\n";
    std::cout << "heap copy_allocs=" << copy_alloc << " move_allocs=" << move_alloc << "\n";
    std::cout << "value move source intact=" << (ym.a[0] == seed) << "\n";
    return 0;
}
