// 见 Examples/_ch149_test_harness.cpp
// ⑦ 零依赖测试桩：测试门禁用退出码表达通过/失败
#include <cstdio>
struct Test { const char* name; bool (*fn)(); };
static int g_pass = 0, g_fail = 0;
void run(const Test& t) {
    if (t.fn()) { ++g_pass; std::printf("[PASS] %s\n", t.name); }
    else        { ++g_fail; std::printf("[FAIL] %s\n", t.name); }
}
bool t_add() { return (2 + 2) == 4; }
bool t_sub() { return (5 - 3) == 2; }
int main() {
    Test tests[] = { {"add", t_add}, {"sub", t_sub} };
    for (auto& t : tests) run(t);
    std::printf("summary: %d passed, %d failed\n", g_pass, g_fail);
    return g_fail ? 1 : 0;
}
