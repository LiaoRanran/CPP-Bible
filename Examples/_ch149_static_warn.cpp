// 见 Examples/_ch149_static_warn.cpp
// ⑥ 故意触发 -Wunused-parameter，演示静态分析门禁产出告警
#include <cstdio>
int compute(int x, int unused) {  // unused 触发 -Wunused-parameter
    return x * 2;
}
int main() {
    std::printf("compute=%d\n", compute(21, 0));
    return 0;
}
