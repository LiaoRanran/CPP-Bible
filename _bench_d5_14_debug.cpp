// _bench_d5_14_debug.cpp — 调试构建代价：-O0 -g 相对 -O2 的运行时开销 (GCC 13.1.0 MinGW)
// 复现：分别用 `g++ -O0 -g` 与 `g++ -O2` 编译并运行，取两者耗时比。
// 复现旗标：g++ -O0 -g -std=c++20 -Wall -Wextra
#include <iostream>
#include <vector>
#include <random>
#include <chrono>
#include <algorithm>

volatile int64_t g_sink = 0;

__attribute__((noinline)) double bench() {
    std::vector<double> t;
    const int R = 30;
    const int M = 5'000'000;
    std::mt19937 g(1);
    for (int r = 0; r < R; ++r) {
        std::vector<int> v(M);
        for (int i = 0; i < M; ++i) v[i] = (int)g();
        auto a = std::chrono::steady_clock::now();
        long long s = 0;
        for (int x : v) s += x;           // 受测工作负载（顺序求和，编译器无法常量折叠）
        auto b = std::chrono::steady_clock::now();
        g_sink += s;
        t.push_back(std::chrono::duration<double, std::milli>(b - a).count());
    }
    std::sort(t.begin(), t.end());
    return t[R / 2];
}

int main() {
    std::cout << "workload (sum " << 5'000'000 << " random int) : " << bench() << " ms\n";
    return 0;
}
