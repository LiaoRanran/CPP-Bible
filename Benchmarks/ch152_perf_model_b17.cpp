// C18 易错点3：优化级别不一致——Debug 基准无意义
// 必须用与目标一致的 -O2/-O3 测；-O0 的"慢"不代表发布版慢。
#include <iostream>
#include <chrono>
int main() {
    const int M = 1000000;
    long long acc = 0;
    auto t0 = std::chrono::steady_clock::now();
    for (int i = 0; i < M; ++i) acc = acc * 31 + i;
    auto t1 = std::chrono::steady_clock::now();
    volatile long long sink = acc;
    std::cout << "ns(M=" << M << ")=" << (t1 - t0).count() << " sink=" << sink << "\n";
    return 0;
}