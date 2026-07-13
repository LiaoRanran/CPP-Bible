// ⑬'' GoogleTest TEST_P 等价：组合 {a,b,expect}
#include <cstdio>
#include <cassert>
static int max(int a, int b) { return a > b ? a : b; }
struct P { int a, b, e; };
int main() {
    P tbl[] = { {1,2,2}, {5,3,5}, {-1,-2,-1}, {0,0,0} };
    int n = (int)(sizeof(tbl)/sizeof(tbl[0]));
    for (int i = 0; i < n; ++i) assert(max(tbl[i].a, tbl[i].b) == tbl[i].e);
    std::printf("param-gtest-equiv: max() %d params OK\n", n);
    return 0;
}
