// 文件：Examples/_ch99_stability.cpp
// 行号：10 (cond_number) / 19 (compensated_pairwise)
#include <numeric>
#include <vector>
#include <algorithm>
#include <iostream>
#include <cmath>

// 数值稳定性：求和的条件数约等于 max|xi|/|Σxi|
double cond_number(const std::vector<double>& v) {
    double sum = std::accumulate(v.begin(), v.end(), 0.0);
    double maxabs = 0.0;
    for (double x : v) maxabs = std::max(maxabs, std::fabs(x));
    return maxabs / std::fabs(sum);
}

// 稳定版：先排序（从小到大）再累加，减小大吞小
double compensated_pairwise(const std::vector<double>& in) {
    std::vector<double> v = in;
    std::sort(v.begin(), v.end(), [](double a, double b){
        return std::fabs(a) < std::fabs(b);
    });
    return std::accumulate(v.begin(), v.end(), 0.0);
}

int main() {
    std::vector<double> v{1e15, 1.0, -1e15, 2.0};
    std::cout << cond_number(v) << " " << compensated_pairwise(v) << "\n";
}
