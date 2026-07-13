// ③' 防止优化（二）：asm volatile 阻止单条表达式被折叠
// 见 Examples/_ch151_asm_volatile.cpp
#include <cstdio>

// 把 x 作为"输出操作数"喂给一个空的 asm 块，编译器无法证明可删。
static int black_box(int x) {
    asm volatile("" : "+r"(x));   // "+r"：读+写，强制 x 真实存在
    return x;
}

int main() {
    int s = 0;
    for (int i = 0; i < 1000; ++i) s += black_box(i);
    std::printf("asm_volatile: s=%d (loop survived optimization)\n", s);
    return 0;
}
