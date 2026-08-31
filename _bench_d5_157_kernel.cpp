// _bench_d5_157_kernel.cpp — 编译器优化对内核算子的影响：-O0 vs -O2 (GCC 15.3.0 MinGW)
// 复现：分别用 `g++ -O0 -std=c++20` 与 `g++ -O2 -std=c++20` 编译并运行，取两者耗时比。
#include <iostream>
#include <vector>
#include <cmath>
#include <chrono>
#include <algorithm>

volatile int64_t g_sink = 0;

__attribute__((noinline)) double bench() {
    std::vector<double> t;
    const int R = 30;
    const int M = 2'000'000;
    std::vector<double> v(M);
    for (int i = 0; i < M; ++i) v[i] = (i % 1000) * 0.001;
    for (int r = 0; r < R; ++r) {
        auto a = std::chrono::steady_clock::now();
        double s = 0;
        for (int i = 0; i < M; ++i) s += std::sin(v[i]) * std::cos(v[i]);   // 受测内核
        auto b = std::chrono::steady_clock::now();
        g_sink += (int64_t)s;
        t.push_back(std::chrono::duration<double, std::milli>(b - a).count());
    }
    std::sort(t.begin(), t.end());
    return t[R / 2];
}

int main() {
    std::cout << "kernel (sin*cos x2M) : " << bench() << " ms\n";
    return 0;
}
