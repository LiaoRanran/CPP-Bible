#include <cmath>
// ⑭ perf 剖析目标：一个会被采样到热点（hot）的密集循环
// 用法见正文 perf stat / perf record 命令
void hot_work(float* a, const float* b, int n) {
    for (int i = 0; i < n; ++i)
        a[i] = std::sqrt(b[i] * b[i] + 1.0f);   // 计算密集，易成瓶颈
}
