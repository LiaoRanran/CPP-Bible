// ⑭ 异常测试：验证被测代码按契约抛异常（等价 EXPECT_THROW）
#include <cstdio>
#include <stdexcept>
#include <cassert>
static int at(std::size_t i, std::size_t n) {
    if (i >= n) throw std::out_of_range("index");
    return (int)i;
}
int main() {
    bool threw = false;
    try { at(5, 3); } catch (const std::out_of_range&) { threw = true; }
    assert(threw);
    try { at(1, 3); assert(true); } catch (...) { assert(false); }
    std::printf("except: out_of_range thrown as expected\n");
    return 0;
}
