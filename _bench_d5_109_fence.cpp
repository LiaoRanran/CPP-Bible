// _bench_d5_109_fence.cpp — ch109 内存栅栏：各类栅栏在 x86 上的真实开销
// g++ -O2 -std=c++23
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <vector>
#include <algorithm>
#include <atomic>

static double now_ms() {
    using namespace std::chrono;
    return duration<double, std::milli>(steady_clock::now().time_since_epoch()).count();
}
template <class F>
static double bench(const char* name, F&& f) {
    std::vector<double> t;
    for (int r = 0; r < 5; ++r) { double t0 = now_ms(); f(); t.push_back(now_ms() - t0); }
    std::sort(t.begin(), t.end());
    std::printf("%-44s %10.3f ms\n", name, t[2]);
    return t[2];
}
volatile std::uint64_t g_sink;
std::atomic<std::uint64_t> g_at{0};

int main() {
    constexpr std::uint64_t N = 100'000'000;

    // 基线：relaxed store（x86 = 普通 mov）
    bench("relaxed store x100M", [&] {
        for (std::uint64_t i = 0; i < N; ++i)
            g_at.store(i, std::memory_order_relaxed);
        g_sink = g_at.load(std::memory_order_relaxed);
    });
    // relaxed store + release fence（x86 上仅编译器屏障，零指令）
    bench("relaxed store + fence(release) x100M", [&] {
        for (std::uint64_t i = 0; i < N; ++i) {
            g_at.store(i, std::memory_order_relaxed);
            std::atomic_thread_fence(std::memory_order_release);
        }
        g_sink = g_at.load(std::memory_order_relaxed);
    });
    // relaxed load + acquire fence（同样零指令）
    bench("relaxed load + fence(acquire) x100M", [&] {
        std::uint64_t s = 0;
        for (std::uint64_t i = 0; i < N; ++i) {
            s += g_at.load(std::memory_order_relaxed);
            std::atomic_thread_fence(std::memory_order_acquire);
        }
        g_sink = s;
    });
    // relaxed store + seq_cst fence（x86 = mfence，全序化点）
    bench("relaxed store + fence(seq_cst) x100M", [&] {
        for (std::uint64_t i = 0; i < N; ++i) {
            g_at.store(i, std::memory_order_relaxed);
            std::atomic_thread_fence(std::memory_order_seq_cst);
        }
        g_sink = g_at.load(std::memory_order_relaxed);
    });
    // seq_cst store（x86 = xchg，通常比 mov+mfence 便宜）
    bench("seq_cst store x100M", [&] {
        for (std::uint64_t i = 0; i < N; ++i)
            g_at.store(i, std::memory_order_seq_cst);
        g_sink = g_at.load(std::memory_order_relaxed);
    });
    // release store（x86 = 普通 mov，与 relaxed 同指令）
    bench("release store x100M", [&] {
        for (std::uint64_t i = 0; i < N; ++i)
            g_at.store(i, std::memory_order_release);
        g_sink = g_at.load(std::memory_order_relaxed);
    });

    std::printf("sink=%llu\n", (unsigned long long)g_sink);
    return 0;
}
