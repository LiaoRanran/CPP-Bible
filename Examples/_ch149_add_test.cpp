// ③ 单元测试用例：断言式测试门禁（自写极简框架）
#include <cstdio>

int add(int, int);
int sub(int, int);

static int g_fail = 0;
#define CHECK(expr) do { if(!(expr)){ std::printf("FAIL: %s @%d\n", #expr, __LINE__); ++g_fail; } } while(0)

int main() {
    CHECK(add(2, 3) == 5);
    CHECK(add(-1, 1) == 0);
    CHECK(sub(5, 2) == 3);
    std::printf(g_fail == 0 ? "tests: ALL PASS\n" : "tests: %d FAILED\n", g_fail);
    return g_fail == 0 ? 0 : 1;
}
