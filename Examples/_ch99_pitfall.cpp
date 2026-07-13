// 文件：Examples/_ch99_pitfall.cpp
// 行号：10 (nonassoc) / 18 (fixed_associative)
// 演示：浮点 reduce 因结合律不成立，结果随执行策略/分块不同而改变
#include <numeric>
#include <vector>
#include <execution>
#include <iostream>

// ❌ 浮点 reduce 结果不确定：不同分块给出不同比特结果
double nonassoc(const std::vector<double>& v) {
    return std::reduce(std::execution::par, v.begin(), v.end(), 0.0);
}

// ✅ 用整数或满足结合律的运算 -> 结果确定
long long fixed_associative(const std::vector<long long>& v) {
    return std::reduce(std::execution::par, v.begin(), v.end(), 0LL);
}

int main() {
    std::vector<double> v(1'000'000, 1e-8);
    v[0] = 1.0;                 // 巨大 + 微小 混合，凸显重排差异
    std::cout << nonassoc(v) << "\n";
}
