// ⑲ 报告与可视化：把多次运行导出为 CSV，便于画图
// 见 Examples/_ch151_report_csv.cpp
#include <cstdio>
#include <chrono>
#include <vector>
#include <algorithm>

static double hot() {
    auto t0 = std::chrono::steady_clock::now();
    volatile long long s = 0;
    for (int i = 0; i < 30'000'000; ++i) s += i;
    auto t1 = std::chrono::steady_clock::now();
    return std::chrono::duration<double, std::milli>(t1 - t0).count();
}

int main() {
    std::vector<double> ms;
    for (int r = 0; r < 12; ++r) ms.push_back(hot());
    std::sort(ms.begin(), ms.end());
    std::printf("run,ms\n");
    for (std::size_t i = 0; i < ms.size(); ++i)
        std::printf("%zu,%.4f\n", i, ms[i]);
    std::printf("# median=%.4f\n", ms[ms.size()/2]);
    return 0;
}
