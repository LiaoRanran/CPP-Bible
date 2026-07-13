// _ch138_strategy_constexpr.cpp
// 第138章 ③：用 if constexpr 在编译期按标签分发不同策略
#include <iostream>
#include <type_traits>

enum class Mode { Fast, Safe, Balanced };

template <Mode M>
int process(int x) {
    if constexpr (M == Mode::Fast)      return x * 2;
    else if constexpr (M == Mode::Safe) return x + 1;
    else                                 return x * 2 + 1;
}

int main() {
    std::cout << process<Mode::Fast>(10)     << '\n';
    std::cout << process<Mode::Safe>(10)     << '\n';
    std::cout << process<Mode::Balanced>(10) << '\n';
    return 0;
}
