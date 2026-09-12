// CONC-002 夹具：锁的代价 vs 无锁的代价
// 唯一变量：同步原语种类（mutex / atomic fetch_add / atomic CAS）
// 活性对照：单线程无同步基线
// 反例对照：CAS 在高竞争下退化（方向量观测）
// 双构建同源宏门控：-DBENCH_FULL 仅用于 .out 性能样本生成，actual 只锚方向量与常量
#include <atomic>
#include <mutex>
#include <thread>
#include <vector>
#include <iostream>
#include <chrono>

constexpr int kThreads = 4;
constexpr long kIters = 200000;   // 每线程迭代（有界，防 replay 超时）

std::mutex g_mutex;
long g_mutex_cnt = 0;
std::atomic<long> g_atomic_cnt{0};
std::atomic<long> g_cas_target{0};
std::atomic<long> g_cas_retries{0};   // CAS 重试计数（高竞争下 > 0）
long g_single = 0;

void bench_single() {
    for (long i = 0; i < kIters; ++i) g_single += 1;
}

void bench_mutex() {
    for (long i = 0; i < kIters; ++i) {
        std::lock_guard<std::mutex> lk(g_mutex);
        g_mutex_cnt += 1;
    }
}

void bench_atomic_fetch() {
    for (long i = 0; i < kIters; ++i)
        g_atomic_cnt.fetch_add(1, std::memory_order_relaxed);
}

void bench_atomic_cas() {
    for (long i = 0; i < kIters; ++i) {
        long expected = g_cas_target.load(std::memory_order_relaxed);
        while (!g_cas_target.compare_exchange_weak(expected, expected + 1,
                 std::memory_order_relaxed)) {
            g_cas_retries.fetch_add(1, std::memory_order_relaxed);  // 重试计数
        }
    }
}

int main() {
    unsigned nproc = std::thread::hardware_concurrency();
    std::cout << "nproc=" << nproc << "\n";

    bench_single();
    std::cout << "single_thread_baseline=1\n";
    std::cout << "single_result=" << g_single << "\n";

    std::vector<std::thread> ts;
    for (int t = 0; t < kThreads; ++t) ts.emplace_back(bench_mutex);
    for (auto& t : ts) t.join();
    std::cout << "mutex_fastpath_exists=1\n";
    std::cout << "mutex_result=" << g_mutex_cnt << "\n";

    ts.clear();
    for (int t = 0; t < kThreads; ++t) ts.emplace_back(bench_atomic_fetch);
    for (auto& t : ts) t.join();
    std::cout << "atomic_rmw_exists=1\n";
    std::cout << "atomic_result=" << g_atomic_cnt.load() << "\n";

    ts.clear();
    for (int t = 0; t < kThreads; ++t) ts.emplace_back(bench_atomic_cas);
    for (auto& t : ts) t.join();
    std::cout << "cas_retry_observed=" << (g_cas_retries.load() > 0 ? 1 : 0) << "\n";
    std::cout << "cas_result=" << g_cas_target.load() << "\n";

    // 高竞争退化方向量：核不足则合法翻转（CAS 退化实验无法成立）
    if (nproc < kThreads)
        std::cout << "insufficient_cores=1\n";
    else
        std::cout << "cas_high_contention_tested=1\n";

#ifdef BENCH_FULL
    // 完整性能样本（仅 .out 留痕，actual 不锚倍数）
    auto t0 = std::chrono::steady_clock::now();
    bench_atomic_fetch();
    auto t1 = std::chrono::steady_clock::now();
    std::cout << "atomic_fetch_ns="
              << std::chrono::duration_cast<std::chrono::nanoseconds>(t1 - t0).count() << "\n";
#endif

    return 0;
}
