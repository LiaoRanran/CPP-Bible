// ⑫ 标量求和（对比 SIMD；汇编见 _ch151_simd_scalar.asm）
// 见 Examples/_ch151_simd_scalar.cpp
#include <cstdio>
#include <vector>
#include <chrono>
#include <numeric>

int main() {
    const std::size_t N = 40'000'000;
    std::vector<float> v(N);
    std::iota(v.begin(), v.end(), 1.0f);
    auto t0 = std::chrono::steady_clock::now();
    volatile float s = 0;
    for (std::size_t i = 0; i < N; ++i) s += v[i];     // 标量累加
    auto t1 = std::chrono::steady_clock::now();
    std::printf("scalar: sum_ms=%.3f s=%.1f\n",
                std::chrono::duration<double, std::milli>(t1 - t0).count(), s);
    return 0;
}
