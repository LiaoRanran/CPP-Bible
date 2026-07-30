// _bench_d5_153_branch.cpp — ch153 CPU 微架构：分支预测的真实惩罚
// g++ -O2 -std=c++23
// 注意：-O2 下 GCC 可能将简单 if-累加 if-conversion 成 cmov/向量化，
// 故除经典 sum-if 外，另设"分支体含存储副作用"的 compaction 内核（无法 cmov 化）。
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <vector>
#include <algorithm>
#include <random>

static double now_ms() {
    using namespace std::chrono;
    return duration<double, std::milli>(steady_clock::now().time_since_epoch()).count();
}
template <class F>
static double bench(const char* name, F&& f) {
    std::vector<double> t;
    for (int r = 0; r < 5; ++r) { double t0 = now_ms(); f(); t.push_back(now_ms() - t0); }
    std::sort(t.begin(), t.end());
    std::printf("%-40s %10.3f ms\n", name, t[2]);
    return t[2];
}
volatile std::uint64_t g_sink;

__attribute__((noinline))
std::uint64_t sum_if(const std::uint8_t* p, std::size_t n) {
    std::uint64_t s = 0;
    for (std::size_t i = 0; i < n; ++i)
        if (p[i] >= 128) s += p[i];
    return s;
}
__attribute__((noinline))
std::uint64_t sum_branchless(const std::uint8_t* p, std::size_t n) {
    std::uint64_t s = 0;
    for (std::size_t i = 0; i < n; ++i)
        s += p[i] * std::uint64_t(p[i] >= 128);
    return s;
}
// 分支体含带副作用的存储 + 游标推进 —— 无法 if-conversion，真实暴露分支缺失
__attribute__((noinline))
std::size_t compact_if(const std::uint8_t* p, std::size_t n, std::uint8_t* out) {
    std::size_t k = 0;
    for (std::size_t i = 0; i < n; ++i)
        if (p[i] >= 128) out[k++] = p[i];
    return k;
}

int main() {
    constexpr std::size_t N = 32'000'000;
    constexpr int REPS = 5;

    std::vector<std::uint8_t> unsorted(N);
    std::mt19937 rng(42);
    for (auto& v : unsorted) v = std::uint8_t(rng());
    std::vector<std::uint8_t> sorted = unsorted;
    std::sort(sorted.begin(), sorted.end());
    std::vector<std::uint8_t> out(N);

    std::uint64_t s1 = 0, s2 = 0, s3 = 0;
    bench("sum-if unsorted", [&] {
        std::uint64_t s = 0;
        for (int r = 0; r < REPS; ++r) s += sum_if(unsorted.data(), N);
        s1 = s; g_sink = s;
    });
    bench("sum-if sorted", [&] {
        std::uint64_t s = 0;
        for (int r = 0; r < REPS; ++r) s += sum_if(sorted.data(), N);
        s2 = s; g_sink = s;
    });
    bench("sum branchless unsorted", [&] {
        std::uint64_t s = 0;
        for (int r = 0; r < REPS; ++r) s += sum_branchless(unsorted.data(), N);
        s3 = s; g_sink = s;
    });
    std::printf("sum checksums: %llu %llu %llu (must equal)\n",
                (unsigned long long)s1, (unsigned long long)s2, (unsigned long long)s3);

    std::size_t k1 = 0, k2 = 0;
    bench("compact-if unsorted", [&] {
        std::size_t k = 0;
        for (int r = 0; r < REPS; ++r) k = compact_if(unsorted.data(), N, out.data());
        k1 = k; g_sink = k;
    });
    bench("compact-if sorted", [&] {
        std::size_t k = 0;
        for (int r = 0; r < REPS; ++r) k = compact_if(sorted.data(), N, out.data());
        k2 = k; g_sink = k;
    });
    std::printf("compact counts: %zu %zu (must equal)\n", k1, k2);
    return 0;
}
