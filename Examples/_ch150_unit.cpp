// ② 自包含单元测试：最小测试 harness（等价 GoogleTest TEST）
#include <cstdio>
#include <cassert>
static int passed = 0, failed = 0;
#define CHECK(cond) do { \
    if (cond) { ++passed; } \
    else { ++failed; std::printf("  FAIL: %s @ line %d\n", #cond, __LINE__); } \
} while (0)
static int add(int a, int b) { return a + b; }
int main() {
    CHECK(add(2, 3) == 5);
    CHECK(add(-1, 1) == 0);
    CHECK(add(0, 0) == 0);
    std::printf("unit: passed=%d failed=%d\n", passed, failed);
    return failed ? 1 : 0;
}
