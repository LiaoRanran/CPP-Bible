// ⑤' 带信息的断言：失败时打印上下文
#include <cstdio>
#include <cassert>
#define EXPECT_EQ(a, b) do { \
    if ((a) != (b)) std::printf("  EXPECT_EQ(%s,%s) got %d vs %d\n", #a, #b, (a), (b)); \
    assert((a) == (b)); } while (0)
int main() {
    int computed = 2 + 2;
    EXPECT_EQ(computed, 4);
    std::printf("assert-msg: 2+2 == 4 verified\n");
    return 0;
}
