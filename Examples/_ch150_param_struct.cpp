// ⑬' 结构化参数：{输入,期望} 表驱动测试
#include <cstdio>
#include <cassert>
static int clamp(int v, int lo, int hi) { return v < lo ? lo : (v > hi ? hi : v); }
struct Case { int v, lo, hi, expect; };
int main() {
    Case tbl[] = { {5,0,10,5}, {-1,0,10,0}, {99,0,10,10}, {3,3,3,3} };
    int n = (int)(sizeof(tbl)/sizeof(tbl[0]));
    for (int i = 0; i < n; ++i) {
        Case c = tbl[i];
        assert(clamp(c.v, c.lo, c.hi) == c.expect);
    }
    std::printf("param-struct: clamp %d cases OK\n", n);
    return 0;
}
