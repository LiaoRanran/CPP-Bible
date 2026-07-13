// 补-A 一维数组 cache 友好归约 + 朴素 vs 分块对比骨架
#include <iostream>
#include <vector>
#include <chrono>

int main() {
    constexpr int N = 8'000'000;
    std::vector<double> a(N, 1.0);
    double s = 0.0;
    auto t0 = std::chrono::steady_clock::now();
    for (double v : a) s += v;
    auto t1 = std::chrono::steady_clock::now();
    std::cout << "reduce=" << std::chrono::duration<double, std::milli>(t1 - t0).count()
              << "ms sum=" << s << "\n";
    return 0;
}