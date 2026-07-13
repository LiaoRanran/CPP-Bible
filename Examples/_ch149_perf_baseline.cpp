// ⑭ 性能回归基线：微基准，CD 前比对 p50 延迟
#include <cstdio>
#include <chrono>
#include <vector>

int main() {
    const int N = 2'000'000;
    std::vector<int> v(N, 1);
    auto t0 = std::chrono::steady_clock::now();
    long long s = 0;
    for (int x : v) s += x;
    auto t1 = std::chrono::steady_clock::now();
    double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
    std::printf("perf: sum=%lld elapsed_ms=%.3f\n", s, ms);
    return 0;
}
