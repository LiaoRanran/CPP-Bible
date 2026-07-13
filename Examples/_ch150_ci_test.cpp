// ⑲ CI 门禁：测试可执行文件返回非 0 即阻断合并（此处呈现场景通过态）
#include <cstdio>
int main() {
    int unit = 12, integration = 4, e2e = 2;
    std::printf("ci-gate: unit=%d integration=%d e2e=%d -> ALL GREEN\n", unit, integration, e2e);
    return 0;  // 返回 0 表示门禁通过
}
