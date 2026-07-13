// 可变参数模板与包展开：用 volatile 计数器强制发射递归实例化链
// 编译：g++ -std=c++23 -O2 -S -masm=intel _asm_tpl_variadic.cpp -o _asm_tpl_variadic.asm
#include <cstddef>

volatile int g_depth = 0;

void print_all() { g_depth += 1; }    // 基线         _Z9print_allv

template <typename T, typename... Rest>
void print_all(T, Rest... rest) {
    g_depth += 1;                     // 每层展开一次
    print_all(rest...);               // 包展开：实例化 print_all<Rest...>
}

template <typename... Ts>
auto fold_sum(Ts... ts) {
    return (0 + ... + ts);            // 一元左折叠
}

int main() {
    print_all(1, 2.0, 'c');           // 展开 4 层：<int,double,char> <double,char> <char> <>
    volatile auto s = fold_sum(1, 2, 3, 4);   // 期望 10
    return static_cast<int>(s) + static_cast<int>(g_depth);
}
