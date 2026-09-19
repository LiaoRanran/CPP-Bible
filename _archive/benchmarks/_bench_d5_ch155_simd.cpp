// _bench_d5_ch155_simd.cpp — 附录 D5 基准：SIMD 向量化的真实收益（ch155）
// 编译（注意：本文件需要 -mavx2，因含 AVX2 intrinsics 路径）:
//   C:/Qt/Tools/mingw1530_64/bin/g++.EXE -O2 -std=c++23 -mavx2 _bench_d5_ch155_simd.cpp -o _bench_d5_ch155_simd.exe
// 方法学:
//   - 每个场景跑 5 轮取中位数，单轮 >= 数十 ms
//   - 数据用运行期随机数填充，防止编译器闭式折叠
//   - 结果累加到 volatile sink，防止 DCE
//   - 标量基线用 #pragma GCC novector 禁止向量化（GCC 15 -O2 默认已开启自动向量化）
//   - 注意: 整个文件用 -mavx2 编译, 因此"自动向量化"路径也是 AVX2 指令;
//     纯 -O2 (SSE2) 自动向量化的数字见正文表格中单独用无 -mavx2 编译测得的行。
#include <algorithm>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <random>
#include <vector>
#if defined(__AVX2__)
#include <immintrin.h>
#endif

using Clock = std::chrono::steady_clock;

static volatile float  g_sinkf = 0.0f;
static volatile std::uint64_t g_sinku = 0;

static double ms_since(Clock::time_point t0) {
    return std::chrono::duration<double, std::milli>(Clock::now() - t0).count();
}

static double median5(double a[5]) {
    std::sort(a, a + 5);
    return a[2];
}

// ---------- 场景 1：float 乘加 y[i] += a*x[i]（saxpy 形） ----------
__attribute__((noinline))
void saxpy_scalar(float a, const float* x, float* y, std::size_t n) {
#pragma GCC novector
    for (std::size_t i = 0; i < n; ++i) y[i] += a * x[i];
}

__attribute__((noinline))
void saxpy_auto(float a, const float* x, float* y, std::size_t n) {
    for (std::size_t i = 0; i < n; ++i) y[i] += a * x[i];
}

#if defined(__AVX2__)
__attribute__((noinline))
void saxpy_avx2(float a, const float* x, float* y, std::size_t n) {
    const __m256 va = _mm256_set1_ps(a);
    std::size_t i = 0;
    for (; i + 8 <= n; i += 8) {
        __m256 vx = _mm256_loadu_ps(x + i);
        __m256 vy = _mm256_loadu_ps(y + i);
        vy = _mm256_add_ps(vy, _mm256_mul_ps(va, vx));   // -O2 -mavx2 无 FMA 合并, 与标量语义一致
        _mm256_storeu_ps(y + i, vy);
    }
    for (; i < n; ++i) y[i] += a * x[i];
}
#endif

// ---------- 场景 2：float 求和归约 ----------
__attribute__((noinline))
float sum_scalar(const float* x, std::size_t n) {
    float s = 0.0f;
#pragma GCC novector
    for (std::size_t i = 0; i < n; ++i) s += x[i];
    return s;
}

// 浮点求和默认不许重结合, 需要局部放开 fast-math 才能自动向量化归约
__attribute__((noinline, optimize("fast-math")))
float sum_auto_fastmath(const float* x, std::size_t n) {
    float s = 0.0f;
    for (std::size_t i = 0; i < n; ++i) s += x[i];
    return s;
}

#if defined(__AVX2__)
__attribute__((noinline))
float sum_avx2(const float* x, std::size_t n) {
    __m256 acc = _mm256_setzero_ps();
    std::size_t i = 0;
    for (; i + 8 <= n; i += 8) acc = _mm256_add_ps(acc, _mm256_loadu_ps(x + i));
    alignas(32) float tmp[8];
    _mm256_store_ps(tmp, acc);
    float s = tmp[0] + tmp[1] + tmp[2] + tmp[3] + tmp[4] + tmp[5] + tmp[6] + tmp[7];
    for (; i < n; ++i) s += x[i];
    return s;
}
#endif

// ---------- 场景 3：分支写法 vs 无分支写法（条件累加） ----------
__attribute__((noinline))
std::uint64_t cond_branch(const int* x, std::size_t n) {
    std::uint64_t s = 0;
#pragma GCC novector
    for (std::size_t i = 0; i < n; ++i) {
        if (x[i] > 500) s += static_cast<std::uint32_t>(x[i]);   // 随机数据 -> 分支预测失败率高
    }
    return s;
}

__attribute__((noinline))
std::uint64_t cond_branchless(const int* x, std::size_t n) {
    std::uint64_t s = 0;
    for (std::size_t i = 0; i < n; ++i) {
        s += static_cast<std::uint32_t>(x[i]) * static_cast<std::uint32_t>(x[i] > 500);
    }
    return s;
}

