// ch43_cache_locality — 真实缓存层级延迟实测
// 编译: g++ -O2 -std=c++23 -m64 _ch43_cache_perf.cpp -o _ch43_cache_perf.exe
// 运行: _ch43_cache_perf.exe  (输出见 .out)
//
// 方法: 指针追逐 (pointer chasing)。在一个大小为 S 的指针数组上构造随机置换链表，
// 沿链表走 N 步，每步一次指针加载。若 S 超过某级缓存容量，则该级缓存未命中，
// 测得的每步延迟 ≈ 该级缓存命中/下一级缓存未命中 的访问延迟。
// 使用 RDTSC 计时 (本机 TSC 频率经 QueryPerformanceCounter 标定)。

#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <vector>
#include <random>
#include <algorithm>
#include <windows.h>

static inline uint64_t rdtsc() {
    uint64_t t;
    __asm__ __volatile__("rdtsc" : "=A"(t));
    return t;
}

// 标定 TSC 频率 (GHz)
static double tsc_ghz() {
    LARGE_INTEGER freq; QueryPerformanceFrequency(&freq);
    LARGE_INTEGER a; QueryPerformanceCounter(&a);
    uint64_t r0 = rdtsc();
    Sleep(100);
    LARGE_INTEGER b; QueryPerformanceCounter(&b);
    uint64_t r1 = rdtsc();
    double secs = (double)(b.QuadPart - a.QuadPart) / (double)freq.QuadPart;
    return (double)(r1 - r0) / secs / 1e9;  // GHz
}

// 指针追逐探针: 沿随机置换链表走 n 步，返回指针和防优化消除
[[gnu::noinline, gnu::noipa]]
static uint64_t chase(uintptr_t* head, size_t n) {
    uint64_t sum = 0;
    uintptr_t p = *head;
    for (size_t i = 0; i < n; ++i) {
        p = *(uintptr_t*)p;        // 加载下一项 (可能缓存未命中)
        sum += p;
    }
    return sum;
}

struct Result { double cyc; double ns; };

static Result measure(size_t bytes, double ghz, int repeats) {
    size_t N = bytes / sizeof(uintptr_t);
    std::vector<uintptr_t> arr(N);
    for (size_t i = 0; i < N; ++i) arr[i] = (uintptr_t)&arr[i];
    // 随机置换: arr[i] -> arr[perm[i]]
    std::vector<size_t> perm(N);
    for (size_t i = 0; i < N; ++i) perm[i] = i;
    std::mt19937_64 rng(0x9E3779B97F4A7C15ULL);
    std::shuffle(perm.begin(), perm.end(), rng);
    for (size_t i = 0; i < N; ++i) arr[i] = (uintptr_t)&arr[perm[i]];

    // 暖一遍 (把链表拉进缓存层级以便稳定测量? 不——我们要测的是随机访问延迟，
    // 暖一遍只warm了第一遍，循环本身每步随机，缓存状态由工作集大小决定)
    volatile uint64_t sink = 0;
    uint64_t best = ~0ULL;
    for (int r = 0; r < repeats; ++r) {
        uint64_t t0 = rdtsc();
        sink += chase((uintptr_t*)&arr[0], N);
        uint64_t t1 = rdtsc();
        uint64_t dt = t1 - t0;
        if (dt < best) best = dt;
    }
    if (sink == 0) printf("");  // 防 sink 被优化
    double per = (double)best / (double)N;
    return Result{ per, per / ghz };
}

int main() {
    double ghz = tsc_ghz();
    printf("TSC = %.3f GHz   (MinGW GCC 13.1.0 -O2, x86_64)\n", ghz);
    printf("%-10s %12s %14s %14s\n", "work_set", "nodes", "cyc/step", "ns/step");
    // L1d 命中 (~32KB): 16KB 工作集全部驻留 L1
    auto r1 = measure(16ULL * 1024, ghz, 50);
    printf("%-10s %12zu %14.2f %14.3f\n", "16KB(L1)", 16*1024/8, r1.cyc, r1.ns);
    // L2 命中 (~256KB): 超过 L1，驻留 L2
    auto r2 = measure(256ULL * 1024, ghz, 30);
    printf("%-10s %12zu %14.2f %14.3f\n", "256KB(L2)", 256*1024/8, r2.cyc, r2.ns);
    // L3 命中 (~8MB): 超过 L2，驻留 L3
    auto r3 = measure(8ULL * 1024 * 1024, ghz, 20);
    printf("%-10s %12zu %14.2f %14.3f\n", "8MB(L3)", 8*1024*1024/8, r3.cyc, r3.ns);
    // 主存 (~64MB): 超过 L3，走 DRAM (+ TLB 未命中)
    auto r4 = measure(64ULL * 1024 * 1024, ghz, 10);
    printf("%-10s %12zu %14.2f %14.3f\n", "64MB(DRAM)", 64ULL*1024*1024/8, r4.cyc, r4.ns);
    return 0;
}
