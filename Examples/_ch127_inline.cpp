// _ch127_inline.cpp : 展示 -O0 与 -O2 下内联/常量传播的差异
#include <cstdio>

__attribute__((noinline)) int add_noinline(int a, int b) { return a + b; }
inline int add_inline(int a, int b) { return a + b; }

int use_inlined() {
    int s = 0;
    for (int i = 0; i < 4; ++i) s += add_inline(i, 1);  // 期望被内联
    return s;
}

int use_noinline() {
    return add_noinline(3, 4);  // noinline：保留真实 call
}

int main() {
    std::printf("%d %d\n", use_inlined(), use_noinline());
    return 0;
}
