// _ch138_strategy.cpp
// 第138章 ②：策略模式——基于 std::function 与基于虚接口的两种实现
#include <functional>
#include <iostream>
#include <vector>

// 方案 A：std::function 擦除
struct TaxCalculator {
    std::function<double(double)> policy;
    double compute(double v) const { return policy ? policy(v) : v; }
};

// 方案 B：经典虚接口
struct Discount { virtual ~Discount() = default; virtual double apply(double p) const = 0; };
struct NoDiscount : Discount { double apply(double p) const override { return p; } };
struct TenPercent : Discount { double apply(double p) const override { return p * 0.9; } };

int main() {
    TaxCalculator tc;
    tc.policy = [](double x) { return x * 1.13; };
    std::cout << tc.compute(100.0) << '\n';

    TenPercent ten;
    std::cout << ten.apply(100.0) << '\n';
    return 0;
}