int main() {
#if defined(__AVX2__)
    std::printf("built with __AVX2__\n");
#else
    std::printf("built WITHOUT AVX2 (SSE2 baseline)\n");
#endif

    std::mt19937 rng(std::random_device{}());
    constexpr std::size_t NF = 1u << 23;   // 8M float = 32 MB
    std::vector<float> x(NF), y(NF);
    std::uniform_real_distribution<float> df(0.0f, 1.0f);
    for (auto& v : x) v = df(rng);
    for (auto& v : y) v = df(rng);
    const float a = df(rng) + 0.5f;

    constexpr int REP = 8;                 // 每轮重复次数

    auto report = [](const char* name, double t[5]) {
        double c[5] = { t[0], t[1], t[2], t[3], t[4] };
        std::printf("%-34s rounds: %8.3f %8.3f %8.3f %8.3f %8.3f  median: %8.3f ms\n",
                    name, t[0], t[1], t[2], t[3], t[4], median5(c));
    };

    // --- 场景 1 ---
    double t1s[5], t1a[5], t1v[5];
    for (int r = 0; r < 5; ++r) {
        auto t0 = Clock::now();
        for (int k = 0; k < REP; ++k) saxpy_scalar(a, x.data(), y.data(), NF);
        t1s[r] = ms_since(t0);
        g_sinkf = g_sinkf + y[static_cast<std::size_t>(r)];
    }
    for (int r = 0; r < 5; ++r) {
        auto t0 = Clock::now();
        for (int k = 0; k < REP; ++k) saxpy_auto(a, x.data(), y.data(), NF);
        t1a[r] = ms_since(t0);
        g_sinkf = g_sinkf + y[static_cast<std::size_t>(r)];
    }
#if defined(__AVX2__)
    for (int r = 0; r < 5; ++r) {
        auto t0 = Clock::now();
        for (int k = 0; k < REP; ++k) saxpy_avx2(a, x.data(), y.data(), NF);
        t1v[r] = ms_since(t0);
        g_sinkf = g_sinkf + y[static_cast<std::size_t>(r)];
    }
#endif
    std::printf("\n-- scenario 1: saxpy y+=a*x, 8M float, %d passes/round --\n", REP);
    report("scalar (#pragma GCC novector)", t1s);
    report("auto-vectorized", t1a);
#if defined(__AVX2__)
    report("AVX2 intrinsics", t1v);
#endif

    // --- 场景 2 ---
    // y 已被场景 1 反复放大, 重新生成 [0,1) 数据用于求和
    // 每次调用前 volatile touch 输入, 防止 IPA pure-const 把 8 次同参调用 CSE 成 1 次
    for (auto& v : x) v = df(rng);
    auto touchf = [&x](int k) {
        volatile float* p = &x[static_cast<std::size_t>(k)];
        *p = *p;
    };
    double t2s[5], t2a[5], t2v[5];
    for (int r = 0; r < 5; ++r) {
        auto t0 = Clock::now();
        float s = 0.0f;
        for (int k = 0; k < REP; ++k) { touchf(k); s += sum_scalar(x.data(), NF); }
        t2s[r] = ms_since(t0);
        g_sinkf = g_sinkf + s;
    }
    for (int r = 0; r < 5; ++r) {
        auto t0 = Clock::now();
        float s = 0.0f;
        for (int k = 0; k < REP; ++k) { touchf(k); s += sum_auto_fastmath(x.data(), NF); }
        t2a[r] = ms_since(t0);
        g_sinkf = g_sinkf + s;
    }
#if defined(__AVX2__)
    for (int r = 0; r < 5; ++r) {
        auto t0 = Clock::now();
        float s = 0.0f;
        for (int k = 0; k < REP; ++k) { touchf(k); s += sum_avx2(x.data(), NF); }
        t2v[r] = ms_since(t0);
        g_sinkf = g_sinkf + s;
    }
#endif
    std::printf("\n-- scenario 2: sum reduction, 8M float, %d passes/round --\n", REP);
    report("scalar (novector, strict FP)", t2s);
    report("auto-vec (optimize fast-math)", t2a);
#if defined(__AVX2__)
    report("AVX2 intrinsics (8-way acc)", t2v);
#endif

    // --- 场景 3 ---
    constexpr std::size_t NI = 1u << 24;   // 16M int
    std::vector<int> xi(NI);
    std::uniform_int_distribution<int> di(0, 1000);
    for (auto& v : xi) v = di(rng);
    auto touchi = [&xi](int k) {
        volatile int* p = &xi[static_cast<std::size_t>(k)];
        *p = *p;
    };
    double t3b[5], t3n[5];
    for (int r = 0; r < 5; ++r) {
        auto t0 = Clock::now();
        std::uint64_t s = 0;
        for (int k = 0; k < 4; ++k) { touchi(k); s += cond_branch(xi.data(), NI); }
        t3b[r] = ms_since(t0);
        g_sinku += s;
    }
    for (int r = 0; r < 5; ++r) {
        auto t0 = Clock::now();
        std::uint64_t s = 0;
        for (int k = 0; k < 4; ++k) { touchi(k); s += cond_branchless(xi.data(), NI); }
        t3n[r] = ms_since(t0);
        g_sinku += s;
    }
    std::printf("\n-- scenario 3: conditional sum, 16M int, 4 passes/round --\n");
    report("branchy (novector)", t3b);
    report("branchless (auto-vec)", t3n);

    std::printf("\nsinkf=%f sinku=%llu\n", static_cast<double>(g_sinkf),
                static_cast<unsigned long long>(g_sinku));
    return 0;
}
