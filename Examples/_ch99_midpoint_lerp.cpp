// 文件：Examples/_ch99_midpoint_lerp.cpp
// 行号：9 (safe_mid) / 15 (anim)
#include <numeric>
#include <cmath>
#include <climits>
#include <iostream>

// 防溢出中点：即使 a,b 接近类型边界也不溢出
int safe_mid(int a, int b) {
    return std::midpoint(a, b);
}

// 线性插值（动画/缓动常用）
double anim(double from, double to, double t) {
    return std::lerp(from, to, t);   // t∈[0,1]
}

int main() {
    std::cout << safe_mid(INT_MAX - 3, INT_MAX) << "\n";
    std::cout << anim(0.0, 100.0, 0.25) << "\n";
}
