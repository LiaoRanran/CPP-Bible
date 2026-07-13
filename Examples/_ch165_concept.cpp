// _ch165_concept.cpp : C++20 concepts 约束模板（高级）
#include <concepts>
#include <iostream>

template <std::integral T>
T square(T x) { return x * x; }

template <typename T>
concept Addable = requires(T a, T b) { a + b; };

template <Addable T>
T twice(T x) { return x + x; }

int main() {
    std::cout << square(5) << "\n";       // 25
    std::cout << twice(3.5) << "\n";       // 7
    return 0;
}
