// ⑩'' 内存带宽粗测：顺序写吞吐（GiB/s 量级近似）
// 见 Examples/_ch151_bandwidth.cpp
#include <cstdio>
#include <vector>
#include <chrono>

int main() {
    const std::size_t MB = 256;
    const std::size_t N = MB * 1024 * 1024 / sizeof(double);
    std::vector<double> v(N, 0.0);
    auto t0 = std::chrono::steady_clock::now();
    for (std::size_t i = 0; i < N; ++i) v[i] = (double)i;   // 顺序写
    auto t1 = std::chrono::steady_clock::now();
    double sec = std::chrono::duration<double>(t1 - t0).count();
    double gib = (double)(N * sizeof(double)) / (1024.0*1024.0*1024.0);
    std::printf("bandwidth: wrote %.2f GiB in %.3f s -> %.2f GiB/s\n", gib, sec, gib/sec);
    return 0;
}
