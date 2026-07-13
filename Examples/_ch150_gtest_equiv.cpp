// ②'' GoogleTest 等价自包含实现：TEST 宏 + ASSERT_EQ 风格
#include <cstdio>
#include <cassert>
// 等价 gtest 的 TEST/Float 简化为编译期可跑的小型 harness
static int sub(int a, int b) { return a - b; }
int main() {
    assert(sub(10, 4) == 6);
    assert(sub(0, 5) == -5);
    std::printf("gtest-equiv: sub() 2 cases OK\n");
    return 0;
}
