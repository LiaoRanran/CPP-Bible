// C17 易错点2：被测函数太短，时钟开销占比过高
#include <iostream>
#include <chrono>
int main() {
    // 单次 work 可能 < 10ns，而 steady_clock::now() 自身 ~25ns
    // → 测量误差 >> 信号。应把 work 放循环里测整体再除次数。
    const int M = 100000;
    long long acc = 0;
    auto t0 = std::chrono::steady_clock::now();
    for (int i = 0; i < M; ++i) acc += i & 7;       // 极轻量操作
    auto t1 = std::chrono::steady_clock::now();
    volatile long long sink = acc;
    double per = std::chrono::duration_cast<std::chrono::nanoseconds>(t1 - t0).count() / double(M);
    std::cout << "per-op ~" << per << " ns (sink=" << sink << ")\n";
    return 0;
}