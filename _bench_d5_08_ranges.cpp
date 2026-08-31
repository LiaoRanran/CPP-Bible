// _bench_d5_08_ranges.cpp — C++20 ranges 抽象代价：views::filter 惰性管线 vs 手写循环 (GCC 13.1.0 MinGW)
// 复现旗标：g++ -O2 -std=c++20 -Wall -Wextra
#include <iostream>
#include <vector>
#include <numeric>
#include <ranges>
#include <chrono>
#include <algorithm>

volatile int64_t g_sink = 0;

__attribute__((noinline)) double bench_manual() {
    std::vector<double> t; const int R = 30; const int M = 5'000'000;
    std::vector<int> v(M);
    std::iota(v.begin(), v.end(), 0);
    for (int r = 0; r < R; ++r) {
        auto a = std::chrono::steady_clock::now();
        long long s = 0;
        for (int x : v) if (x % 2 == 0) s += x;   // 手写过滤 + 求和
        auto b = std::chrono::steady_clock::now();
        g_sink += s;
        t.push_back(std::chrono::duration<double, std::milli>(b - a).count());
    }
    std::sort(t.begin(), t.end());
    return t[R / 2];
}
__attribute__((noinline)) double bench_ranges() {
    std::vector<double> t; const int R = 30; const int M = 5'000'000;
    std::vector<int> v(M);
    std::iota(v.begin(), v.end(), 0);
    for (int r = 0; r < R; ++r) {
        auto a = std::chrono::steady_clock::now();
        auto even = v | std::views::filter([](int x) { return x % 2 == 0; });
        long long s = 0;
        for (int x : even) s += x;                // 惰性视图迭代
        auto b = std::chrono::steady_clock::now();
        g_sink += s;
        t.push_back(std::chrono::duration<double, std::milli>(b - a).count());
    }
    std::sort(t.begin(), t.end());
    return t[R / 2];
}
int main() {
    double m = bench_manual();
    double g = bench_ranges();
    std::cout << "manual loop   : " << m << " ms\n";
    std::cout << "ranges filter : " << g << " ms  (" << g / m << "x vs manual)\n";
    return 0;
}
