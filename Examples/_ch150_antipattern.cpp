// ⑱ 反模式：依赖全局顺序/隐式状态的脆弱测试（演示为何要避免）
#include <cstdio>
#include <cassert>
static int g_counter = 0;          // 反模式：共享可变全局状态
static int next_id() { return ++g_counter; }
int main() {
    // 若两个测试共享 g_counter 且未重置，则第二个断言会失败
    g_counter = 0;                  // 正确做法：每个用例前重置
    assert(next_id() == 1);
    g_counter = 0;                  // 必须重置，否则脆弱
    assert(next_id() == 1);
    std::printf("antipattern: reset global before each case -> stable\n");
    return 0;
}
