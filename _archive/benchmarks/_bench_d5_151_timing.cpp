// _bench_d5_151_timing.cpp  (GCC 15.3.0, g++ -O2 -std=c++23)
// 真实基准：benchmark 章节本身的两大陷阱——时钟分辨率 + 单次采样的巨大方差。
// 循环内用 asm volatile fence 阻止 DCE（否则极轻量操作被闭式化，测得≈0）。
#include <chrono>
#include <cmath>
#include <iostream>
#include <numeric>
#include <vector>
#include <algorithm>

int main() {
    using namespace std::chrono;

    // 1) steady_clock 分辨率（相邻两次 now() 的最小可分辨间隔）
    auto r0 = steady_clock::now();
    auto r1 = r0;
    int cnt = 0;
    while (r1 == r0 && cnt < 2'000'000) { r1 = steady_clock::now(); ++cnt; }
    double res_ns = duration<double, std::nano>(r1 - r0).count();
    std::cout << "steady_clock resolution ~ " << res_ns << " ns (samples=" << cnt << ")" << std::endl;

    // 2) 单次采样方差：对一个极轻量操作反复计时，看 min/max 散布
    const int N = 3000;
    std::vector<double> samples(N);
    volatile long long sinkv = 0;
    for (int k = 0; k < N; ++k) {
        auto t0 = steady_clock::now();
        long long s = 0; for (int i = 0; i < 100; ++i) { s += i; asm volatile("" : "+r"(s) :: "memory"); }
        auto t1 = steady_clock::now();
        sinkv += s;
        samples[k] = duration<double, std::nano>(t1 - t0).count();
    }
    double mean = std::accumulate(samples.begin(), samples.end(), 0.0) / N;
    double var = 0; for (double x : samples) var += (x - mean) * (x - mean);
    var /= N;
    double mn = *std::min_element(samples.begin(), samples.end());
    double mx = *std::max_element(samples.begin(), samples.end());
    std::cout << "100-iter sum: mean=" << mean << " ns  stddev=" << std::sqrt(var)
              << " ns  min=" << mn << " ns  max=" << mx << " ns" << std::endl;
    std::cout << "single-shot spread max/min = " << (mx / mn) << "x ; sink=" << sinkv << std::endl;
    return 0;
}
