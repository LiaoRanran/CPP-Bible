// D5 Wave 3 benchmark: ch93 thread/future/async — std::async 每调用开销 vs 线程复用 vs deferred
// 编译: g++ -O2 -std=c++23 -pthread -o bench.exe _bench_d5_93_async.cpp
// 目的: 量化 每次 std::async(launch::async) 都建线程+promise 的开销；预建线程池复用远快.
#include <iostream>
#include <chrono>
#include <vector>
#include <thread>
#include <future>
#include <cstdint>

static volatile long long g_esc = 0;

template <class F>
double bench(const char* name, F f, int rounds = 5) {
    double best = 1e18;
    for (int r = 0; r < rounds; ++r) {
        auto t0 = std::chrono::steady_clock::now();
        long long res = f();
        auto t1 = std::chrono::steady_clock::now();
        g_esc += res;
        double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
        if (ms < best) best = ms;
    }
    std::cout << name << ": " << best << " ms\n";
    return best;
}

int trivial(int x) { int s = 0; for (int i = 0; i < 100; ++i) s += x + i; return s; }

int main() {
    const int N = 10'000;
    const int BATCH = 256;

    bench("async_percall", [&] {
        int64_t sa = 0;
        for (int b = 0; b < N; b += BATCH) {
            std::vector<std::future<int64_t>> futs;
            futs.reserve(BATCH);
            int end = (b + BATCH < N) ? b + BATCH : N;
            for (int i = b; i < end; ++i)
                futs.push_back(std::async(std::launch::async, [i] {
                    int64_t s = 0;
                    for (int k = 0; k < 100; ++k) s += trivial(i + k);
                    return s;
                }));
            for (auto& f : futs) sa += f.get();
        }
        return sa;
    });

    const int K = 16;
    bench("thread_reuse", [&] {
        std::vector<std::thread> ths;
        std::vector<int64_t> acc(K, 0);
        for (int t = 0; t < K; ++t) {
            ths.emplace_back([&, t] {
                int64_t s = 0;
                for (int i = t; i < N; i += K)
                    for (int k = 0; k < 100; ++k) s += trivial(i + k);
                acc[t] = s;
            });
        }
        for (auto& th : ths) th.join();
        int64_t sp = 0;
        for (auto v : acc) sp += v;
        return sp;
    });

    bench("deferred", [&] {
        int64_t sd = 0;
        for (int b = 0; b < N; b += BATCH) {
            std::vector<std::future<int64_t>> futs;
            futs.reserve(BATCH);
            int end = (b + BATCH < N) ? b + BATCH : N;
            for (int i = b; i < end; ++i)
                futs.push_back(std::async(std::launch::deferred, [i] {
                    int64_t s = 0;
                    for (int k = 0; k < 100; ++k) s += trivial(i + k);
                    return s;
                }));
            for (auto& f : futs) sd += f.get();
        }
        return sd;
    });

    std::cout << "esc=" << g_esc << "\n";
    return 0;
}
