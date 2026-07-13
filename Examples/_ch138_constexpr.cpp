// _ch138_constexpr.cpp
// 第138章 ⑱：行为型模式与 constexpr——在编译期完成策略/状态选择
#include <iostream>

enum class Op { Add, Mul };

constexpr int run(Op op, int a, int b) {
    switch (op) {
        case Op::Add: return a + b;
        case Op::Mul: return a * b;
    }
    return 0;
}

int main() {
    constexpr int r = run(Op::Mul, 6, 7);   // 编译期计算
    std::cout << r << '\n';
    return 0;
}
