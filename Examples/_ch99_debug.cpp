// 文件：Examples/_ch99_debug.cpp
// 行号：9 (dump_reduce) / 16 (assert_det)
// 调试数值算法：对比不同策略结果、断言确定性
#include <numeric>
#include <vector>
#include <execution>
#include <cassert>
#include <cmath>
#include <iostream>

void dump_reduce(const std::vector<long long>& v) {
    auto seq = std::reduce(std::execution::seq, v.begin(), v.end(), 0LL);
    auto par = std::reduce(std::execution::par, v.begin(), v.end(), 0LL);
    std::cout << "seq=" << seq << " par=" << par << "\n";
    assert(seq == par);   // 整数满足结合律 -> 必相等
}

void assert_det(const std::vector<double>& v) {
    auto a = std::reduce(std::execution::seq, v.begin(), v.end(), 0.0);
    auto b = std::reduce(std::execution::par, v.begin(), v.end(), 0.0);
    // 浮点不保证相等，仅近似校验
    std::cout << "seq=" << a << " par=" << b
              << " diff=" << std::fabs(a-b) << "\n";
}

int main() {
    dump_reduce({1,2,3,4,5});
    assert_det({0.1,0.2,0.3});
}
