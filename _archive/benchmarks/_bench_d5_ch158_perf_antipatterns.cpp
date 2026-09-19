// Wave8 D5 bench: 性能反模式 —— 行优先 vs 列优先 2D 遍历（缓存命中 vs 失效）
// 编译: g++ -O2 -std=c++23 _bench_d5_ch158_perf_antipatterns.cpp -o _bench_d5_ch158_perf_antipatterns.exe
// 运行: ./_bench_d5_ch158_perf_antipatterns.exe  (输出毫秒, 不断言时间/倍数)
#include <cstdio>
#include <cstdint>
#include <chrono>
#include <vector>

static volatile std::uint64_t g_sink = 0;

int main() {
    constexpr int M = 4096, N = 4096;
    std::vector<int> a(static_cast<std::size_t>(M) * N, 1);

    auto t0 = std::chrono::steady_clock::now();
    std::uint64_t s = 0;
    for (int i = 0; i < M; ++i)
        for (int j = 0; j < N; ++j)
            s += a[static_cast<std::size_t>(i) * N + j];   // 行优先：顺序访问
    auto t1 = std::chrono::steady_clock::now();
    g_sink += s;
    std::printf("row-major (cache-friendly): %.3f ms\n",
                std::chrono::duration<double, std::milli>(t1 - t0).count());

    auto t2 = std::chrono::steady_clock::now();
    s = 0;
    for (int j = 0; j < N; ++j)
        for (int i = 0; i < M; ++i)
            s += a[static_cast<std::size_t>(i) * N + j];   // 列优先：跨步访问（反模式）
    auto t3 = std::chrono::steady_clock::now();
    g_sink += s;
    std::printf("column-major (cache-unfriendly antipattern): %.3f ms\n",
                std::chrono::duration<double, std::milli>(t3 - t2).count());

    return 0;
}
