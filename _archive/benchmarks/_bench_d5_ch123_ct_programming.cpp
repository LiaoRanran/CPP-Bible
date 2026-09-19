// _bench_d5_ch123_ct_programming.cpp
// Compile: C:/Qt/Tools/mingw1530_64/bin/g++.EXE -O2 -std=c++23 -o bench_d5_ch123 _bench_d5_ch123_ct_programming.cpp
// Benchmarks: constexpr / consteval / TMP vs runtime — compile-time moves cost to translation
// Platform: AMD Ryzen 9 7940HX, GCC 15.3.0 (MinGW-w64), 5 rounds median

#include <iostream>
#include <chrono>
#include <algorithm>
#include <numeric>
#include <random>
#include <array>
#include <cstddef>
#include <cstdint>
#include <cstdlib>
#include <vector>

// ---- Volatile sink: prevent the optimizer from eliminating measured work ----
volatile long long g_sink = 0;
volatile int g_seed = 0;

// ============================================================================
// Scenario 1: constexpr function CT vs RT — factorial
// ============================================================================
constexpr long long fact_ct(int n) {
    return n <= 1 ? 1 : n * fact_ct(n - 1);
}
static constexpr long long kFact12 = fact_ct(12);   // 479001600 — already in binary

long long fact_rt(int n) {
    if (n <= 1) return 1;
    long long r = 1;
    for (int i = 2; i <= n; ++i) r *= i;
    return r;
}

// ============================================================================
// Scenario 2: constexpr sorted array vs runtime std::sort
// ============================================================================
constexpr int SORT_N = 512;

constexpr std::array<int, SORT_N> make_sorted_ct() {
    std::array<int, SORT_N> a{};
    for (int i = 0; i < SORT_N; ++i)
        a[i] = (i * 7919 + 104729) % 10007;
    // constexpr bubble sort
    for (int i = 0; i < SORT_N - 1; ++i)
        for (int j = 0; j < SORT_N - 1 - i; ++j)
            if (a[j] > a[j + 1]) { int t = a[j]; a[j] = a[j + 1]; a[j + 1] = t; }
    return a;
}
constexpr auto kArraySorted = make_sorted_ct();

// ============================================================================
// Scenario 3: consteval vs constexpr — ensure no runtime fallback
// ============================================================================
consteval long long fibonacci_ce(int n) {
    long long a = 0, b = 1;
    for (int i = 0; i < n; ++i) { long long t = b; b = a + b; a = t; }
    return a;
}
constexpr long long fibonacci_cx(int n) {
    long long a = 0, b = 1;
    for (int i = 0; i < n; ++i) { long long t = b; b = a + b; a = t; }
    return a;
}
long long fibonacci_rt(int n) {
    long long a = 0, b = 1;
    for (int i = 0; i < n; ++i) { long long t = b; b = a + b; a = t; }
    return a;
}
static constexpr long long kFib40CE = []() consteval { return fibonacci_ce(40); }();
static constexpr long long kFib40CX = fibonacci_cx(40);

// ============================================================================
// Scenario 4: TMP recursion vs constexpr loop — fib(40)
// ============================================================================
template <int N> struct TMP_Fib {
    static constexpr long long value = TMP_Fib<N - 1>::value + TMP_Fib<N - 2>::value;
};
template <> struct TMP_Fib<0> { static constexpr long long value = 0; };
template <> struct TMP_Fib<1> { static constexpr long long value = 1; };

// ============================================================================
// Scenario 5: constexpr lookup table vs runtime computation — integer sqrt
// ============================================================================
constexpr int LUT_SZ = 256;

constexpr std::array<unsigned char, LUT_SZ> make_sqrt_lut() {
    std::array<unsigned char, LUT_SZ> a{};
    for (int i = 0; i < LUT_SZ; ++i) {
        int lo = 0, hi = i + 1;
        while (lo + 1 < hi) {
            int mid = (lo + hi) / 2;
            if (mid * mid <= i) lo = mid; else hi = mid;
        }
        a[i] = static_cast<unsigned char>(lo);
    }
    return a;
}
constexpr auto kSqrtLUT = make_sqrt_lut();

int isqrt_ct(int v) {
    if (v < 0) return 0;
    if (static_cast<unsigned>(v) < static_cast<unsigned>(LUT_SZ))
        return static_cast<int>(kSqrtLUT[static_cast<unsigned>(v)]);
    // fallback for out-of-range values
    int lo = 0, hi = v;
    while (lo + 1 < hi) { int mid = (lo + hi) / 2; if (mid * mid <= v) lo = mid; else hi = mid; }
    return lo;
}

