// [redacted]
// [redacted]
//
// [redacted]
// [redacted]
// [redacted]
// 由 stdout 断言（非确定值会让 replay 双平台失配）。
//
// -DBENCH_FULL：额外打印诊断行（scenario= / kIters=），不影响 run_match_keys。

#include <atomic>
#include <cstdio>
#include <chrono>
#include <thread>
#include <vector>

static const int kIters = 100000;

// [redacted]
static int g_shared = 0;
// [redacted]
static std::atomic<int> g_atomic{0};

// [redacted]
// __attribute__((noinline))：防止 -O2 把负载内联进 main 而让其在工件中"消失"
// [redacted]
__attribute__((noinline)) void bench_single() {
    int local = 0;
    for (int i = 0; i < kIters; ++i) local += 1;
    std::printf("single_total=%d\n", local);
}

// [redacted]
// [redacted]
__attribute__((noinline)) void bench_race() {
    g_shared = 0;
    std::thread a([]() {
        for (int i = 0; i < kIters; ++i) g_shared += 1;
    });
    std::thread b([]() {
        std::this_thread::sleep_for(std::chrono::milliseconds(1));
        for (int i = 0; i < kIters; ++i) g_shared += 1;
    });
    a.join();
    b.join();
    // [redacted]
    std::printf("race_ops_total=%d\n", 2 * kIters);
}

// [redacted]
__attribute__((noinline)) void bench_safe() {
    g_atomic.store(0, std::memory_order_relaxed);
    std::thread a([]() {
        for (int i = 0; i < kIters; ++i)
            g_atomic.fetch_add(1, std::memory_order_relaxed);
    });
    std::thread b([]() {
        for (int i = 0; i < kIters; ++i)
            g_atomic.fetch_add(1, std::memory_order_relaxed);
    });
    a.join();
    b.join();
    std::printf("safe_ops_total=%d\n", 2 * kIters);
    std::printf("safe_final=%d\n", g_atomic.load());   // 确定性 = 2*kIters
}

int main() {
    bench_single();
    bench_race();
    bench_safe();
#ifdef BENCH_FULL
    std::printf("scenario=single|race|safe\n");
    std::printf("kIters=%d\n", kIters);
#endif
    return 0;
}
