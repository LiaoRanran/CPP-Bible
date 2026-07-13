// ⑱ 与 CI 集成：基准回归自测（退出码非零 = 性能退化超阈值）
// 见 Examples/_ch151_ci_harness.cpp
#include <cstdio>
#include <chrono>

static double bench_once() {
    auto t0 = std::chrono::steady_clock::now();
    volatile long long s = 0;
    for (int i = 0; i < 50'000'000; ++i) s += i;
    auto t1 = std::chrono::steady_clock::now();
    return std::chrono::duration<double, std::milli>(t1 - t0).count();
}

int main() {
    const double BASELINE_MS = 120.0;   // 由历史基线写入 CI 配置
    const double REGRESS_LIMIT = 1.20;  // 允许 +20% 噪声
    double ms = bench_once();
    std::printf("ci_bench: current=%.3f baseline=%.3f limit=%.3f\n",
                ms, BASELINE_MS, BASELINE_MS * REGRESS_LIMIT);
    if (ms > BASELINE_MS * REGRESS_LIMIT) {
        std::printf("CI FAIL: performance regression detected\n");
        return 1;
    }
    std::printf("CI PASS\n");
    return 0;
}
