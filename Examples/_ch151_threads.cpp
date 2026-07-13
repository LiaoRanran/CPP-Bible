// ⑬ 多线程基准：用 N 个线程并行累加，计时含线程开销
// 见 Examples/_ch151_threads.cpp
#include <cstdio>
#include <chrono>
#include <thread>
#include <vector>

static void chunk(std::size_t from, std::size_t to, volatile long long* out) {
    long long s = 0;
    for (std::size_t i = from; i < to; ++i) s += i;
    *out = s;
}

int main() {
    const std::size_t N = 100'000'000;
    const unsigned T = 8;
    std::vector<std::thread> pool;
    std::vector<long long> res(T);

    auto t0 = std::chrono::steady_clock::now();
    std::size_t step = N / T;
    for (unsigned t = 0; t < T; ++t)
        pool.emplace_back(chunk, t * step, (t + 1) * step, &res[t]);
    for (auto& th : pool) th.join();
    auto t1 = std::chrono::steady_clock::now();

    long long total = 0; for (auto x : res) total += x;
    std::printf("threads: T=%u par_ms=%.3f total=%lld\n", T,
                std::chrono::duration<double, std::milli>(t1 - t0).count(), total);
    return 0;
}
