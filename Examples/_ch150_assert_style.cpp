// ⑤ REQUIRE 风格自定义断言宏（等价 Catch2）
#include <cstdio>
#include <cassert>
#define REQUIRE(expr) do { \
    if (!(expr)) { std::printf("  REQUIRE failed: %s\n", #expr); return 1; } \
} while (0)
static int twice(int x) { return x * 2; }
int main() {
    REQUIRE(twice(21) == 42);
    REQUIRE(twice(0) == 0);
    REQUIRE(twice(-3) == -6);
    std::printf("assert-style: REQUIRE 3 cases passed\n");
    return 0;
}
