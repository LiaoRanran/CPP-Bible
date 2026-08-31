// _bench_d5_07_format.cpp — C++20 std::format vs snprintf vs ostringstream (GCC 13.1.0 MinGW)
// 复现旗标：g++ -O2 -std=c++20 -Wall -Wextra
#include <iostream>
#include <string>
#include <format>
#include <sstream>
#include <cstdio>
#include <chrono>
#include <vector>
#include <algorithm>

volatile int64_t g_sink = 0;

__attribute__((noinline)) double bench_format() {
    std::vector<double> t; const int R = 20; const int N = 300'000;
    for (int r = 0; r < R; ++r) {
        auto a = std::chrono::steady_clock::now();
        for (int i = 0; i < N; ++i) {
            std::string s = std::format("id={} pi={:.4f}", i, 3.14159265);
            g_sink += (int64_t)s.size();
        }
        auto b = std::chrono::steady_clock::now();
        t.push_back(std::chrono::duration<double, std::milli>(b - a).count());
    }
    std::sort(t.begin(), t.end());
    return t[R / 2];
}
__attribute__((noinline)) double bench_snprintf() {
    std::vector<double> t; const int R = 20; const int N = 300'000;
    char buf[64];
    for (int r = 0; r < R; ++r) {
        auto a = std::chrono::steady_clock::now();
        for (int i = 0; i < N; ++i) {
            int n = std::snprintf(buf, sizeof(buf), "id=%d pi=%.4f", i, 3.14159265);
            g_sink += n;
        }
        auto b = std::chrono::steady_clock::now();
        t.push_back(std::chrono::duration<double, std::milli>(b - a).count());
    }
    std::sort(t.begin(), t.end());
    return t[R / 2];
}
__attribute__((noinline)) double bench_oss() {
    std::vector<double> t; const int R = 20; const int N = 300'000;
    for (int r = 0; r < R; ++r) {
        auto a = std::chrono::steady_clock::now();
        for (int i = 0; i < N; ++i) {
            std::ostringstream os;
            os << "id=" << i << " pi=" << 3.14159265;
            g_sink += (int64_t)os.str().size();
        }
        auto b = std::chrono::steady_clock::now();
        t.push_back(std::chrono::duration<double, std::milli>(b - a).count());
    }
    std::sort(t.begin(), t.end());
    return t[R / 2];
}
int main() {
    double f = bench_format();
    double s = bench_snprintf();
    double o = bench_oss();
    std::cout << "std::format   : " << f << " ms\n";
    std::cout << "snprintf      : " << s << " ms  (" << f / s << "x vs format)\n";
    std::cout << "ostringstream : " << o << " ms  (" << f / o << "x vs format)\n";
    return 0;
}
