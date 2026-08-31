// 文件：Examples/_ch127_inline.cpp，行号：9（use_inlined）/ 14（use_noinline）/ 5（add_inline）
// 编译命令（真实）：
//   g++ -std=c++20 -O0 -S -masm=intel _ch127_inline.cpp -o _ch127_inline_O0.asm
//   g++ -std=c++20 -O2 -S -masm=intel _ch127_inline.cpp -o _ch127_inline_O2.asm
#include <cstdio>
inline int add_inline(int a, int b) { return a + b; }
__attribute__((noinline)) int add_noinline(int a, int b) { return a + b; }
int use_inlined() {
    int s = 0;
    for (int i = 0; i < 4; ++i) s += add_inline(i, 1); // 期望被内联
    return s;
}
int use_noinline() { return add_noinline(3, 4); }       // noinline：保留真实 call