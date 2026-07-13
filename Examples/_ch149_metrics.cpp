// 见 Examples/_ch149_metrics.cpp
// ⑲ 度量：DORA 四项核心指标
#include <cstdio>
struct DORA {
    int   deploy_freq_per_day;
    double mttr_hours;
    double change_fail_rate;
};
int main() {
    DORA d{10, 1.5, 0.08};
    std::printf("DORA: freq=%d/day mttr=%.1fh cfr=%.0f%%\n",
                d.deploy_freq_per_day, d.mttr_hours, d.change_fail_rate * 100);
    return 0;
}
