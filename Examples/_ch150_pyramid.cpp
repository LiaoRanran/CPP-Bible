// ① 测试金字塔：单元/集成/端到端的比例经验值
#include <cstdio>
int main() {
    int unit = 70, integration = 20, e2e = 10;
    std::printf("test pyramid: unit=%d%% integration=%d%% e2e=%d%%\n", unit, integration, e2e);
    std::printf("invariant: unit_tests >> integration_tests > e2e_tests\n");
    return 0;
}
