// _bench_d5_77_vector.cpp  — std::vector 内部效率：reserve 与 erase-remove (GCC 15.3.0)
#include <iostream>
#include <vector>
#include <algorithm>
#include <chrono>
#include <numeric>
#include <random>

static constexpr int N = 4'000'000;
volatile int64_t g_sink = 0;

__attribute__((noinline)) double bench_no_reserve() {
    std::vector<double> t;
    const int R = 5;
    for (int r = 0; r < R; ++r) {
        auto a = std::chrono::steady_clock::now();
        std::vector<int> v;
        for (int i = 0; i < N; ++i) v.push_back(i);
        auto b = std::chrono::steady_clock::now();
        g_sink += v.size();
        t.push_back(std::chrono::duration<double, std::milli>(b - a).count());
    }
    std::sort(t.begin(), t.end());
    return t[R / 2];
}
__attribute__((noinline)) double bench_reserve() {
    std::vector<double> t;
    const int R = 5;
    for (int r = 0; r < R; ++r) {
        auto a = std::chrono::steady_clock::now();
        std::vector<int> v;
        v.reserve(N);
        for (int i = 0; i < N; ++i) v.push_back(i);
        auto b = std::chrono::steady_clock::now();
        g_sink += v.size();
        t.push_back(std::chrono::duration<double, std::milli>(b - a).count());
    }
    std::sort(t.begin(), t.end());
    return t[R / 2];
}
__attribute__((noinline)) double bench_erase_remove() {
    std::vector<double> t;
    const int R = 5;
    std::mt19937 g(1);
    for (int r = 0; r < R; ++r) {
        std::vector<int> v(N);
        std::iota(v.begin(), v.end(), 0);
        std::shuffle(v.begin(), v.end(), g);  // 打乱以削弱预测
        auto a = std::chrono::steady_clock::now();
        v.erase(std::remove_if(v.begin(), v.end(), [](int x) { return x % 2 == 0; }), v.end());
        auto b = std::chrono::steady_clock::now();
        g_sink += v.size();
        t.push_back(std::chrono::duration<double, std::milli>(b - a).count());
    }
    std::sort(t.begin(), t.end());
    return t[R / 2];
}
int main() {
    double t_nr = bench_no_reserve();
    double t_r  = bench_reserve();
    double t_er = bench_erase_remove();
    std::cout << "push_back no-reserve : " << t_nr << " ms\n";
    std::cout << "push_back reserve    : " << t_r  << " ms  (" << t_nr / t_r << "x faster)\n";
    std::cout << "erase-remove (N even): " << t_er << " ms\n";
    return 0;
}
