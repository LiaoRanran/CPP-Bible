// ⑤ 预热与稳定：JIT/缓存/分支预测需热身，丢弃首批样本
// 见 Examples/_ch151_warmup.cpp
#include <cstdio>
#include <chrono>
#include <vector>
#include <numeric>

static double work(const std::vector<double>& v) {
    double s = 0;
    for (auto x : v) s += x * 1.0000001;
    return s;
}

int main() {
    const int WARMUP = 5, TRIALS = 10;
    const std::size_t N = 5'000'000;
    std::vector<double> v(N);
    std::iota(v.begin(), v.end(), 1.0);

    // 预热：不计时
    for (int i = 0; i < WARMUP; ++i) { volatile double d = work(v); (void)d; }

    double best = 1e9;
    for (int i = 0; i < TRIALS; ++i) {
        auto t0 = std::chrono::steady_clock::now();
        volatile double d = work(v);
        (void)d;
        auto t1 = std::chrono::steady_clock::now();
        double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
        if (ms < best) best = ms;
        std::printf("  trial %d: %.4f ms\n", i, ms);
    }
    std::printf("warmup: best_ms=%.4f (after %d warmup iters)\n", best, WARMUP);
    return 0;
}
