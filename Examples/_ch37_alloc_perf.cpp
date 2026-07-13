// Examples/_ch37_alloc_perf.cpp
// 第 37 章 microbenchmark 真实化：用 RDTSC 直接测每轮分配的 CPU 周期→纳秒。
// 编译：本机 MinGW GCC 13.1.0 -O2 -std=c++23 x86_64
//   g++ -O2 -std=c++23 _ch37_alloc_perf.cpp -o _ch37_alloc_perf.exe
// 计时法：__rdtsc()（MinGW 内联汇编 rdtsc）。TSC 频率由 rdtsc↔steady_clock 自旋校准。
// 防优化消除：每个被测操作包在 [[gnu::noinline]] 探针里，且分配结果/写回值通过
//   `void* volatile g_sink` 逃逸，阻止 GCC 把 malloc/free 对、placement 写回、new/delete
//   对识别为无副作用而整体删除（否则测出 0 cy）。循环本身因探针有可观察副作用而保留。
#include <new>
#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <chrono>

static inline uint64_t rdtsc() {
    uint64_t a, d;
    asm volatile("rdtsc" : "=a"(a), "=d"(d));
    return (d << 32) | a;
}

// 自旋校准 TSC：用 steady_clock 量 50ms 真实墙钟，比对 rdtsc 增量，得 GHz。
static double tsc_ghz() {
    using namespace std::chrono;
    auto t0 = steady_clock::now();
    uint64_t c0 = rdtsc();
    while (duration_cast<milliseconds>(steady_clock::now() - t0).count() < 50) {}
    auto t1 = steady_clock::now();
    uint64_t c1 = rdtsc();
    double sec = std::chrono::duration<double>(t1 - t0).count();
    return (double)(c1 - c0) / sec / 1e9; // GHz
}

struct Obj { long a, b, c, d; Obj(): a(1), b(2), c(3), d(4) {} };

// 逃逸汇：任何写入它的指针/值都被视为可观察副作用，阻止编译器删除分配/写回。
void* volatile g_sink = nullptr;

// 简易类专属池（指针碰撞分配器）
alignas(16) static char g_pool[2'000'000 * 16];
static char* g_pool_ptr = g_pool;
[[gnu::noinline]] void* pool_alloc() {
    void* p = g_pool_ptr;
    g_pool_ptr += 16;
    g_sink = p;          // 逃逸：防止指针碰撞被优化掉
    return p;
}

// --- 被测探针（noinline，防跨边界内联消除；结果经 g_sink 逃逸）---
[[gnu::noinline]] void probe_new_delete() {
    void* p = ::operator new(16);
    g_sink = p;          // 逃逸：保留 operator new
    ::operator delete(p);
    g_sink = p;          // 逃逸：保留 operator delete
}
[[gnu::noinline]] void probe_malloc_free() {
    void* p = std::malloc(16);
    g_sink = p;          // 逃逸：保留 malloc
    std::free(p);
    g_sink = p;          // 逃逸：保留 free
}
alignas(Obj) static char g_pb[sizeof(Obj)];
[[gnu::noinline]] void probe_placement() {
    Obj* o = new (g_pb) Obj();
    g_sink = (void*)o;   // 逃逸：保留构造写回
    long v = o->a;       // 强制读回，确保构造副作用真实发生
    o->~Obj();
    g_sink = (void*)(intptr_t)v;
}
[[gnu::noinline]] void probe_new_obj_delete() {
    Obj* o = new Obj();
    g_sink = (void*)o;   // 逃逸：保留 new+构造
    long v = o->a;       // 强制读回
    delete o;
    g_sink = (void*)(intptr_t)v;
}

template <typename F>
static double bench(const char* name, F f) {
    (void)name;
    const int N = 2'000'000;
    for (int i = 0; i < 100000; ++i) f();   // 预热
    uint64_t c0 = rdtsc();
    for (int i = 0; i < N; ++i) f();
    uint64_t c1 = rdtsc();
    return (double)(c1 - c0) / N;           // 每轮平均周期
}

int main() {
    double ghz = tsc_ghz();
    printf("TSC calibrated = %.4f GHz\n", ghz);
    auto cy_newdel = bench("op_new_delete", [](){ probe_new_delete(); });
    auto cy_malloc = bench("malloc_free",   [](){ probe_malloc_free(); });
    auto cy_place  = bench("placement",     [](){ probe_placement(); });
    auto cy_newobj = bench("new_obj_delete",[](){ probe_new_obj_delete(); });
    auto cy_pool   = bench("pool_alloc",    [](){ pool_alloc(); });

    auto ns = [ghz](double cy){ return cy / ghz; };
    printf("operator new + delete : %6.2f cy  %7.3f ns  (round-trip)\n", cy_newdel, ns(cy_newdel));
    printf("malloc + free         : %6.2f cy  %7.3f ns  (round-trip)\n", cy_malloc, ns(cy_malloc));
    printf("placement new+dtor    : %6.2f cy  %7.3f ns  (no alloc)\n",   cy_place,  ns(cy_place));
    printf("new Obj + delete      : %6.2f cy  %7.3f ns  (round-trip)\n", cy_newobj, ns(cy_newobj));
    printf("pool alloc (bump)     : %6.2f cy  %7.3f ns  (pointer bump)\n", cy_pool,  ns(cy_pool));
    return 0;
}
