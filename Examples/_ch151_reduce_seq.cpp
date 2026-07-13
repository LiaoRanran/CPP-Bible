// ⑫'' std::accumulate vs std::reduce（顺序）对照
// 见 Examples/_ch151_reduce_seq.cpp
#include <cstdio>
#include <vector>
#include <chrono>
#include <numeric>

int main() {
    const std::size_t N = 30'000'000;
    std::vector<double> v(N);
    for (std::size_t i = 0; i < N; ++i) v[i] = (double)(i % 1000) + 1.0;

    auto t0 = std::chrono::steady_clock::now();
    volatile double a = std::accumulate(v.begin(), v.end(), 0.0);
    (void)a;
    auto t1 = std::chrono::steady_clock::now();

    auto t2 = std::chrono::steady_clock::now();
    volatile double r = std::reduce(v.begin(), v.end(), 0.0);
    (void)r;
    auto t3 = std::chrono::steady_clock::now();

    std::printf("accumulate: ms=%.3f  reduce: ms=%.3f\n",
                std::chrono::duration<double, std::milli>(t1 - t0).count(),
                std::chrono::duration<double, std::milli>(t3 - t2).count());
    return 0;
}
