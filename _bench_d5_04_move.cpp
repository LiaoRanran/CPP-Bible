// _bench_d5_04_move.cpp — C++11 移动语义：拷贝构造 vs 移动构造的代价 (GCC 13.1.0 MinGW)
// 复现旗标：g++ -O2 -std=c++20 -Wall -Wextra
#include <iostream>
#include <vector>
#include <string>
#include <chrono>
#include <algorithm>

static constexpr int N = 200'000;   // 字符串个数
static constexpr int L = 64;         // 每个字符串长度
volatile int64_t g_sink = 0;

__attribute__((noinline)) double bench_copy() {
    std::vector<double> t;
    const int R = 5;
    for (int r = 0; r < R; ++r) {
        std::vector<std::string> src;
        for (int i = 0; i < N; ++i) src.emplace_back(L, char('a' + (i % 26)));
        auto a = std::chrono::steady_clock::now();
        std::vector<std::string> dst = src;        // 拷贝构造：深拷贝 N 个字符串
        auto b = std::chrono::steady_clock::now();
        g_sink += dst.size();
        t.push_back(std::chrono::duration<double, std::micro>(b - a).count());
    }
    std::sort(t.begin(), t.end());
    return t[R / 2];
}

__attribute__((noinline)) double bench_move() {
    std::vector<double> t;
    const int R = 5;
    for (int r = 0; r < R; ++r) {
        std::vector<std::string> src;
        for (int i = 0; i < N; ++i) src.emplace_back(L, char('a' + (i % 26)));
        auto a = std::chrono::steady_clock::now();
        std::vector<std::string> dst = std::move(src);   // 移动构造：仅搬 3 个指针
        auto b = std::chrono::steady_clock::now();
        g_sink += dst.size();
        t.push_back(std::chrono::duration<double, std::micro>(b - a).count());
    }
    std::sort(t.begin(), t.end());
    return t[R / 2];
}

int main() {
    double t_c = bench_copy();
    double t_m = bench_move();
    std::cout << "copy construct (N=" << N << ", L=" << L << ") : " << t_c << " us\n";
    std::cout << "move construct                   : " << t_m << " us  (" << t_c / t_m << "x faster)\n";
    return 0;
}
