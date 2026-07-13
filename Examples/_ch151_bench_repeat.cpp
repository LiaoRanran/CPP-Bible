// ⑯' 重复循环：用大 N 摊薄单次时钟开销，而非单次计时
// 见 Examples/_ch151_bench_repeat.cpp
#include <cstdio>
#include <chrono>
#include <vector>

int main() {
    const int N = 200'000'000;
    volatile long long s = 0;
    auto t0 = std::chrono::steady_clock::now();
    for (int i = 0; i < N; ++i) s += i;     // 单次计时不可靠，大循环摊薄
    auto t1 = std::chrono::steady_clock::now();
    double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
    std::printf("repeat: total_ms=%.3f per_iter_ns=%.4f s=%lld\n",
                ms, ms * 1e6 / N, (long long)s);
    return 0;
}
