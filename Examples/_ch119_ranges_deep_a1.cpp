// 文件：Examples/_asm_ranges.cpp，行号：8（_Z10use_rangesv）/ 39（test cl,1 过滤）/ 47（imul 平方）
// 编译：g++ 15.3.0 -std=c++23 -O2 -S -masm=intel _asm_ranges.cpp -o _asm_ranges.asm
#include <ranges>
#include <vector>
int use_ranges() {
    std::vector<int> v = {1,2,3,4,5,6};
    int s = 0;
    for (int x : v | std::views::filter([](int i){ return i % 2 == 0; })
                  | std::views::transform([](int i){ return i * i; }))
        s += x;   // 2*2 + 4*4 + 6*6 = 56
    return s;
}