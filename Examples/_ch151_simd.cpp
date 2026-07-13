// ⑫' std::reduce 并行策略 + 自动向量化提示（汇编见 _ch151_simd.asm）
// 见 Examples/_ch151_simd.cpp
// 注：本机 mingw 并行策略需 TBB，故此处用顺序 reduce 触发自动向量化，
//     -O3 -march=native 下累加会被展开为 SIMD 指令。
#include <cstdio>
#include <vector>
#include <chrono>
#include <numeric>
#include <execution>

int main() {
    const std::size_t N = 40'000'000;
    std::vector<float> v(N);
    std::iota(v.begin(), v.end(), 1.0f);
    auto t0 = std::chrono::steady_clock::now();
    volatile float s = std::reduce(std::execution::seq, v.begin(), v.end(), 0.0f);
    auto t1 = std::chrono::steady_clock::now();
    std::printf("simd(reduce): sum_ms=%.3f s=%.1f\n",
                std::chrono::duration<double, std::milli>(t1 - t0).count(), s);
    return 0;
}
