// _bench_d5_107_atomic.cpp  — 原子操作 vs 互斥锁 (GCC 15.3.0)
// 对比：atomic fetch_add(relaxed) vs std::mutex 保护计数，单/多线程
#include <iostream>
#include <vector>
#include <thread>
#include <atomic>
#include <mutex>
#include <chrono>

static constexpr int N = 2'000'000;
volatile int64_t g_sink = 0;

void bench_atomic_relaxed(int nthreads) {
    std::atomic<int64_t> c{0};
    std::vector<std::thread> ts;
    auto a = std::chrono::steady_clock::now();
    for (int t = 0; t < nthreads; ++t)
        ts.emplace_back([&c, nthreads] {
            int64_t per = N / nthreads;
            for (int64_t i = 0; i < per; ++i) c.fetch_add(1, std::memory_order_relaxed);
        });
    for (auto& t : ts) t.join();
    auto b = std::chrono::steady_clock::now();
    g_sink += c.load();
    std::cout << "atomic relaxed " << nthreads << "T: "
              << std::chrono::duration<double, std::milli>(b - a).count()
              << " ms (final=" << c.load() << ")\n";
}
void bench_mutex(int nthreads) {
    std::mutex m;
    int64_t c = 0;
    std::vector<std::thread> ts;
    auto a = std::chrono::steady_clock::now();
    for (int t = 0; t < nthreads; ++t)
        ts.emplace_back([&] {
            int64_t per = N / nthreads;
            for (int64_t i = 0; i < per; ++i) {
                std::lock_guard<std::mutex> lk(m);
                ++c;
            }
        });
    for (auto& t : ts) t.join();
    auto b = std::chrono::steady_clock::now();
    g_sink += c;
    std::cout << "mutex         " << nthreads << "T: "
              << std::chrono::duration<double, std::milli>(b - a).count()
              << " ms (final=" << c << ")\n";
}
int main() {
    for (int nt : {1, 4, 8}) {
        bench_atomic_relaxed(nt);
        bench_mutex(nt);
    }
    return (int)g_sink;
}
