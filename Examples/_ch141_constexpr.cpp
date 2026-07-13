// Examples/_ch141_constexpr.cpp
// DI 与 constexpr：编译期策略对象可作为常量表达式注入，进入 ROM / 常量折叠。
#include <iostream>

struct PolicyA { static constexpr int factor() { return 2; } };
struct PolicyB { static constexpr int factor() { return 3; } };

template <class P>
constexpr int compute(int x) { return x * P::factor(); }   // ✅ constexpr 注入

int main() {
    constexpr int r1 = compute<PolicyA>(10);   // 编译期 = 20
    constexpr int r2 = compute<PolicyB>(10);   // 编译期 = 30
    std::cout << r1 << " " << r2 << "\n";
}
