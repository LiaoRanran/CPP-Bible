// Examples/_ch04_move_perf.cpp
// 真实实证：C++11 move 语义的底层成本（MinGW GCC 13.1.0 -O2, x86_64）
//
// 本文件双重用途：
//   1) 运行时基准：main() 实测 move vs copy 延迟，替换书中的 ~N 估算量级
//   2) 静态证据：mv_vec / cp_vec / mv_assign / mv_str / read_tl / write_tl / null_ptr
//      为 [[gnu::noinline]] 自由函数，g++ -S -O2 生成的 _ch04_move_perf.asm 用于
//      《现代 C++ 终极圣经》ch04_cpp11「附录 H：真实基准/汇编证据」的锚定块。
//
// 编译运行: g++ -O2 -std=c++17 _ch04_move_perf.cpp -o _ch04_move_perf && ./_ch04_move_perf
// 生成汇编: g++ -S -O2 -m64 _ch04_move_perf.cpp -o _ch04_move_perf.asm
//
// 计时策略：
//   * copy 成本（µs 级）≫ 计时器开销，用 std::chrono::steady_clock 单次计时即可。
//   * move 仅 3 指针交换（亚纳秒~低纳秒级），steady_clock（~20-40ns/次）无法分辨，
//     且对"3 个等价 vector 轮换"这类微基准，优化器会把整段移动消去。
//     故 move 改用 RDTSC，并强制经 [[gnu::noinline]] 的 mv_vec/mv_str 调用，
//     使每次移动都真实执行（测得值含一次函数调用开销，为偏大的上界；
//     纯 move 仅是调用内部的 3 条 mov，见附录 H 汇编）。扣除空循环基线得净周期。
//   所有数值随 CPU 微架构/频率/带宽变化，仅代表本机；倍数优势稳定。

#include <iostream>
#include <vector>
#include <string>
#include <chrono>
#include <cstdint>
#include <utility>
#include <x86intrin.h>

using steady_t = std::chrono::steady_clock;
static inline long long ns_now() {
    return std::chrono::duration_cast<std::chrono::nanoseconds>(
               steady_t::now().time_since_epoch()).count();
}
static inline uint64_t rdtsc() { return __rdtsc(); }

// 校准 TSC 频率（现代 Intel/AMD TSC 恒定，测一次即可）
static double tsc_ns_per_cycle() {
    auto s0 = steady_t::now(); uint64_t r0 = rdtsc();
    uint64_t r_start = rdtsc();
    while (rdtsc() - r_start < 300'000'000ULL) {}
    uint64_t r1 = rdtsc();
    auto s1 = steady_t::now();
    double secs = std::chrono::duration<double>(s1 - s0).count();
    double hz = double(r1 - r0) / secs;
    return 1'000'000'000.0 / hz;   // ns / cycle
}

// ---------------- 静态汇编证据函数（[[gnu::noinline]] 保证独立符号）----------------
[[gnu::noinline]] std::vector<int>  mv_vec(std::vector<int> src)  { return std::move(src); }
[[gnu::noinline]] std::vector<int>  cp_vec(const std::vector<int>& src) { return src; }
[[gnu::noinline]] void mv_assign(std::vector<int>& dst, std::vector<int>& src) { dst = std::move(src); }
[[gnu::noinline]] std::string mv_str(std::string src) { return std::move(src); }
thread_local int tl_var = 0;
[[gnu::noinline]] int  read_tl() { return tl_var; }
[[gnu::noinline]] void write_tl(int v) { tl_var = v; }
[[gnu::noinline]] int* null_ptr() { return nullptr; }

// ---------------- 运行时基准 ----------------
// move（亚纳秒级）：经 [[gnu::noinline]] 调用，RDTSC + 空循环基线扣除
static double bench_vec_move_call(int N, int K, int outer, double ns_per_cycle) {
    uint64_t base = 0;
    for (int o = 0; o < outer; ++o) {
        uint64_t t0 = rdtsc();
        for (int k = 0; k < K; ++k) __asm__ volatile("" : : : "memory");
        uint64_t t1 = rdtsc();
        base += (t1 - t0);
    }
    uint64_t total = 0; uint64_t sink = 0;
    for (int o = 0; o < outer; ++o) {
        std::vector<int> a(N, 42);
        uint64_t t0 = rdtsc();
        for (int k = 0; k < K; ++k) {
            std::vector<int> b = mv_vec(std::move(a));   // a 空, b 持缓冲
            a = mv_vec(std::move(b));                    // 缓冲交回 a（2 次 noinline 调用）
        }
        uint64_t t1 = rdtsc();
        total += (t1 - t0);
        sink += (uint64_t)a.data();
    }
    (void)sink;
    int64_t net = (int64_t)total - (int64_t)base;
    if (net < 0) net = 0;
    return double(net) / double(outer * 2 * K) * ns_per_cycle;   // 每次 move（调用+3mov）
}
static double bench_str_move_call(int bytes, int K, int outer, double ns_per_cycle) {
    uint64_t base = 0;
    for (int o = 0; o < outer; ++o) {
        uint64_t t0 = rdtsc();
        for (int k = 0; k < K; ++k) __asm__ volatile("" : : : "memory");
        uint64_t t1 = rdtsc();
        base += (t1 - t0);
    }
    uint64_t total = 0; uint64_t sink = 0;
    for (int o = 0; o < outer; ++o) {
        std::string a(bytes, 'x');
        uint64_t t0 = rdtsc();
        for (int k = 0; k < K; ++k) {
            std::string b = mv_str(std::move(a));
            a = mv_str(std::move(b));
        }
        uint64_t t1 = rdtsc();
        total += (t1 - t0);
        sink += (uint64_t)a.data();
    }
    (void)sink;
    int64_t net = (int64_t)total - (int64_t)base;
    if (net < 0) net = 0;
    return double(net) / double(outer * 2 * K) * ns_per_cycle;
}
// copy（µs 级）：steady_clock 单次计时
static double bench_vec_copy(int N, int iters) {
    long long total = 0; uint64_t sink = 0;
    for (int i = 0; i < iters; ++i) {
        std::vector<int> a(N, 42);
        long long t0 = ns_now();
        std::vector<int> b = a;
        long long t1 = ns_now();
        total += (t1 - t0);
        sink += (uint64_t)b.data() + b.size();
    }
    (void)sink;
    return double(total) / iters;
}
static double bench_str_copy(int bytes, int iters) {
    long long total = 0; uint64_t sink = 0;
    for (int i = 0; i < iters; ++i) {
        std::string a(bytes, 'x');
        long long t0 = ns_now();
        std::string b = a;
        long long t1 = ns_now();
        total += (t1 - t0);
        sink += (uint64_t)b.data() + b.size();
    }
    (void)sink;
    return double(total) / iters;
}

