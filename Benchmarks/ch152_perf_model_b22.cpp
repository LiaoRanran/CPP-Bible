// C23 模型量化：当算术强度低，优化方向是"减少内存访问"而非"加算力"
#include <iostream>
#include <vector>
#include <chrono>
int main() {
    const std::size_t N = 4 * 1024 * 1024;
    std::vector<double> a(N, 1.0), b(N, 2.0), c(N);
    // 低算术强度：每读 3 个元素只做 1 次乘加 → 受带宽限制
    auto t0 = std::chrono::steady_clock::now();
    for (std::size_t i = 0; i < N; ++i) c[i] = a[i] * b[i];
    auto t1 = std::chrono::steady_clock::now();
    double sec = std::chrono::duration_cast<std::chrono::nanoseconds>(t1 - t0).count() / 1e9;
    double bytes = 3.0 * N * sizeof(double);
    std::cout << "axpy bandwidth=" << (bytes / sec / 1e9) << " GB/s (对比 DRAM~50GB/s)\n";
    return 0;
}