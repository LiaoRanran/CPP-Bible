// ⑥ 统计：均值 / 中位数 / 方差（离线计算）
// 见 Examples/_ch151_stats.cpp
#include <cstdio>
#include <vector>
#include <algorithm>
#include <cmath>

static double mean(const std::vector<double>& x) {
    double s = 0; for (double v : x) s += v; return s / x.size();
}
static double median(std::vector<double> x) {
    std::sort(x.begin(), x.end());
    std::size_t n = x.size();
    return n % 2 ? x[n/2] : (x[n/2-1] + x[n/2]) / 2.0;
}
static double variance(const std::vector<double>& x, double m) {
    double s = 0; for (double v : x) s += (v - m) * (v - m);
    return s / (x.size() - 1);
}

int main() {
    std::vector<double> samples = {10.1, 9.8, 10.4, 9.9, 10.0, 10.2, 9.7, 10.1, 10.3, 9.6};
    double m = mean(samples);
    std::printf("stats: mean=%.4f median=%.4f stddev=%.4f n=%zu\n",
                m, median(samples), std::sqrt(variance(samples, m)), samples.size());
    return 0;
}
