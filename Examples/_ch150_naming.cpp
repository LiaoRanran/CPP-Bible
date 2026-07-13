// ⑥ 测试命名：Method_Condition_Expectation（Given/When/Then 风格）
#include <cstdio>
#include <cassert>
static int divide(int a, int b) { return a / b; }
int main() {
    // Divide_PositiveByPositive_ReturnsQuotient
    assert(divide(10, 2) == 5);
    // Divide_NegativeByPositive_ReturnsNegative
    assert(divide(-9, 3) == -3);
    std::printf("naming: 2 named cases (Divide_*) OK\n");
    return 0;
}
