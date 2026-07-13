// 见 Examples/_ch149_regression.cpp
// ⑭ 回归比较：当前耗时超出基线阈值即判定回归
#include <cstdio>
int main() {
    double baseline = 120.0, current = 135.0;  // 毫秒
    double delta = (current - baseline) / baseline * 100.0;
    std::printf("perf delta=%.1f%% %s\n", delta, delta > 10 ? "[REGRESSION]" : "[OK]");
    return 0;
}
