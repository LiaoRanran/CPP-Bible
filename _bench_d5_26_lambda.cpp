// _bench_d5_26_lambda.cpp  — 捕获 lambda 进 std::function 的类型擦除开销 (GCC 15.3.0)
// 对比：模板直传捕获 lambda(零开销, 内联) vs std::function 包装捕获 lambda(类型擦除+可能堆分配)
#include <functional>
#include <iostream>
#include <vector>
#include <chrono>
#include <numeric>
#include <random>
#include <algorithm>

static constexpr int N = 10'000'000;
volatile int64_t g_sink = 0;

template <class F>
__attribute__((noinline)) int64_t via_template(const std::vector<int>& v, F f) {
    int64_t s = 0;
    for (int x : v) f(s, x);
    return s;
}
__attribute__((noinline)) int64_t via_std_function(const std::vector<int>& v, std::function<void(int64_t&, int)> f) {
    int64_t s = 0;
    for (int x : v) f(s, x);
    return s;
}
int main() {
    std::vector<int> v(N);
    std::mt19937 rng(7);
    for (int& x : v) x = (int)rng();  // 随机数据，防闭式求值
    const int R = 5;
    int k = 3;  // 被 lambda 捕获的变量
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
    double t_tmpl = med([&] { return via_template(v, [k](int64_t& s, int x) { s += x * k + 1; }); });
    double t_sf   = med([&] { return via_std_function(v, [k](int64_t& s, int x) { s += x * k + 1; }); });
    std::cout << "template + 捕获lambda : " << t_tmpl << " ms  (baseline, 内联)\n";
    std::cout << "std::function + 捕获  : " << t_sf   << " ms  (" << t_sf / t_tmpl << "x)\n";
    return (int)g_sink;
}
