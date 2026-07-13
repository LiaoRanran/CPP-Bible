// ch110_lockfree — 真实锁/无锁开销实测 (uncontended, 单线程)
// 编译: g++ -O2 -std=c++23 -m64 _ch110_lockfree_perf.cpp -o _ch110_lockfree_perf.exe -lpthread
// 运行: _ch110_lockfree_perf.exe  (输出见 .out)
//
// 方法: RDTSC 计时。对三类同步原语各跑 N 次，减去等结构空循环开销得到单次延迟。
// uncontended 单线程延迟可干净复现；contended 多线延迟属平台相关，本基准不给出单一数字。

#include <atomic>
#include <mutex>
#include <cstdint>
#include <cstdio>
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

std::mutex g_mtx;
std::atomic<uint64_t> g_a{0};
void* volatile g_sink = nullptr;

[[gnu::noinline, gnu::noipa]]
static uint64_t probe_nop(size_t n) {
    uint64_t s = 0;
    for (size_t i = 0; i < n; ++i) s += i;
    return s;
}
[[gnu::noinline, gnu::noipa]]
static uint64_t probe_mutex(size_t n) {
    for (size_t i = 0; i < n; ++i) { g_mtx.lock(); g_mtx.unlock(); }
    return 0;
}
[[gnu::noinline, gnu::noipa]]
static uint64_t probe_cas(size_t n) {
    for (size_t i = 0; i < n; ++i) {
        uint64_t cur = g_a.load(std::memory_order_relaxed);
        g_a.compare_exchange_weak(cur, cur + 1, std::memory_order_relaxed);
    }
    return 0;
}
[[gnu::noinline, gnu::noipa]]
static uint64_t probe_fetch(size_t n) {
    for (size_t i = 0; i < n; ++i) {
        g_a.fetch_add(1, std::memory_order_relaxed);
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
    printf("TSC = %.3f GHz   (MinGW GCC 13.1.0 -O2, x86_64, uncontended single-thread)\n", ghz);
    const size_t N = 5'000'000;
    double nop   = bench(probe_nop,   N, 20);
    double mutex = bench(probe_mutex, N, 20);
    double cas   = bench(probe_cas,   N, 20);
    double fetch = bench(probe_fetch, N, 20);
    auto per = [&](double raw){ double cyc = raw - nop; return std::make_pair(cyc, cyc / ghz); };
    auto [mc, mns] = per(mutex);
    auto [cc, cns] = per(cas);
    auto [fc, fns] = per(fetch);
    printf("%-12s %10s %10s %12s\n", "op", "cyc/op", "ns/op", "raw(cyc)");
    printf("%-12s %10.2f %10.3f %12.2f\n", "mutex", mc, mns, mutex);
    printf("%-12s %10.2f %10.3f %12.2f\n", "CAS",   cc, cns, cas);
    printf("%-12s %10.2f %10.3f %12.2f\n", "fetch_add", fc, fns, fetch);
    return 0;
}
