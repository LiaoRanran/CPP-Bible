// _bench_d5_110_lockfree.cpp  — 无锁三档：wait-free > lock-free > lock-based (GCC 15.3.0)
// 对比：per-thread 局部计数(无共享写) / atomic fetch_add / std::mutex，多线程累加 N
#include <iostream>
#include <vector>
#include <thread>
#include <atomic>
#include <mutex>
#include <numeric>
#include <chrono>

static constexpr int N = 2'000'000;
volatile int64_t g_sink = 0;

void bench_mutex(int nt) {
    std::mutex m;
    int64_t c = 0;
    std::vector<std::thread> ts;
    auto a = std::chrono::steady_clock::now();
    for (int t = 0; t < nt; ++t)
        ts.emplace_back([&] {
            int64_t per = N / nt;
            for (int64_t i = 0; i < per; ++i) {
                std::lock_guard<std::mutex> lk(m);
                ++c;
            }
        });
    for (auto& t : ts) t.join();
    auto b = std::chrono::steady_clock::now();
    g_sink += c;
    std::cout << "mutex(lock-based) " << nt << "T: "
              << std::chrono::duration<double, std::milli>(b - a).count() << " ms\n";
}
void bench_atomic(int nt) {
    std::atomic<int64_t> c{0};
    std::vector<std::thread> ts;
    auto a = std::chrono::steady_clock::now();
    for (int t = 0; t < nt; ++t)
        ts.emplace_back([&c, nt] {
            int64_t per = N / nt;
            for (int64_t i = 0; i < per; ++i) c.fetch_add(1, std::memory_order_relaxed);
        });
    for (auto& t : ts) t.join();
    auto b = std::chrono::steady_clock::now();
    g_sink += c.load();
    std::cout << "atomic(lock-free)   " << nt << "T: "
              << std::chrono::duration<double, std::milli>(b - a).count() << " ms\n";
}
void bench_perthread(int nt) {
    std::vector<int64_t> local(nt, 0);
    std::vector<std::thread> ts;
    auto a = std::chrono::steady_clock::now();
    for (int t = 0; t < nt; ++t)
        ts.emplace_back([&, t] {
            int64_t per = N / nt;
            for (int64_t i = 0; i < per; ++i) local[t]++;
        });
    for (auto& t : ts) t.join();
    int64_t tot = std::accumulate(local.begin(), local.end(), int64_t{0});
    auto b = std::chrono::steady_clock::now();
    g_sink += tot;
    std::cout << "per-thread(wait-free) " << nt << "T: "
              << std::chrono::duration<double, std::milli>(b - a).count() << " ms\n";
}
int main() {
    for (int nt : {1, 4, 8}) {
        bench_perthread(nt);
        bench_atomic(nt);
        bench_mutex(nt);
    }
    return (int)g_sink;
}
