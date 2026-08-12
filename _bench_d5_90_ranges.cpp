// _bench_d5_90_ranges.cpp  — C++20 ranges 抽象开销 (GCC 15.3.0)
// 对比：手写循环(基线) vs ranges::for_each vs views::filter|transform 管道（随机数据防闭式）
#include <iostream>
#include <vector>
#include <numeric>
#include <chrono>
#include <algorithm>
#include <random>
#include <ranges>

static constexpr int N = 5'000'000;
volatile int64_t g_sink = 0;

__attribute__((noinline)) int64_t manual(const std::vector<int>& v) {
    int64_t s = 0;
    for (int x : v)
        if (x % 2 == 0) s += x * 3;
    return s;
}
__attribute__((noinline)) int64_t ranges_pipe(const std::vector<int>& v) {
    int64_t s = 0;
    for (int x : v | std::views::filter([](int x) { return x % 2 == 0; }) |
                    std::views::transform([](int x) { return x * 3; }))
        s += x;
    return s;
}
__attribute__((noinline)) int64_t ranges_for_each(const std::vector<int>& v) {
    int64_t s = 0;
    std::ranges::for_each(v, [&](int x) {
        if (x % 2 == 0) s += x * 3;
    });
    return s;
}
int main() {
    std::vector<int> v(N);
    std::mt19937 rng(11);
    for (int& x : v) x = (int)rng();  // 随机数据，防闭式求值
    const int R = 5;
    auto med = [&](auto fn) -> double {
        std::vector<double> t;
        for (int r = 0; r < R; ++r) {
            auto a = std::chrono::steady_clock::now();
            int64_t s = fn();
            auto b = std::chrono::steady_clock::now();
            g_sink = s;
            t.push_back(std::chrono::duration<double, std::milli>(b - a).count());
        }
        std::sort(t.begin(), t.end());
        return t[R / 2];
    };
    double t_manual = med([&] { return manual(v); });
    double t_pipe  = med([&] { return ranges_pipe(v); });
    double t_fe    = med([&] { return ranges_for_each(v); });
    std::cout << "manual loop         : " << t_manual << " ms  (baseline)\n";
    std::cout << "ranges for_each     : " << t_fe   << " ms  (" << t_fe / t_manual   << "x)\n";
    std::cout << "ranges filter|trans : " << t_pipe << " ms  (" << t_pipe / t_manual << "x)\n";
    return 0;
}
