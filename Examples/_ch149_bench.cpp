// 见 Examples/_ch149_bench.cpp
// ⑭ 性能基准：统计耗时，作为性能回归门禁基线
#include <cstdio>
#include <chrono>
long fib(int n) { return n < 2 ? n : fib(n-1) + fib(n-2); }
int main() {
    auto t0 = std::chrono::steady_clock::now();
    volatile long r = fib(35);
    auto t1 = std::chrono::steady_clock::now();
    double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
    std::printf("fib(35)=%ld time=%.2f ms\n", r, ms);
    return 0;
}
