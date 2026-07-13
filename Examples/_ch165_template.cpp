// _ch165_template.cpp : 模板/特化/可变参数 练习（中级→高级）
#include <iostream>
#include <type_traits>

template <typename T>
T max(T a, T b) { return a > b ? a : b; }      // 函数模板

template <typename T>
struct Box { T v; };                            // 类模板

template <>
struct Box<bool> {                             // 全特化
    bool v;
    void flip() { v = !v; }
};

template <typename... Ts>                       // 可变参数模板
void print(Ts... xs) {
    ((std::cout << xs << " "), ...);            // 折叠表达式
    std::cout << "\n";
}

int main() {
    std::cout << max(3, 7) << " " << max(1.5, 0.5) << "\n";
    Box<int> b{42};
    Box<bool> bb{false}; bb.flip();
    std::cout << b.v << " " << bb.v << "\n";
    print(1, 2.0, "hi", 'x');
    return 0;
}
