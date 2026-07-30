// D5 Wave 4 benchmark: ch92 chrono — "计时本身"的代价: 各时钟 now() 的单次成本
// 编译: g++ -O2 -std=c++23 -o bench.exe _bench_d5_92_chrono.cpp
// 设计要点: 热循环里随手插 now() 是常见的"观察者效应"事故源;
//   rdtsc 是用户态指令, steady/system_clock 在 Windows 上走 QPC/GetSystemTime 系 API。
#include <iostream>
#include <chrono>
#include <cstdint>
#if defined(__x86_64__) || defined(_M_X64)
#include <x86intrin.h>
#endif

static volatile long long g_esc = 0;

int main() {
    const int N = 20'000'000;
    auto ms = [](auto a, auto b) { return std::chrono::duration<double, std::milli>(b - a).count(); };

    long long s1 = 0, s2 = 0, s3 = 0, s4 = 0;

    auto t0 = std::chrono::steady_clock::now();
    for (int i = 0; i < N; ++i) s1 += std::chrono::steady_clock::now().time_since_epoch().count();
    auto t1 = std::chrono::steady_clock::now();
    for (int i = 0; i < N; ++i) s2 += std::chrono::system_clock::now().time_since_epoch().count();
    auto t2 = std::chrono::steady_clock::now();
    for (int i = 0; i < N; ++i) s3 += std::chrono::high_resolution_clock::now().time_since_epoch().count();
    auto t3 = std::chrono::steady_clock::now();
#if defined(__x86_64__) || defined(_M_X64)
    for (int i = 0; i < N; ++i) s4 += static_cast<long long>(__rdtsc());
#endif
    auto t4 = std::chrono::steady_clock::now();

    g_esc = s1 + s2 + s3 + s4;
    std::cout << "steady_clock_now_x20M  " << ms(t0, t1) << " ms\n";
    std::cout << "system_clock_now_x20M  " << ms(t1, t2) << " ms\n";
    std::cout << "highres_clock_now_x20M " << ms(t2, t3) << " ms\n";
    std::cout << "rdtsc_x20M             " << ms(t3, t4) << " ms\n";
    std::cout << "esc=" << g_esc << "\n";
    return 0;
}
