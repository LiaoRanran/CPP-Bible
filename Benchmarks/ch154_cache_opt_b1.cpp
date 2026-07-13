// ② 指针追逐（pointer chasing）演示"等内存"：随机跳，缓存几乎全失效
#include <iostream>
#include <vector>
#include <chrono>
#include <cstdint>

int main() {
    constexpr std::size_t N = 1u << 20;          // 1M 节点
    std::vector<std::uint32_t> idx(N);
    for (std::size_t i = 0; i < N; ++i) idx[i] = (std::uint32_t)i;
    // 确定性 xorshift 驱动的 Fisher–Yates 洗牌（禁用 <random>，自带 PRNG）
    std::uint64_t s = 88172645463325252ULL;
    auto rng = [&]() { s ^= s << 13; s ^= s >> 7; s ^= s << 17; return s; };
    for (std::size_t i = N - 1; i > 0; --i) {
        std::size_t j = rng() % (i + 1);
        std::swap(idx[i], idx[j]);
    }
    std::uint32_t p = 0;
    constexpr std::size_t STEPS = 50'000'000;
    auto t0 = std::chrono::steady_clock::now();
    for (std::size_t k = 0; k < STEPS; ++k) p = idx[p];   // 每一步都随机跳
    auto t1 = std::chrono::steady_clock::now();
    double ns = std::chrono::duration<double, std::nano>(t1 - t0).count() / STEPS;
    std::cout << "pointer-chase ≈ " << ns << " ns/step (acc=" << p << ")\n";
    return 0;
}