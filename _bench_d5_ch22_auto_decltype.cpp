// _bench_d5_ch22_auto_decltype.cpp
// D5 benchmark: auto vs decltype(auto) — measure proxy type overhead & copy cost
#include <cstdio>
#include <chrono>
#include <vector>

volatile long g_sink = 0;

// === Test 1: vector<bool> proxy reference ===
[[gnu::noinline]] long bench_auto_proxy(int N) {
    std::vector<bool> vb(N, false);
    for (int i = 0; i < N; i += 2) vb[i] = true;
    long sum = 0;
    for (int i = 0; i < N; i++) {
        auto x = vb[i];      // auto → captures proxy reference, may defer materialization
        if (x) sum++;
    }
    g_sink ^= sum;
    return sum;
}

[[gnu::noinline]] long bench_explicit_bool(int N) {
    std::vector<bool> vb(N, false);
    for (int i = 0; i < N; i += 2) vb[i] = true;
    long sum = 0;
    for (int i = 0; i < N; i++) {
        bool x = vb[i];      // explicit bool forces immediate conversion
        if (x) sum++;
    }
    g_sink ^= sum;
    return sum;
}

// === Test 2: Big struct copy (decltype(auto) ref vs auto value) ===
struct Big { int data[128]; int compute() const { int s = 0; for (int i = 0; i < 128; i++) s += data[i]; return s; } };
struct Wrapper {
    Big b;
    Big& get_ref() { return b; }
    Big get_val() { return b; }  // copies
};

[[gnu::noinline]] int bench_auto_val(int N) {
    Wrapper w;
    int acc = 0;
    for (int i = 0; i < N; i++) {
        auto r = w.get_val();   // copies 128 ints each iteration
        r.data[0] = i;
        acc += r.compute();
    }
    g_sink ^= acc;
    return acc;
}

[[gnu::noinline]] int bench_decltype_ref(int N) {
    Wrapper w;
    int acc = 0;
    for (int i = 0; i < N; i++) {
        auto& r = w.get_ref();  // reference, no copy
        r.data[0] = i;
        acc += r.compute();
    }
    g_sink ^= acc;
    return acc;
}

int main() {
    const int N = 200000;

    volatile long w = bench_auto_proxy(1000);

    struct { const char* name; long (*fn)(int); double median; } tests_proxy[] = {
        {"auto (proxy ref)",      bench_auto_proxy,    0},
        {"explicit bool",          bench_explicit_bool, 0},
    };

    for (auto& t : tests_proxy) {
        double times[5];
        for (int trial = 0; trial < 5; trial++) {
            auto s = std::chrono::high_resolution_clock::now();
            volatile long r = t.fn(N);
            (void)r;
            auto e = std::chrono::high_resolution_clock::now();
            times[trial] = std::chrono::duration<double, std::milli>(e - s).count();
        }
        for (int i = 0; i < 5; i++)
            for (int j = i+1; j < 5; j++)
                if (times[j] < times[i]) { double tmp = times[i]; times[i] = times[j]; times[j] = tmp; }
        t.median = times[2];
    }

    struct { const char* name; int (*fn)(int); double median; } tests_big[] = {
        {"auto (copy 128 ints)",  bench_auto_val,      0},
        {"auto& (reference)",     bench_decltype_ref,  0},
    };

    for (auto& t : tests_big) {
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

    printf("=== ch22 auto_decltype D5 benchmark (N=%d, 5-trial median) ===\n", N);
    printf("  [vector<bool> proxy: auto vs bool]\n");
    for (auto& t : tests_proxy)
        printf("    %-25s  %8.2f ms\n", t.name, t.median);
    printf("  [Big struct: auto (copy) vs auto& (ref)]\n");
    for (auto& t : tests_big)
        printf("    %-25s  %8.2f ms\n", t.name, t.median);

    g_sink = tests_proxy[1].median > 0 ? 1 : 0;
    return 0;
}
