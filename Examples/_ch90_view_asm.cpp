// ch90 ranges —— 真实反汇编证据源（对应 §⑩ view 管道 vs 手写循环）
// 编译：g++ -std=c++23 -O2 -S -masm=intel _ch90_view_asm.cpp -o _ch90_view_asm.asm
#include <vector>
#include <ranges>
#include <iostream>
long sum_even(const std::vector<int>& v) {
    long s = 0;
    for (int x : v | std::views::filter([](int n){ return n % 2 == 0; }))
        s += x;
    return s;
}
int main() { std::vector<int> v{1,2,3,4,5}; return (int)sum_even(v); }
