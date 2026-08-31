// P1：观察栈帧与参数落位（配合 §3 汇编阅读）
#include <cstdio>
int leaf(int a, int b) {
    int x = a + b;
    int y = x * 2;
    return y + 3;
}
int caller(int a, int b, int c, int d) {
    int local = leaf(a, b) + leaf(c, d);
    return local;
}