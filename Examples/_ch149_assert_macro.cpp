// 见 Examples/_ch149_assert_macro.cpp
// ⑦ 断言宏：门禁中任何 CHECK 失败即非零退出，阻断合并
#include <cstdio>
#include <cstdlib>
#define CHECK(cond) do { if(!(cond)){ std::printf("ASSERT FAIL: %s\n", #cond); std::abort(); } } while(0)
int main() {
    CHECK(1 + 1 == 2);
    CHECK(sizeof(int) >= 4);
    std::printf("all checks passed\n");
    return 0;
}