int isqrt_pure(int v) {
    if (v < 0) return 0;
    int lo = 0, hi = v + 1;
    while (lo + 1 < hi) { int mid = (lo + hi) / 2; if (mid * mid <= v) lo = mid; else hi = mid; }
    return lo;
}

// ============================================================================
// Timing helper
// ============================================================================
using Clock = std::chrono::high_resolution_clock;
using Ms    = std::chrono::milliseconds;

double elapsed_ms(Clock::time_point start, Clock::time_point end) {
    return static_cast<double>(
        std::chrono::duration_cast<std::chrono::microseconds>(end - start).count()) / 1000.0;
}

// Run one scenario multiple rounds and print median
struct BenchResult {
    const double* data;
    int count;
};
double median_of(double* vals, int n) {
    std::nth_element(vals, vals + n / 2, vals + n);
    return vals[n / 2];
}

// ============================================================================
int main() {
    // Seed from runtime entropy to defeat any compile-time precomputation
    std::random_device rd;
    std::mt19937 rng(rd());
    volatile int seed = static_cast<int>(rng() % 1000000 + 1);
    g_seed = seed;

    constexpr long long ITER_CT  = 50'000'000LL;   // 50M iterations for CT paths (must be high)
    constexpr long long ITER_RT  = 5'000'000LL;    // 5M  for RT paths
    constexpr long long ITER_SORT = 5'000;         // sort + read whole array N times
    constexpr long long ITER_LUT  = 10'000'000LL;  // LUT or calc 10M times
    constexpr int NROUNDS = 5;

    // Pre-compute volatile inputs (so compiler cannot pre-compute arguments)
    volatile int vfact = (seed % 11) + 2;         // 2..12
    volatile int vfib  = (seed % 39) + 2;          // 2..40
    volatile int vsqrt = (seed % 250) + 5;         // 5..254

    std::cout << "=== D5 Benchmark: Compile-Time vs Runtime (GCC 15.3.0, -O2 -std=c++23) ===" << std::endl;
    std::cout << "Environment: AMD Ryzen 9 7940HX, MinGW-w64" << std::endl;
    std::cout << "seed=" << seed << std::endl;
    std::cout << std::endl;

    // Verify CT values are correct
    std::cout << "constexpr fact(12)  = " << kFact12 << std::endl;
    std::cout << "constexpr fib(40)   = " << kFib40CE << std::endl;
    std::cout << "TMP     fib(40)     = " << TMP_Fib<40>::value << std::endl;
    std::cout << "sorted-array[0]     = " << kArraySorted[0] << std::endl;
    std::cout << "sorted-array[511]   = " << kArraySorted[511] << std::endl;
    std::cout << std::endl;

    // ---------------------------------------------------------
    // Scenario 1: CT constant read vs RT factorial compute
    // ---------------------------------------------------------
    std::cout << "--- S1: constexpr constant vs runtime factorial ---" << std::endl;
    {
        double times[NROUNDS];

        // CT path: read a compile-time constant in a tight loop
        for (int r = 0; r < NROUNDS; ++r) {
            volatile long long local_sink = 0;
            auto t0 = Clock::now();
            for (long long i = 0; i < ITER_CT; ++i) {
                local_sink = local_sink + kFact12;
            }
            auto t1 = Clock::now();
            g_sink = local_sink;
            times[r] = elapsed_ms(t0, t1);
        }
        double md_ct = median_of(times, NROUNDS);
        std::cout << "  S1 CT (read constexpr 50M iters): " << md_ct << " ms" << std::endl;

        // RT path: compute factorial in a tight loop
        int fv = vfact;
        for (int r = 0; r < NROUNDS; ++r) {
            volatile long long local_sink = 0;
            auto t0 = Clock::now();
            for (long long i = 0; i < ITER_RT; ++i) {
                local_sink = local_sink + fact_rt(fv);
            }
            auto t1 = Clock::now();
            g_sink = local_sink;
            times[r] = elapsed_ms(t0, t1);
        }
        double md_rt = median_of(times, NROUNDS);
        std::cout << "  S1 RT (factorial 5M iters):       " << md_rt << " ms" << std::endl;

        // Normalize to per-iter
        double ct_per = md_ct * 1000000.0 / ITER_CT;   // ns
        double rt_per = md_rt * 1000000.0 / ITER_RT;
        std::cout << "  S1 per-item: CT=" << ct_per << " ns, RT=" << rt_per << " ns"
                  << " (speedup " << (rt_per / ct_per) << "x)" << std::endl;
    }
    std::cout << std::endl;

    // ---------------------------------------------------------
    // Scenario 2: CT sorted array read vs RT std::sort
    // ---------------------------------------------------------
    std::cout << "--- S2: constexpr sorted array vs runtime sort ---" << std::endl;
    {
        double times[NROUNDS];

        // CT path: read from pre-sorted constexpr array
        // Access every element with a dependency chain — the array is already in .rodata
        for (int r = 0; r < NROUNDS; ++r) {
            volatile long long local_sink = 0;
            auto t0 = Clock::now();
            for (int k = 0; k < ITER_SORT; ++k) {
                for (int i = 0; i < SORT_N; ++i) {
                    local_sink = local_sink + kArraySorted[i];
                }
            }
            auto t1 = Clock::now();
            g_sink = local_sink;
            times[r] = elapsed_ms(t0, t1);
        }
        double md_ct = median_of(times, NROUNDS);
        std::cout << "  S2 CT (read sorted " << SORT_N << " x " << ITER_SORT << "): " << md_ct << " ms" << std::endl;

        // RT path: generate array + sort each iteration
        std::array<int, SORT_N> arr;
        for (int r = 0; r < NROUNDS; ++r) {
            volatile long long local_sink = 0;
            auto t0 = Clock::now();
            for (int k = 0; k < ITER_SORT; ++k) {
                // Re-fill with deterministic shuffle (uses seed to prevent constant-prop)
                for (int i = 0; i < SORT_N; ++i)
                    arr[i] = (static_cast<int>(rng()) % 10007);
                std::sort(arr.begin(), arr.end());
                for (int i = 0; i < SORT_N; ++i)
                    local_sink = local_sink + arr[i];
            }
            auto t1 = Clock::now();
            g_sink = local_sink;
            times[r] = elapsed_ms(t0, t1);
        }
        double md_rt = median_of(times, NROUNDS);
        std::cout << "  S2 RT (fill+sort+read " << SORT_N << " x " << ITER_SORT << "): " << md_rt << " ms" << std::endl;
        std::cout << "  S2 RT/CT ratio: " << (md_rt / md_ct) << "x" << std::endl;
    }
    std::cout << std::endl;

    // ---------------------------------------------------------
    // Scenario 3: consteval vs constexpr (runtime path)
    // ---------------------------------------------------------
    std::cout << "--- S3: consteval vs constexpr runtime fallback ---" << std::endl;
    {
        double times[NROUNDS];

        // consteval result is a compile-time constant — measure reading it
        for (int r = 0; r < NROUNDS; ++r) {
            volatile long long local_sink = 0;
            auto t0 = Clock::now();
            for (long long i = 0; i < ITER_CT; ++i) {
                local_sink = local_sink + kFib40CE;
            }
            auto t1 = Clock::now();
            g_sink = local_sink;
            times[r] = elapsed_ms(t0, t1);
        }
        double md_ce = median_of(times, NROUNDS);
        std::cout << "  S3 CE (read consteval fib(40) " << (ITER_CT/1000000) << "M): " << md_ce << " ms" << std::endl;

        // constexpr called with volatile runtime input → actual computation
        int fv = vfib;
        for (int r = 0; r < NROUNDS; ++r) {
            volatile long long local_sink = 0;
            auto t0 = Clock::now();
            for (long long i = 0; i < ITER_RT; ++i) {
                local_sink = local_sink + fibonacci_cx(fv);
                // mutate fv slightly so each iteration differs (dependency chain)
                fv = fv > 10 ? fv - 1 : 10;
            }
            auto t1 = Clock::now();
            g_sink = local_sink;
            times[r] = elapsed_ms(t0, t1);
        }
        double md_cx = median_of(times, NROUNDS);
        std::cout << "  S3 CX (constexpr fib " << ITER_RT/1000000 << "M): " << md_cx << " ms" << std::endl;

        // constexpr with compile-time constant input (static_assert already validates)
        // The compiler likely computes this at compile-time even without constexpr var
        for (int r = 0; r < NROUNDS; ++r) {
            volatile long long local_sink = 0;
            auto t0 = Clock::now();
            for (long long i = 0; i < ITER_CT; ++i) {
                local_sink = local_sink + kFib40CX;
            }
            auto t1 = Clock::now();
            g_sink = local_sink;
            times[r] = elapsed_ms(t0, t1);
        }
        double md_cxct = median_of(times, NROUNDS);
        std::cout << "  S3 CX-CT (read constexpr fib(40) " << (ITER_CT/1000000) << "M): " << md_cxct << " ms" << std::endl;
    }
    std::cout << std::endl;

    // ---------------------------------------------------------
    // Scenario 4: TMP (compile-time constant) vs constexpr loop (runtime)
    // ---------------------------------------------------------
    std::cout << "--- S4: TMP recursion vs constexpr loop ---" << std::endl;
    {
        double times[NROUNDS];

        // TMP result is a compile-time constant — measure reading it
        constexpr long long kTMP40 = TMP_Fib<40>::value;
        for (int r = 0; r < NROUNDS; ++r) {
            volatile long long local_sink = 0;
            auto t0 = Clock::now();
            for (long long i = 0; i < ITER_CT; ++i) {
                local_sink = local_sink + kTMP40;
            }
            auto t1 = Clock::now();
            g_sink = local_sink;
            times[r] = elapsed_ms(t0, t1);
        }
        double md_tmp = median_of(times, NROUNDS);
        std::cout << "  S4 TMP (read TMP fib(40) " << (ITER_CT/1000000) << "M): " << md_tmp << " ms" << std::endl;

        // Runtime loop fib — constexpr function called at runtime
        int fv = vfib;
        for (int r = 0; r < NROUNDS; ++r) {
            volatile long long local_sink = 0;
            auto t0 = Clock::now();
            for (long long i = 0; i < ITER_RT; ++i) {
                local_sink = local_sink + fibonacci_rt(fv);
                fv = fv > 10 ? fv - 1 : 10;
            }
            auto t1 = Clock::now();
            g_sink = local_sink;
            times[r] = elapsed_ms(t0, t1);
        }
        double md_rt = median_of(times, NROUNDS);
        std::cout << "  S4 RT (iterative fib " << ITER_RT/1000000 << "M): " << md_rt << " ms" << std::endl;
    }
    std::cout << std::endl;

    // ---------------------------------------------------------
    // Scenario 5: constexpr LUT vs runtime computation
    // ---------------------------------------------------------
    std::cout << "--- S5: constexpr lookup table vs runtime isqrt ---" << std::endl;
    {
        double times[NROUNDS];

        // CT LUT path: array index lookup with bounds check
        volatile int vs = vsqrt;
        for (int r = 0; r < NROUNDS; ++r) {
            volatile long long local_sink = 0;
            auto t0 = Clock::now();
            for (long long i = 0; i < ITER_LUT; ++i) {
                local_sink = local_sink + isqrt_ct(vs);
                vs = (vs + 7) % 200 + 5;
            }
            auto t1 = Clock::now();
            g_sink = local_sink;
            times[r] = elapsed_ms(t0, t1);
        }
        double md_lut = median_of(times, NROUNDS);
        std::cout << "  S5 LUT (isqrt via LUT " << ITER_LUT/1000000 << "M): " << md_lut << " ms" << std::endl;

        // Pure computation path: binary search sqrt, no LUT
        vs = vsqrt;
        for (int r = 0; r < NROUNDS; ++r) {
            volatile long long local_sink = 0;
            auto t0 = Clock::now();
            for (long long i = 0; i < ITER_LUT; ++i) {
                local_sink = local_sink + isqrt_pure(vs);
                vs = (vs + 7) % 200 + 5;
            }
            auto t1 = Clock::now();
            g_sink = local_sink;
            times[r] = elapsed_ms(t0, t1);
        }
        double md_pure = median_of(times, NROUNDS);
        std::cout << "  S5 RT (isqrt pure calc " << ITER_LUT/1000000 << "M): " << md_pure << " ms" << std::endl;
        std::cout << "  S5 Pure/LUT ratio: " << (md_pure / md_lut) << "x" << std::endl;
    }
    std::cout << std::endl;

    // ---- Semantic correctness verification (no timing assertions) ----
    // S1: CT and RT should produce the same value
    if (kFact12 == fact_rt(12)) {
        std::cout << "[OK] S1: constexpr fact(12) == fact_rt(12)" << std::endl;
    } else {
        std::cout << "[FAIL] S1" << std::endl;
    }

    // S2: sorted array is monotonically non-decreasing
    bool sorted_ok = true;
    for (int i = 1; i < SORT_N; ++i) {
        if (kArraySorted[i] < kArraySorted[i - 1]) { sorted_ok = false; break; }
    }
    std::cout << (sorted_ok ? "[OK] S2: sorted array is monotonic" : "[FAIL] S2") << std::endl;

    // S3: fib(40) computed multiple ways produce the same value
    bool s3_ok = (kFib40CE == kFib40CX) && (kFib40CE == TMP_Fib<40>::value) && (kFib40CE == fibonacci_rt(40));
    std::cout << (s3_ok ? "[OK] S3: fib(40) same via CE/CX/TMP/RT" : "[FAIL] S3") << std::endl;

    // S5: isqrt_ct matches isqrt_pure for sample values
    bool s5_ok = true;
    for (int v = 0; v < LUT_SZ; ++v)
        if (isqrt_ct(v) != isqrt_pure(v)) { s5_ok = false; break; }
    std::cout << (s5_ok ? "[OK] S5: LUT matches pure calculation" : "[FAIL] S5") << std::endl;

    std::cout << std::endl;
    std::cout << "Done. volatile sink=" << g_sink << " seed=" << g_seed << std::endl;
    return 0;
}
