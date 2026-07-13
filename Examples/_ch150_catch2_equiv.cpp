// ②'' Catch2 等价自包含实现：SECTION 风格计数
#include <cstdio>
#include <cassert>
static int mul(int a, int b) { return a * b; }
int main() {
    // 等价 Catch2 的多个 SECTION
    assert(mul(3, 4) == 12);
    assert(mul(0, 9) == 0);
    assert(mul(-2, 5) == -10);
    std::printf("catch2-equiv: mul() 3 sections OK\n");
    return 0;
}