// noexcept move 对 vector realloc 的真实收益：
//   - 元素 move ctor 为 noexcept → realloc 时"移动"元素（浅，仅交换指针）
//   - 元素 move ctor 非 noexcept → 为强异常安全，realloc 时"深拷贝"元素
struct Owned {
    int* p;
    Owned() : p(new int[64]) {}
    Owned(const Owned& o) : p(new int[64]) { for (int i = 0; i < 64; ++i) p[i] = o.p[i]; }
    Owned(Owned&& o) noexcept : p(o.p) { o.p = nullptr; }
    ~Owned() { delete[] p; }
};
struct OwnedThrowing {
    int* p;
    OwnedThrowing() : p(new int[64]) {}
    OwnedThrowing(const OwnedThrowing& o) : p(new int[64]) { for (int i = 0; i < 64; ++i) p[i] = o.p[i]; }
    OwnedThrowing(OwnedThrowing&& o) : p(o.p) { o.p = nullptr; }   // 非 noexcept
    ~OwnedThrowing() { delete[] p; }
};
static double bench_realloc_noexcept(int N, int iters) {
    long long total = 0; uint64_t sink = 0;
    for (int i = 0; i < iters; ++i) {
        std::vector<Owned> v; v.reserve(N);
        for (int j = 0; j < N; ++j) v.push_back(Owned{});
        long long t0 = ns_now();
        v.push_back(Owned{});
        long long t1 = ns_now();
        total += (t1 - t0);
        sink += (uint64_t)v.data() + v.size();
    }
    (void)sink;
    return double(total) / iters;
}
static double bench_realloc_throwing(int N, int iters) {
    long long total = 0; uint64_t sink = 0;
    for (int i = 0; i < iters; ++i) {
        std::vector<OwnedThrowing> v; v.reserve(N);
        for (int j = 0; j < N; ++j) v.push_back(OwnedThrowing{});
        long long t0 = ns_now();
        v.push_back(OwnedThrowing{});
        long long t1 = ns_now();
        total += (t1 - t0);
        sink += (uint64_t)v.data() + v.size();
    }
    (void)sink;
    return double(total) / iters;
}

int main() {
    double ns_per_cycle = tsc_ns_per_cycle();
    std::cout << "=== ch04 move 语义真实基准 (MinGW GCC 13.1.0 -O2 x86_64) ===\n";
    std::cout << "[TSC] " << (1.0 / ns_per_cycle) << " GHz | "
              << "[注] 数值随 CPU/频率/带宽变化，仅代表本机；倍数优势稳定\n\n";

    double mv1m = bench_vec_move_call(1'000'000, 3000, 200, ns_per_cycle);
    double cp1m = bench_vec_copy(1'000'000, 200);
    std::cout << "[vector<int>(1M)]  move(含调用开销上界) = " << mv1m << " ns | copy = " << cp1m
              << " ns | (纯 move 仅 3 指针交换, 见附录 H 汇编)\n";

    double mv1k = bench_vec_move_call(1000, 4000, 150, ns_per_cycle);
    double cp1k = bench_vec_copy(1000, 50000);
    std::cout << "[vector<int>(1K)]   move(含调用开销上界) = " << mv1k << " ns | copy = " << cp1k
              << " ns\n";

    double mvs = bench_str_move_call(1024, 4000, 150, ns_per_cycle);
    double cps = bench_str_copy(1024, 50000);
    std::cout << "[string(1KB)]      move(含调用开销上界) = " << mvs << " ns | copy = " << cps
              << " ns\n";

    double rne = bench_realloc_noexcept(20000, 2000);
    double rth = bench_realloc_throwing(20000, 200);
    std::cout << "[realloc 20K 元素] Owned(noexcept move→浅移动) = " << rne << " ns | "
              << "OwnedThrowing(非noexcept→深拷贝) = " << rth << " ns | 比 ≈ "
              << (rth / rne) << "x\n";

    (void)mv_vec; (void)cp_vec; (void)mv_assign; (void)mv_str;
    (void)read_tl; (void)write_tl; (void)null_ptr;
    return 0;
}
