// ch144 ⑥ constexpr：编译期求值，运行期无计算
// 编译：g++ -std=c++23 -O2 -S -masm=intel _ch144_constexpr.cpp -o _ch144_constexpr_O2.asm
constexpr int factorial(int n) {
    return n <= 1 ? 1 : n * factorial(n - 1);
}

static_assert(factorial(5) == 120);

int use_factorial() {
    return factorial(5);   // ✅ 编译期常量折叠，运行期直接是常数
}
