// _bench_d5_ch23_namespace_adl.cpp
// D5 benchmark: ADL vs qualified call vs member — all forced to do real work
#include <cstdio>
#include <chrono>
#include <vector>
#include <numeric>

volatile long g_sink = 0;

namespace foo {
    struct Item { int x; int y; int z; };

    // Opaque function bodies — NOT inline, prevent full optimization
    [[gnu::noinline]] long compute(const Item& a, const Item& b, const Item& c) {
        return (long)a.x * b.y + (long)a.y * c.z + (long)b.x * c.x + (long)c.y * a.z;
    }
}

[[gnu::noinline]] long bench_adl(int N) {
    using namespace foo;
    Item a = {1, 2, 3}, b = {4, 5, 6}, c = {7, 8, 9};
    long sum = 0;
    for (int i = 0; i < N; i++) {
        sum += compute(a, b, c);  // ADL finds foo::compute
    }
    g_sink ^= sum;
    return sum;
}

[[gnu::noinline]] long bench_qualified(int N) {
    foo::Item a = {1, 2, 3}, b = {4, 5, 6}, c = {7, 8, 9};
    long sum = 0;
    for (int i = 0; i < N; i++) {
        sum += foo::compute(a, b, c);
    }
    g_sink ^= sum;
    return sum;
}

// Direct struct member with noinline body
struct DirectItem {
    int x, y, z;
    [[gnu::noinline]] long compute(const DirectItem& b, const DirectItem& c) const {
        return (long)x * b.y + (long)y * c.z + (long)b.x * c.x + (long)c.y * z;
    }
};

[[gnu::noinline]] long bench_member(int N) {
    DirectItem a = {1, 2, 3}, b = {4, 5, 6}, c = {7, 8, 9};
    long sum = 0;
    for (int i = 0; i < N; i++) {
        sum += a.compute(b, c);
    }
    g_sink ^= sum;
    return sum;
}

int main() {
    const int N = 50000000;

    volatile long w = bench_adl(1000);

    struct { const char* name; long (*fn)(int); double median; } tests[] = {
        {"ADL (unqualified)",      bench_adl,       0},
        {"qualified (foo::)",       bench_qualified, 0},
        {"member fn (no lookup)",   bench_member,    0},
    };

    for (auto& t : tests) {
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

    printf("=== ch23 namespace_adl D5 benchmark (N=%d, 5-trial median) ===\n", N);
    for (auto& t : tests)
        printf("  %-25s  %8.2f ms\n", t.name, t.median);

    g_sink = tests[2].median > 0 ? 1 : 0;
    return 0;
}
