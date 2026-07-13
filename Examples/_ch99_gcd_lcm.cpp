// 文件：Examples/_ch99_gcd_lcm.cpp
// 行号：8 (simplify_fraction) / 14 (ring_wrap)
#include <numeric>
#include <iostream>

// 约分：分子分母同除以 gcd
void simplify_fraction(long num, long den) {
    long g = std::gcd(num, den);
    std::cout << num/g << "/" << den/g << "\n";
}

// 周期对齐：两个周期 a,b 的最小公倍数
long ring_wrap(long a, long b) {
    return std::lcm(a, b);
}

int main() {
    simplify_fraction(12, 18);
    std::cout << ring_wrap(4, 6) << "\n";
}
