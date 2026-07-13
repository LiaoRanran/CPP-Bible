// ⑪' 朴素基准陷阱：循环结果未消费时可能被整体消除（此处保留消费以真实计时）
#include <cstdio>
#include <chrono>
int main() {
    const int N = 1'000'000;
    long long total = 0;  // 消费累加结果，避免被 DCE
    auto t0 = std::chrono::steady_clock::now();
    for (int i = 0; i < N; ++i) total += i;
    auto t1 = std::chrono::steady_clock::now();
    volatile long long sink = total; (void)sink;
    double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
    std::printf("bench-naive: sum 0..%d = %lld in %.3f ms\n", N, (long long)total, ms);
    return 0;
}
