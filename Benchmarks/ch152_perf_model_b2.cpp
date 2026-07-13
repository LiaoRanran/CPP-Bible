// C3 带宽直觉：拷贝大数组，估算 GB/s（示意量级）
#include <iostream>
#include <chrono>
#include <cstring>
int main() {
    const std::size_t N = 16 * 1024 * 1024;       // 16M 元素
    long long* a = new long long[N];
    long long* b = new long long[N];
    auto t0 = std::chrono::steady_clock::now();
    std::memcpy(b, a, N * sizeof(long long));       // 顺序大块拷贝
    auto t1 = std::chrono::steady_clock::now();
    double sec = std::chrono::duration_cast<std::chrono::nanoseconds>(t1 - t0).count() / 1e9;
    double bytes = 2.0 * N * sizeof(long long);     // 读 a + 写 b
    std::cout << "bandwidth ~ " << (bytes / sec / 1e9) << " GB/s\n";
    delete[] a; delete[] b;
    return 0;
}