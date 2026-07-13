// ⑨ -O2 优化下的热点（用于和 -O3 -march=native 对比）
// 见 Examples/_ch151_opt_O2.cpp（-O2 汇编见 _ch151_opt_O2.asm）
#include <cstdio>
#include <vector>
#include <numeric>
#include <chrono>

int main() {
    const std::size_t N = 50'000'000;
    std::vector<double> a(N), b(N), c(N);
    std::iota(a.begin(), a.end(), 1.0);
    std::iota(b.begin(), b.end(), 2.0);
    auto t0 = std::chrono::steady_clock::now();
    for (std::size_t i = 0; i < N; ++i) c[i] = a[i] * b[i] + a[i];  // 向量化热点
    auto t1 = std::chrono::steady_clock::now();
    volatile double chk = c[N-1];
    std::printf("opt_O2: axpy_ms=%.3f chk=%.1f\n",
                std::chrono::duration<double, std::milli>(t1 - t0).count(), chk);
    return 0;
}
