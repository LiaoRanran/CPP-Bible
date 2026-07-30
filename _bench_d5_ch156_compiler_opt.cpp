// 真实基准 D5 — ch156 编译器优化（GCC 15.3.0）
// 维度：① 函数级 optimize("O0")/默认(-O2)/optimize("O3") 属性对照
//       ② noinline vs always_inline 对小函数热循环的影响
//       ③ [[likely]] / __builtin_expect 分支提示实测（预期差异极小，诚实标注）
// 防 DCE：所有结果累加到 volatile g_sink；数据运行期随机生成，编译器无法折叠。
#include <algorithm>
#include <chrono>
#include <cstdio>
#include <random>
#include <vector>

static volatile long g_sink = 0;

// ---------- 维度①：函数级优化等级属性 ----------
__attribute__((optimize("O0"), noinline))
long kernel_o0(long n, const long* d) {
    long s = 0;
    for (long i = 0; i < n; ++i) s += d[i] * i + (s >> 3);
    return s;
}
__attribute__((noinline))
long kernel_default(long n, const long* d) {   // 全局以 -O2 编译
    long s = 0;
    for (long i = 0; i < n; ++i) s += d[i] * i + (s >> 3);
    return s;
}
__attribute__((optimize("O3"), noinline))
long kernel_o3(long n, const long* d) {
    long s = 0;
    for (long i = 0; i < n; ++i) s += d[i] * i + (s >> 3);
    return s;
}

// ---------- 维度②：内联开关 ----------
__attribute__((noinline))
long step_noinline(long a, long b) { return a + b * 2 + (a >> 1); }
__attribute__((always_inline))
inline long step_alwaysinline(long a, long b) { return a + b * 2 + (a >> 1); }

long loop_noinline(long n, const long* d) {
    long s = 0;
    for (long i = 0; i < n; ++i) s = step_noinline(s, d[i]);
    return s;
}
long loop_alwaysinline(long n, const long* d) {
    long s = 0;
    for (long i = 0; i < n; ++i) s = step_alwaysinline(s, d[i]);
    return s;
}

// ---------- 维度③：分支提示 ----------
long branch_plain(long n, const long* d) {
    long c = 0;
    for (long i = 0; i < n; ++i) {
        if (d[i] >= 0) c += d[i]; else c -= d[i];
    }
    return c;
}
long branch_likely(long n, const long* d) {
    long c = 0;
    for (long i = 0; i < n; ++i) {
        if (d[i] >= 0) [[likely]] c += d[i]; else c -= d[i];
    }
    return c;
}
long branch_expect(long n, const long* d) {
    long c = 0;
    for (long i = 0; i < n; ++i) {
        if (__builtin_expect(d[i] >= 0, 1)) c += d[i]; else c -= d[i];
    }
    return c;
}

static double median(std::vector<double>& v) {
    std::sort(v.begin(), v.end());
    return v[v.size() / 2];
}

int main() {
    const long N1 = 5'000'000;     // 维度① 内核规模
    const long N2 = 60'000'000;    // 维度② 内联循环规模
    const long N3 = 200'000'000;   // 维度③ 分支循环规模

    // 运行期随机数据（强偏正，便于分支预测发挥），编译器无法折叠
    std::vector<long> d(N3, 0);
    std::mt19937_64 rng(20260730);
    std::uniform_int_distribution<long> dist(-1000, 100000); // ~99% 为正
    for (long i = 0; i < N3; ++i) d[i] = dist(rng);

    const int ROUNDS = 5;
    std::vector<double> r1, r2, r3, r4, r5, r6, r7, r8;

    for (int t = 0; t < ROUNDS; ++t) {
        auto t0 = std::chrono::steady_clock::now();
        g_sink += kernel_o0(N1, d.data());
        auto t1 = std::chrono::steady_clock::now();
        r1.push_back(std::chrono::duration<double, std::milli>(t1 - t0).count());

        t0 = std::chrono::steady_clock::now();
        g_sink += kernel_default(N1, d.data());
        t1 = std::chrono::steady_clock::now();
        r2.push_back(std::chrono::duration<double, std::milli>(t1 - t0).count());

        t0 = std::chrono::steady_clock::now();
        g_sink += kernel_o3(N1, d.data());
        t1 = std::chrono::steady_clock::now();
        r3.push_back(std::chrono::duration<double, std::milli>(t1 - t0).count());

        t0 = std::chrono::steady_clock::now();
        g_sink += loop_noinline(N2, d.data());
        t1 = std::chrono::steady_clock::now();
        r4.push_back(std::chrono::duration<double, std::milli>(t1 - t0).count());

        t0 = std::chrono::steady_clock::now();
        g_sink += loop_alwaysinline(N2, d.data());
        t1 = std::chrono::steady_clock::now();
        r5.push_back(std::chrono::duration<double, std::milli>(t1 - t0).count());

        t0 = std::chrono::steady_clock::now();
        g_sink += branch_plain(N3, d.data());
        t1 = std::chrono::steady_clock::now();
        r6.push_back(std::chrono::duration<double, std::milli>(t1 - t0).count());

        t0 = std::chrono::steady_clock::now();
        g_sink += branch_likely(N3, d.data());
        t1 = std::chrono::steady_clock::now();
        r7.push_back(std::chrono::duration<double, std::milli>(t1 - t0).count());

        t0 = std::chrono::steady_clock::now();
        g_sink += branch_expect(N3, d.data());
        t1 = std::chrono::steady_clock::now();
        r8.push_back(std::chrono::duration<double, std::milli>(t1 - t0).count());
    }

    auto dump = [](const char* name, std::vector<double>& v) {
        std::printf("%-14s", name);
        for (double x : v) std::printf(" %.2f", x);
        std::printf("  median=%.2f\n", median(v));
    };
    std::printf("g_sink=%ld\n", (long)g_sink);
    dump("kernel_O0", r1);
    dump("kernel_def", r2);
    dump("kernel_O3", r3);
    dump("noinline", r4);
    dump("always_inl", r5);
    dump("branch_plain", r6);
    dump("branch_likely", r7);
    dump("branch_expect", r8);
    return 0;
}
