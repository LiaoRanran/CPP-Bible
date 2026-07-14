// UB-C5 false sharing：两个线程各自改独立变量，但变量落入同一缓存行 → 伪共享性能崩塌
// 真实基准（无需 sanitizer）：-O2 下对比「同缓存行」与「按缓存行对齐」两版耗时。
// 用 std::atomic<long>(relaxed) 强制真实内存流量，避免编译器把计数器留在寄存器而掩盖伪共享。
// 编译: g++ -std=c++23 -O2 -pthread -o fs ub_false_sharing.cpp
#include <atomic>
#include <chrono>
#include <cstdio>
#include <thread>

static const long N = 200'000'000L;

// ---- 版本 A：伪共享（x, y 同处一个 64B 缓存行）----
struct Packed { std::atomic<long> x{0}, y{0}; } g_packed;

// ---- 版本 B：按缓存行隔离（x, y 各占一行）----
struct Aligned { alignas(64) std::atomic<long> x{0}; alignas(64) std::atomic<long> y{0}; } g_aligned;

double bench_packed() {
    auto t0 = std::chrono::steady_clock::now();
    std::thread t1([&] { for (long i = 0; i < N; ++i) g_packed.x.fetch_add(1, std::memory_order_relaxed); });
    std::thread t2([&] { for (long i = 0; i < N; ++i) g_packed.y.fetch_add(1, std::memory_order_relaxed); });
    t1.join(); t2.join();
    auto t1end = std::chrono::steady_clock::now();
    return std::chrono::duration<double, std::milli>(t1end - t0).count();
}

double bench_aligned() {
    auto t0 = std::chrono::steady_clock::now();
    std::thread t1([&] { for (long i = 0; i < N; ++i) g_aligned.x.fetch_add(1, std::memory_order_relaxed); });
    std::thread t2([&] { for (long i = 0; i < N; ++i) g_aligned.y.fetch_add(1, std::memory_order_relaxed); });
    t1.join(); t2.join();
    auto t1end = std::chrono::steady_clock::now();
    return std::chrono::duration<double, std::milli>(t1end - t0).count();
}

int main() {
    double tp = bench_packed();
    double ta = bench_aligned();
    std::printf("Packed  (false sharing): %.1f ms\n", tp);
    std::printf("Aligned (no sharing)  : %.1f ms\n", ta);
    std::printf("slowdown x: %.2f\n", tp / ta);
    return 0;
}
