// _bench_d5_152_clock.cpp — 性能测量学：steady_clock 分辨率与单次计时开销 (GCC 13.1.0 MinGW)
// 复现旗标：g++ -O2 -std=c++20 -Wall -Wextra
// 说明：分辨率 = 连续两次读取之间能观测到的最小非零间隔；它决定了"可测量的最小耗时"。
//       单次计时对 = 一次 now() 起点 + 一次 now() 终点，其固有开销≈2×分辨率。
#include <iostream>
#include <chrono>
#include <vector>
#include <algorithm>

volatile int64_t g_sink = 0;

__attribute__((noinline)) double resolution_ns() {
    using namespace std::chrono;
    const int T = 3'000'000;
    auto prev = steady_clock::now();
    long long min_delta = 1'000'000'000;
    for (int i = 0; i < T; ++i) {
        auto cur = steady_clock::now();
        long long d = duration_cast<nanoseconds>(cur - prev).count();
        if (d > 0 && d < min_delta) min_delta = d;
        prev = cur;
        g_sink += d & 1;
    }
    return (double)min_delta;
}

__attribute__((noinline)) double pair_overhead_ns() {
    using namespace std::chrono;
    const int N = 50'000'000;
    std::vector<double> t;
    const int R = 5;
    for (int r = 0; r < R; ++r) {
        auto a = steady_clock::now();
        for (int i = 0; i < N; ++i) {
            auto t0 = steady_clock::now();
            auto t1 = steady_clock::now();
            g_sink += (int64_t)duration_cast<nanoseconds>(t1 - t0).count() & 1;
        }
        auto b = steady_clock::now();
        t.push_back(std::chrono::duration<double, std::nano>(b - a).count() / N);
    }
    std::sort(t.begin(), t.end());
    return t[R / 2];
}

int main() {
    std::cout << "steady_clock 分辨率       : " << resolution_ns() << " ns\n";
    std::cout << "单次计时对开销 (~2x 分辨率) : " << pair_overhead_ns() << " ns/call-pair\n";
    return 0;
}
