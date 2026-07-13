// Examples/_ch08_perf.cpp
// 真实基准：ch08_cpp23.md 的 expected vs exception 失败路径延迟实测替换
// 编译: g++ -O2 -std=c++23 -m64 _ch08_perf.cpp -o _ch08_perf
//
// 目的：为 ch08 附录 D "expected 比异常快100x" 提供本机真值，替换 ~N 估算。
//   - 异常失败路径（throw + unwind + catch）真实延迟
//   - std::expected 错误返回路径真实延迟（无 unwind，~数 ns）
// 平台：MinGW GCC 13.1.0 -O2，TSC 2.395 GHz（本机校准，见 _ch120_coroutine_perf）。
//
// 关键：throw_path 的抛出条件依赖 volatile 全局 g_trigger，阻止编译器把
// "必然抛异常"优化成直接 return（否则测不到真实 unwind 成本）。expected 路径
// 即使被优化为直接 return，也恰好反映"无异常机制、~数 ns"的廉价本质。
#include <iostream>
#include <expected>
#include <cstdint>
#include <x86intrin.h>

static inline uint64_t rdtsc() { return __rdtsc(); }
static const double TSC_GHZ = 2.395;
static volatile int g_trigger = 1;   // 防止编译器消除异常路径

[[gnu::noinline]] int throw_path() {
    try { if (g_trigger) throw 1; } catch (int e) { return e; }
    return 0;
}
[[gnu::noinline]] int expected_path() {
    std::expected<int,int> r = std::unexpected(1);
    if (!r) return r.error();
    return *r;
}

int main() {
    const int N = 1'000'000;
    volatile int sink = 0;
    uint64_t t0, t1;

    t0 = rdtsc(); for (int i = 0; i < N; ++i) sink += throw_path();   t1 = rdtsc();
    double exc_ns = (double)(t1 - t0) / N / TSC_GHZ;

    t0 = rdtsc(); for (int i = 0; i < N; ++i) sink += expected_path(); t1 = rdtsc();
    double exp_ns = (double)(t1 - t0) / N / TSC_GHZ;

    std::cout << "\n=== 实测（GCC 13.1 -O2, TSC " << TSC_GHZ << "GHz, N=" << N << ") ===" << std::endl;
    std::cout << "exception_throw_catch_ns : " << exc_ns << std::endl;
    std::cout << "expected_error_path_ns   : " << exp_ns << std::endl;
    std::cout << "speedup(失败路径)         : " << (exc_ns / exp_ns) << "x" << std::endl;
    std::cout << "[sink] " << sink << std::endl;
    return 0;
}
