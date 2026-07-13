// ⑪ 真实对比：标量累积（loop-carried 依赖长）vs 多累加器（缩短依赖链）
// 编译计时：g++ -std=c++23 -O2 _ch15_scalar_vs_accum.cpp -o _ch15_scalar_vs_accum
// 取汇编：  g++ -std=c++23 -O2 -S -masm=intel _ch15_scalar_vs_accum.cpp -o _ch15_scalar_vs_accum.asm
#include <vector>
#include <numeric>
#include <chrono>
#include <cstdio>

// 朴素标量累加：单累加器，依赖链长度 = N
long scalar_sum(const long* a, long n) {
    long s = 0;
    for (long i = 0; i < n; ++i) s += a[i];
    return s;
}

// 多累加器：4 条独立依赖链，ILP 更高（向量化雏形）
long four_acc_sum(const long* a, long n) {
    long s0 = 0, s1 = 0, s2 = 0, s3 = 0;
    long i = 0;
    for (; i + 4 <= n; i += 4) {
        s0 += a[i];
        s1 += a[i + 1];
        s2 += a[i + 2];
        s3 += a[i + 3];
    }
    for (; i < n; ++i) s0 += a[i];
    return s0 + s1 + s2 + s3;
}

int main() {
    const long N = 50'000'000;
    std::vector<long> a(N);
    for (long i = 0; i < N; ++i) a[i] = i % 97;

    volatile long sink = 0; (void)sink;

    auto t0 = std::chrono::steady_clock::now();
    long r1 = scalar_sum(a.data(), N);
    auto t1 = std::chrono::steady_clock::now();
    long r2 = four_acc_sum(a.data(), N);
    auto t2 = std::chrono::steady_clock::now();

    double ms1 = std::chrono::duration<double, std::milli>(t1 - t0).count();
    double ms2 = std::chrono::duration<double, std::milli>(t2 - t1).count();
    std::printf("scalar_sum  : %8.2f ms  (result=%ld)\n", ms1, r1);
    std::printf("four_acc_sum: %8.2f ms  (result=%ld)\n", ms2, r2);
    return 0;
}
