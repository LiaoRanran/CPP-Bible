// 文件：Examples/_ch99_best_practice.cpp
// 行号：11 (safe_mean) / 19 (kahan)
#include <numeric>
#include <vector>
#include <execution>
#include <cmath>
#include <iostream>

// 实践1：先求和使用稳定初值类型，避免 int 初值截断
double safe_mean(const std::vector<int>& v) {
    long long sum = std::reduce(std::execution::par,
        v.begin(), v.end(), 0LL);   // 用 0LL 而非 0
    return static_cast<double>(sum) / v.size();
}

// 实践2：大数量级差异求和用 Kahan 补偿（算法层面的数值稳定性）
double kahan(const std::vector<double>& v) {
    double sum = 0.0, c = 0.0;
    for (double x : v) {
        double y = x - c;
        double t = sum + y;
        c = (t - sum) - y;
        sum = t;
    }
    return sum;
}

int main() {
    std::vector<int> v{1,2,3,4,5};
    std::cout << safe_mean(v) << "\n";
    std::cout << kahan({1e16, 1.0, -1e16}) << "\n";
}
