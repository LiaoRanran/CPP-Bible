// D5 Wave 3 benchmark: ch43 CPU 缓存与内存局部性 — 行优先 vs 列优先
// 编译: g++ -O2 -std=c++23 -o bench.exe _bench_d5_43_cache.cpp
// 目的: 同一份 4096x4096 矩阵, 行优先(连续)vs 列优先(跨行大步长)遍历的缓存友好度差.
// 注: stride 子基准已被移除——不同 stride 的访问次数不同会混淆结论, 行/列对比已足够说明缓存局部性.
#include <iostream>
#include <chrono>
#include <vector>
#include <random>
#include <cstdint>

static volatile long long g_esc = 0;

template <class F>
double bench(const char* name, F f, int rounds = 5) {
    double best = 1e18;
    for (int r = 0; r < rounds; ++r) {
        auto t0 = std::chrono::steady_clock::now();
        long long res = f();
        auto t1 = std::chrono::steady_clock::now();
        g_esc += res;
        double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
        if (ms < best) best = ms;
    }
    std::cout << name << ": " << best << " ms\n";
    return best;
}

int main() {
    const int N = 4096;                 // 16M int = 64MB，超过 L3，逼迫缓存行为显现
    std::vector<int> m((size_t)N * N);
    std::mt19937 rng(7);
    for (size_t i = 0; i < m.size(); ++i) m[i] = (int)(rng() % 1000);

    bench("row_major", [&] {
        long long s = 0;
        for (int i = 0; i < N; ++i)
            for (int j = 0; j < N; ++j)
                s += m[(size_t)i * N + j];
        return s;
    });
    bench("col_major", [&] {
        long long s = 0;
        for (int j = 0; j < N; ++j)
            for (int i = 0; i < N; ++i)
                s += m[(size_t)i * N + j];
        return s;
    });
    std::cout << "esc=" << g_esc << "\n";
    return 0;
}
