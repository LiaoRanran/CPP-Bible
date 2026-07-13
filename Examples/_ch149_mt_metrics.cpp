// ⑲ 构建度量：用 chrono 记录阶段耗时（MTTR/部署频率另见正文）
#include <cstdio>
#include <chrono>
int main() {
    auto t0 = std::chrono::steady_clock::now();
    volatile long long s = 0;
    for (int i = 0; i < 50'000'000; ++i) s += i;
    auto t1 = std::chrono::steady_clock::now();
    double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
    std::printf("stage-time: %.2f ms\n", ms);
    return 0;
}
