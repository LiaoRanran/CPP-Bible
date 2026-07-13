// 见 Examples/_ch149_coverage.cpp
// ⑧ 被测单元：覆盖率门禁度量 gcd/lcm 是否被执行
#include <cstdio>
int gcd(int a, int b) { while (b) { int t = b; b = a % b; a = t; } return a; }
int lcm(int a, int b) { return a / gcd(a, b) * b; }
int main() {
    std::printf("gcd(12,18)=%d\n", gcd(12, 18));
    std::printf("lcm(4,6)=%d\n", lcm(4, 6));
    return 0;
}
