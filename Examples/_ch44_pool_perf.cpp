// ch44_memory_pool — bump / freelist / malloc 单次分配延迟实测
// 编译: g++ -O2 -std=c++23 -m64 _ch44_pool_perf.cpp -o _ch44_pool_perf.exe
// 运行: _ch44_pool_perf.exe  (输出见 .out)
//
// 方法: RDTSC 计时。每类分配器跑 N 次，减去等结构空循环开销得到单次分配延迟。
// bump / freelist 为单线程无锁版（仅测指针运算本身）；malloc 为本机 glibc(ptmalloc) 等价。
// tcmalloc/jemalloc 本机未安装，保留量级 + 文献来源。

#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstddef>
#include <vector>
#include <windows.h>

static inline uint64_t rdtsc() {
    uint64_t t;
    __asm__ __volatile__("rdtsc" : "=A"(t));
    return t;
}
static double tsc_ghz() {
    LARGE_INTEGER freq; QueryPerformanceFrequency(&freq);
    LARGE_INTEGER a; QueryPerformanceCounter(&a);
    uint64_t r0 = rdtsc();
    Sleep(100);
    LARGE_INTEGER b; QueryPerformanceCounter(&b);
    uint64_t r1 = rdtsc();
    double secs = (double)(b.QuadPart - a.QuadPart) / (double)freq.QuadPart;
    return (double)(r1 - r0) / secs / 1e9;
}

// bump allocator（不释放）
struct Bump { char* base; char* cur; size_t cap; };
static Bump g_bump;
// freelist（定长，单线程无锁 pop/push）
static void* g_fl_head = nullptr;
static void* g_fl_head0 = nullptr;   // 每次测量重置用的原始头
void* volatile g_sink = nullptr;

[[gnu::noinline, gnu::noipa]]
static uint64_t probe_nop(size_t n) {
    uint64_t s = 0;
    for (size_t i = 0; i < n; ++i) s += i;
    return s;
}
[[gnu::noinline, gnu::noipa]]
static uint64_t probe_bump(size_t n) {
    char* p = g_bump.base;            // 每次测量从 base 重新开始
    for (size_t i = 0; i < n; ++i) {
        void* r = p;                  // 模拟"返回当前指针"
        p += 16;                      // bump: 仅移动指针
        g_sink = r;                   // 防优化消除
    }
    return 0;
}
[[gnu::noinline, gnu::noipa]]
static uint64_t probe_freelist(size_t n) {
    void* h = g_fl_head0;            // 每次测量从原始头重新开始
    for (size_t i = 0; i < n; ++i) {
        void* p = h;
        h = *(void**)h;          // 依赖链: 取下一个
        g_sink = p;
    }
    return 0;
}
[[gnu::noinline, gnu::noipa]]
static uint64_t probe_malloc(size_t n) {
    for (size_t i = 0; i < n; ++i) {
        void* p = malloc(16);
        g_sink = p;              // 防优化消除
        free(p);
    }
    return 0;
}

static double bench(uint64_t (*fn)(size_t), size_t n, int reps) {
    uint64_t best = ~0ULL;
    for (int r = 0; r < reps; ++r) {
        uint64_t t0 = rdtsc();
        g_sink = (void*)fn(n);
        uint64_t t1 = rdtsc();
        uint64_t dt = t1 - t0;
        if (dt < best) best = dt;
    }
    return (double)best / (double)n;
}

int main() {
    double ghz = tsc_ghz();
    printf("TSC = %.3f GHz   (MinGW GCC 13.1.0 -O2, x86_64)\n", ghz);
    // 准备 bump 缓冲区 + freelist 节点链
    const size_t N = 4'000'000;
    // bump 缓冲区
    g_bump.base = (char*)malloc(N * 16 + 64);
    g_bump.cur = g_bump.base;
    g_bump.cap = N * 16;
    // freelist：单一大缓冲内构造 N 个 16B 节点链（避免 4M 次 malloc）
    char* pool = (char*)malloc(N * 16);
    for (size_t i = 0; i < N; ++i) {
        void* nxt = (i + 1 < N) ? (pool + (i + 1) * 16) : nullptr;
        *(void**)(pool + i * 16) = nxt;
    }
    g_fl_head = pool;
    g_fl_head0 = pool;

    double nop   = bench(probe_nop,      N, 20);
    double bump  = bench(probe_bump,     N, 20);
    double fl    = bench(probe_freelist,  N, 20);
    double mall  = bench(probe_malloc,    N, 20);
    auto per = [&](double raw){ double cyc = raw - nop; return std::make_pair(cyc, cyc / ghz); };
    auto [bc, bns] = per(bump);
    auto [fc, fns] = per(fl);
    auto [mc, mns] = per(mall);
    printf("%-14s %10s %10s %12s\n", "alloc", "cyc/op", "ns/op", "raw(cyc)");
    printf("%-14s %10.2f %10.3f %12.2f\n", "bump",       bc, bns, bump);
    printf("%-14s %10.2f %10.3f %12.2f\n", "freelist",   fc, fns, fl);
    printf("%-14s %10.2f %10.3f %12.2f\n", "malloc",     mc, mns, mall);
    return 0;
}
