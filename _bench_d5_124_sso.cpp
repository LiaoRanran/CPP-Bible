// _bench_d5_124_sso.cpp — libstdc++ std::string 短字符串优化(SSO)阈值：堆内 vs 堆外拷贝代价 (GCC 13.1.0 MinGW)
// 复现旗标：g++ -O2 -std=c++20 -Wall -Wextra
#include <iostream>
#include <string>
#include <chrono>
#include <vector>
#include <algorithm>
#include <cassert>
#include <cstdlib>

volatile int64_t g_sink = 0;
static long long g_allocs = 0;
void* operator new(std::size_t n) { g_allocs++; return std::malloc(n); }
void operator delete(void* p) noexcept { std::free(p); }
void operator delete(void* p, std::size_t) noexcept { std::free(p); }

__attribute__((noinline)) double bench_copy(const std::string& proto, int N) {
    std::vector<double> t; const int R = 10;
    for (int r = 0; r < R; ++r) {
        auto a = std::chrono::steady_clock::now();
        for (int i = 0; i < N; ++i) {
            std::string c = proto;          // 拷贝构造
            g_sink += (int64_t)c.size();
        }
        auto b = std::chrono::steady_clock::now();
        t.push_back(std::chrono::duration<double, std::micro>(b - a).count());
    }
    std::sort(t.begin(), t.end());
    return t[R / 2];
}

int main() {
    double t_short = bench_copy(std::string(15, 'x'), 2'000'000);  // libstdc++ SSO 容量内（≤15B）
    double t_long  = bench_copy(std::string(40, 'x'), 2'000'000);  // 超出 SSO → 走堆
    std::cout << "copy SSO(15B)  : " << t_short << " us\n";
    std::cout << "copy heap(40B) : " << t_long  << " us  (" << t_long / t_short << "x)\n";
    return 0;
}
