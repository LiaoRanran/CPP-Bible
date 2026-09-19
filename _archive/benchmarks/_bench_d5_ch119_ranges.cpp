// _bench_d5_ch119_ranges.cpp
// Benchmark: Ranges views pipelines vs hand-written loops
// Compiler: GCC 15.3.0 (MinGW-w64)
// Flags: -O2 -std=c++23
// Methodology: 5 rounds, median, volatile sink, steady_clock

#include <iostream>
#include <vector>
#include <ranges>
#include <algorithm>
#include <numeric>
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <random>

#ifdef _WIN32
#include <windows.h>
#endif

// ---- volatile sink: prevent dead code elimination ----
volatile unsigned long long g_sink = 0;

// ---- median of 5 (double) ----
static double med5(double a[5]) {
    std::sort(a, a + 5);
    return a[2];
}

// ---- timer: floating-point milliseconds ----
using Clock = std::chrono::steady_clock;

template<typename F>
static double timed_ms(F&& f) {
    auto t0 = Clock::now();
    f();
    auto t1 = Clock::now();
    return std::chrono::duration<double, std::milli>(t1 - t0).count();
}

// ---- constants ----
constexpr int N = 10'000'000;
constexpr int N_SORT = 1'000'000;
constexpr int TAKE_N = 500'000;

// ================================================================
// Scenario 1: filter|transform (full scan) vs hand-written loop
// ================================================================
static unsigned long long sc1_ranges(const std::vector<int>& v) {
    unsigned long long s = 0;
    for (auto x : v
        | std::views::filter([](int i) { return i % 2 == 0; })
        | std::views::transform([](int i) -> long long { return (long long)i * i; }))
        s += (unsigned long long)x;
    return s;
}

static unsigned long long sc1_hand(const std::vector<int>& v) {
    unsigned long long s = 0;
    for (int i : v)
        if (i % 2 == 0) s += (unsigned long long)((long long)i * i);
    return s;
}

// ================================================================
// Scenario 2: filter|transform|take(N) (early termination)
// ================================================================
static unsigned long long sc2_ranges(const std::vector<int>& v) {
    unsigned long long s = 0;
    for (auto x : v
        | std::views::filter([](int i) { return i % 2 == 0; })
        | std::views::transform([](int i) -> long long { return (long long)i * i; })
        | std::views::take(TAKE_N))
        s += (unsigned long long)x;
    return s;
}

static unsigned long long sc2_hand(const std::vector<int>& v) {
    unsigned long long s = 0;
    int cnt = 0;
    for (int i : v) {
        if (i % 2 == 0) {
            s += (unsigned long long)((long long)i * i);
            if (++cnt == TAKE_N) break;
        }
    }
    return s;
}

// ================================================================
// Scenario 3: 4-level pipeline (filter|transform|filter|transform)
// ================================================================
static unsigned long long sc3_ranges(const std::vector<int>& v) {
    unsigned long long s = 0;
    for (auto x : v
        | std::views::filter([](int i) { return i % 2 == 0; })
        | std::views::transform([](int i) -> long long { return (long long)i * i; })
        | std::views::filter([](long long i) { return i > 100; })
        | std::views::transform([](long long i) -> long long { return i + 1; }))
        s += (unsigned long long)x;
    return s;
}

static unsigned long long sc3_hand(const std::vector<int>& v) {
    unsigned long long s = 0;
    for (int i : v) {
        if (i % 2 == 0) {
            long long sq = (long long)i * i;
            if (sq > 100) s += (unsigned long long)(sq + 1);
        }
    }
    return s;
}

// ================================================================
// Scenario 4: ranges::sort vs std::sort
// ================================================================

// ================================================================
// Scenario 5: views::iota|transform vs for loop
// ================================================================
static unsigned long long sc5_ranges() {
    unsigned long long s = 0;
    for (auto x : std::views::iota(0, N)
        | std::views::transform([](int i) -> long long { return (long long)i * i; }))
        s += (unsigned long long)x;
    return s;
}

static unsigned long long sc5_hand() {
    unsigned long long s = 0;
    for (int i = 0; i < N; ++i)
        s += (unsigned long long)((long long)i * i);
    return s;
}

