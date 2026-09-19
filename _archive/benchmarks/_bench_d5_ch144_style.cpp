// _bench_d5_ch144_style.cpp
// D5 benchmark: range-for element access — `auto` (copy) vs `const auto&` (ref)
// for a NON-TRIVIAL (heavy) element type. For tiny types (int) all forms are
// equivalent; the real, teachable cost appears only when the element is large
// enough that copying per-iteration dominates.
#include <cstdio>
#include <chrono>
#include <vector>

volatile int g_sink = 0;

struct Heavy {
    long long a, b, c, d, e, f, g, h; // 64 bytes
    long long head() const { return a; }
};

constexpr int SZ = 512;

[[gnu::noinline]] long long bench_copy(const std::vector<Heavy>& v) {
    long long acc = 0;
    for (auto h : v) acc += h.head();   // copies 64 bytes per element
    return acc;
}

[[gnu::noinline]] long long bench_ref(const std::vector<Heavy>& v) {
    long long acc = 0;
    for (const auto& h : v) acc += h.head(); // no copy
    return acc;
}

[[gnu::noinline]] long long bench_fwd(const std::vector<Heavy>& v) {
    long long acc = 0;
    for (auto&& h : v) acc += h.head(); // no copy, binds to const ref
    return acc;
}

[[gnu::noinline]] long long bench_index(const std::vector<Heavy>& v) {
    long long acc = 0;
    for (size_t i = 0; i < v.size(); i++) acc += v[i].head();
    return acc;
}

int main() {
    const int N = 2000000;
    std::vector<Heavy> v(SZ);
    for (int i = 0; i < SZ; i++) v[i].a = i;

    volatile long long w = bench_ref(v); (void)w;

    struct { const char* name; long long (*fn)(const std::vector<Heavy>&); double median; } tests[] = {
        {"const auto& (ref)",   bench_ref,   0},
        {"auto&& (fwd)",        bench_fwd,   0},
        {"index v[i]",          bench_index, 0},
        {"auto (copy)",         bench_copy,  0},
    };

    for (auto& t : tests) {
        double times[5];
        for (int trial = 0; trial < 5; trial++) {
            auto s = std::chrono::high_resolution_clock::now();
            for (int i = 0; i < N; i++) { volatile long long r = t.fn(v); (void)r; }
            auto e = std::chrono::high_resolution_clock::now();
            times[trial] = std::chrono::duration<double, std::milli>(e - s).count();
        }
        for (int i = 0; i < 5; i++)
            for (int j = i+1; j < 5; j++)
                if (times[j] < times[i]) { double tmp = times[i]; times[i] = times[j]; times[j] = tmp; }
        t.median = times[2];
    }

    printf("=== ch144 style D5 benchmark (Heavy=64B, vec=%d x %d iters, 5-trial median) ===\n", SZ, N);
    for (auto& t : tests)
        printf("  %-22s  %8.3f ms  (%5.2fx)\n", t.name, t.median, t.median / tests[0].median);

    g_sink = tests[3].median > 0 ? 1 : 0;
    return 0;
}
