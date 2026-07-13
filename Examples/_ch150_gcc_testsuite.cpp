// ⑰ libstdc++ testsuite 风格：dg-do run + VERIFY 宏
#include <cstdio>
#include <vector>
#include <cassert>
// 等价于 testsuite 的 VERIFY 宏
#define VERIFY(expr) do { if (!(expr)) { std::printf("VERIFY failed: %s\n", #expr); return 1; } } while (0)
int main() {
    std::vector<int> v(5, 7);     // dg-do run
    VERIFY(v.size() == 5);
    VERIFY(v.front() == 7);
    VERIFY(v.back() == 7);
    std::printf("gcc-testsuite-style: vector(5,7) VERIFY OK\n");
    return 0;
}
