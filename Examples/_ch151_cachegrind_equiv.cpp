// ⑧ 自包含等价 cache miss 探针（等价于 cachegrind 的 D1 miss 观察）
// 见 Examples/_ch151_cachegrind_equiv.cpp
#include <cstdio>
#include <vector>
#include <chrono>

// 顺序访问：缓存友好；随机访问：缓存不友好。用计时近似反映 cache 行为。
int main() {
    const std::size_t N = 20'000'000;
    std::vector<int> v(N);
    for (std::size_t i = 0; i < N; ++i) v[i] = (int)i;

    // 顺序
    auto t0 = std::chrono::steady_clock::now();
    volatile long long s = 0;
    for (std::size_t i = 0; i < N; ++i) s += v[i];
    auto t1 = std::chrono::steady_clock::now();
    std::printf("sequential: ms=%.3f (cache-friendly)\n",
                std::chrono::duration<double, std::milli>(t1 - t0).count());

    // 跨步 1024（典型 cache miss 模式）
    const std::size_t stride = 1024;
    auto t2 = std::chrono::steady_clock::now();
    volatile long long r = 0;
    for (std::size_t i = 0; i < N; i += stride) r += v[i];
    auto t3 = std::chrono::steady_clock::now();
    std::printf("stride1024: ms=%.3f (cache-unfriendly)\n",
                std::chrono::duration<double, std::milli>(t3 - t2).count());
    return 0;
}
