// D5 Wave 4 benchmark: ch99 numeric — accumulate vs reduce: 浮点结合律如何锁死 SIMD
// 编译: g++ -O2 -std=c++23 -o bench.exe _bench_d5_99_numeric.cpp
// 设计要点: accumulate 是严格左折叠, float 加法不满足结合律 → 编译器不得重排 → 标量链;
//   reduce 明说"任意顺序/分组" → 可重结合 → 自动向量化。int 加法天然可结合, 两者应同速。
#include <iostream>
#include <chrono>
#include <vector>
#include <numeric>
#include <random>
#include <cstdint>

static volatile double g_escd = 0;
static volatile long long g_esci = 0;

int main() {
    const int N = 32'000'000;
    const int REP = 5;
    std::mt19937 rng(42);
    auto ms = [](auto a, auto b) { return std::chrono::duration<double, std::milli>(b - a).count(); };

    std::vector<float> vf(N);
    std::uniform_real_distribution<float> dist(0.0f, 1.0f);
    for (auto& x : vf) x = dist(rng);
    std::vector<int> vi(N);
    for (auto& x : vi) x = static_cast<int>(rng() % 100);

    double a1 = 0, a2 = 0;
    long long b1 = 0, b2 = 0;

    auto t0 = std::chrono::steady_clock::now();
    for (int r = 0; r < REP; ++r) a1 += std::accumulate(vf.begin(), vf.end(), 0.0f);
    auto t1 = std::chrono::steady_clock::now();
    for (int r = 0; r < REP; ++r) a2 += std::reduce(vf.begin(), vf.end(), 0.0f);
    auto t2 = std::chrono::steady_clock::now();
    for (int r = 0; r < REP; ++r) b1 += std::accumulate(vi.begin(), vi.end(), 0LL);
    auto t3 = std::chrono::steady_clock::now();
    for (int r = 0; r < REP; ++r) b2 += std::reduce(vi.begin(), vi.end(), 0LL);
    auto t4 = std::chrono::steady_clock::now();

    g_escd = a1 + a2;
    g_esci = b1 + b2;
    std::cout << "accumulate_float_x5 " << ms(t0, t1) << " ms\n";
    std::cout << "reduce_float_x5     " << ms(t1, t2) << " ms\n";
    std::cout << "accumulate_int_x5   " << ms(t2, t3) << " ms\n";
    std::cout << "reduce_int_x5       " << ms(t3, t4) << " ms\n";
    std::cout << "escd=" << g_escd << " esci=" << g_esci << "\n";
    return 0;
}