// ================================================================
// main
// ================================================================
int main() {
#ifdef _WIN32
    // Reduce scheduling noise on Windows
    SetThreadPriority(GetCurrentThread(), THREAD_PRIORITY_HIGHEST);
#endif

    // Prepare data: 0..N-1 sequential
    std::vector<int> data(N);
    for (int i = 0; i < N; ++i) data[i] = i;

    // Prepare sort data: random
    std::mt19937 rng(42);
    std::vector<int> sort_master(N_SORT);
    for (int i = 0; i < N_SORT; ++i) sort_master[i] = (int)rng();

    std::printf("=== D5 Benchmark: Ranges Pipelines vs Hand-written Loops ===\n");
    std::printf("Compiler: GCC 15.3.0 (MinGW-w64), -O2 -std=c++23\n");
    std::printf("CPU: AMD Ryzen 9 7940HX\n");
    std::printf("Data: %d ints, Sort: %d ints, TakeN: %d\n", N, N_SORT, TAKE_N);
    std::printf("Timer: steady_clock (double ms), 5 rounds (median), volatile sink\n\n");

    // Warm up
    g_sink = sc1_ranges(data);
    g_sink = sc1_hand(data);
    g_sink = sc5_ranges();
    g_sink = sc5_hand();
    { auto tmp = sort_master; std::ranges::sort(tmp); std::sort(tmp.begin(), tmp.end()); }

    // --- Scenario 1: filter|transform (full scan) ---
    {
        double tr[5], th[5];
        for (int r = 0; r < 5; ++r) {
            tr[r] = timed_ms([&]{ g_sink = sc1_ranges(data); });
            th[r] = timed_ms([&]{ g_sink = sc1_hand(data); });
        }
        double mr = med5(tr), mh = med5(th);
        std::printf("[S1] filter|transform (full scan %d)\n", N);
        std::printf("     Ranges : %.3f ms\n", mr);
        std::printf("     Hand   : %.3f ms\n", mh);
        std::printf("     Ratio  : %.3f\n\n", mr / mh);
    }

    // --- Scenario 2: filter|transform|take(N) (early termination) ---
    {
        double tr[5], th[5];
        for (int r = 0; r < 5; ++r) {
            tr[r] = timed_ms([&]{ g_sink = sc2_ranges(data); });
            th[r] = timed_ms([&]{ g_sink = sc2_hand(data); });
        }
        double mr = med5(tr), mh = med5(th);
        std::printf("[S2] filter|transform|take(%d) (early termination)\n", TAKE_N);
        std::printf("     Ranges : %.3f ms\n", mr);
        std::printf("     Hand   : %.3f ms\n", mh);
        std::printf("     Ratio  : %.3f\n\n", mr / mh);
    }

    // --- Scenario 3: 4-level pipeline ---
    {
        double tr[5], th[5];
        for (int r = 0; r < 5; ++r) {
            tr[r] = timed_ms([&]{ g_sink = sc3_ranges(data); });
            th[r] = timed_ms([&]{ g_sink = sc3_hand(data); });
        }
        double mr = med5(tr), mh = med5(th);
        std::printf("[S3] 4-level pipeline (filter|transform|filter|transform)\n");
        std::printf("     Ranges : %.3f ms\n", mr);
        std::printf("     Hand   : %.3f ms\n", mh);
        std::printf("     Ratio  : %.3f\n\n", mr / mh);
    }

    // --- Scenario 4: ranges::sort vs std::sort ---
    {
        double tr[5], th[5];
        for (int r = 0; r < 5; ++r) {
            auto copy1 = sort_master;
            tr[r] = timed_ms([&]{ std::ranges::sort(copy1); });
            g_sink = (unsigned long long)copy1[0];

            auto copy2 = sort_master;
            th[r] = timed_ms([&]{ std::sort(copy2.begin(), copy2.end()); });
            g_sink = (unsigned long long)copy2[0];
        }
        double mr = med5(tr), mh = med5(th);
        std::printf("[S4] ranges::sort vs std::sort (%d random ints)\n", N_SORT);
        std::printf("     Ranges : %.3f ms\n", mr);
        std::printf("     Std    : %.3f ms\n", mh);
        std::printf("     Ratio  : %.3f\n\n", mr / mh);
    }

    // --- Scenario 5: iota|transform vs for loop ---
    {
        double tr[5], th[5];
        for (int r = 0; r < 5; ++r) {
            tr[r] = timed_ms([&]{ g_sink = sc5_ranges(); });
            th[r] = timed_ms([&]{ g_sink = sc5_hand(); });
        }
        double mr = med5(tr), mh = med5(th);
        std::printf("[S5] iota|transform vs for loop (%d)\n", N);
        std::printf("     Ranges : %.3f ms\n", mr);
        std::printf("     Hand   : %.3f ms\n", mh);
        std::printf("     Ratio  : %.3f\n\n", mr / mh);
    }

    std::printf("=== Done ===\n");
    return 0;
}
