// ⑯ 结果可信度：多次运行取最小/中位数，过滤噪声
// 见 Examples/_ch151_credibility.cpp
#include <cstdio>
#include <chrono>
#include <vector>
#include <algorithm>
#include <numeric>

static void hot() {
    volatile long long s = 0;
    for (int i = 0; i < 50'000'000; ++i) s += i;
}

int main() {
    const int RUNS = 21;
    std::vector<double> ms;
    for (int r = 0; r < RUNS; ++r) {
        auto t0 = std::chrono::steady_clock::now();
        hot();
        auto t1 = std::chrono::steady_clock::now();
        ms.push_back(std::chrono::duration<double, std::milli>(t1 - t0).count());
    }
    std::sort(ms.begin(), ms.end());
    double med = ms[RUNS/2];
    double lo = ms.front(), hi = ms.back();
    std::printf("credibility: runs=%d median=%.4f min=%.4f max=%.4f spread=%.4f ms\n",
                RUNS, med, lo, hi, hi - lo);
    return 0;
}
