// _bench_d5_ch121_contracts.cpp
// D5 benchmark: contract-style precondition checking (assert vs manual vs none)
// GCC 15.3.0 supports -fcontracts but we benchmark assert (portable equivalent)
#include <cstdio>
#include <chrono>
#include <cassert>

volatile int g_sink = 0;

[[gnu::noinline]] int bench_no_check(int N) {
    int acc = 0;
    for (int i = 0; i < N; i++) {
        int x = i;
        if (x < 0) x = 0;  // clamp without assert
        acc += x;
    }
    return acc;
}

[[gnu::noinline]] int bench_assert(int N) {
    int acc = 0;
    for (int i = 0; i < N; i++) {
        int x = i;
        assert(x >= 0);  // contract precondition
        acc += x;
    }
    return acc;
}

[[gnu::noinline]] int bench_manual_check(int N) {
    int acc = 0;
    for (int i = 0; i < N; i++) {
        int x = i;
        if (x < 0) {       // manual precondition: always false in release
            return -1;
        }
        acc += x;
    }
    return acc;
}

// If-check that stays in release (always true but compiler can't prove it)
[[gnu::noinline]] int bench_always_true_if(int N) {
    int acc = 0;
    for (int i = 0; i < N; i++) {
        int x = i;
        if (x < 0) return -1;
        if (x > 2000000000) return -2;
        acc += x;
    }
    return acc;
}

int main() {
    const int N = 100000000;

    volatile int w = bench_no_check(1000);

    struct { const char* name; int (*fn)(int); double median; } tests[] = {
        {"no check (baseline)",     bench_no_check,        0},
        {"assert (NDEBUG=off)",     bench_assert,          0},
        {"manual check (removable)", bench_manual_check,   0},
        {"always-true if (stays)",   bench_always_true_if, 0},
    };

    for (auto& t : tests) {
        double times[5];
        for (int trial = 0; trial < 5; trial++) {
            auto s = std::chrono::high_resolution_clock::now();
            volatile int r = t.fn(N);
            (void)r;
            auto e = std::chrono::high_resolution_clock::now();
            times[trial] = std::chrono::duration<double, std::milli>(e - s).count();
        }
        for (int i = 0; i < 5; i++)
            for (int j = i+1; j < 5; j++)
                if (times[j] < times[i]) { double tmp = times[i]; times[i] = times[j]; times[j] = tmp; }
        t.median = times[2];
    }

    printf("=== ch121 contracts D5 benchmark (N=%d, 5-trial median) ===\n", N);
    for (auto& t : tests)
        printf("  %-25s  %8.2f ms\n", t.name, t.median);

    g_sink = tests[3].median > 0 ? 1 : 0;
    return 0;
}
