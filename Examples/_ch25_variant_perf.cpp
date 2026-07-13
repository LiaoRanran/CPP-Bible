// B8 benchmark: std::variant visit vs virtual call DISPATCH latency, hot working set (L1)
// MinGW GCC 13.1.0 -O2 x86_64. Isolates pure dispatch (objects kept in cache).
#include <cstdio>
#include <cstdint>
#include <chrono>
#include <variant>
#include <vector>
#include <random>

static inline uint64_t rdtsc() {
    unsigned int lo, hi;
    __asm__ __volatile__("rdtsc" : "=a"(lo), "=d"(hi));
    return ((uint64_t)hi << 32) | lo;
}
static double tsc_ghz() {
    using namespace std::chrono;
    auto t0 = steady_clock::now(); uint64_t c0 = rdtsc();
    while (duration_cast<milliseconds>(steady_clock::now() - t0).count() < 100) {}
    uint64_t c1 = rdtsc(); auto t1 = steady_clock::now();
    double sec = duration<double>(t1 - t0).count();
    return (double)(c1 - c0) / sec / 1e9;
}
static volatile uint64_t g_sink = 0;

struct A { virtual int f() { return 1; } virtual ~A() = default; };
struct B : A { int f() override { return 2; } };
struct C : A { int f() override { return 3; } };
struct D : A { int f() override { return 4; } };
using Var = std::variant<int, long, double, char>;

// hot set of 4 objects + 4 variants, randomized dispatch to defeat BTB prediction
[[gnu::noinline]] uint64_t probe_variant_visit_hot(const Var* vv, const int* idx, int n) {
    uint64_t s = 0;
    for (int i = 0; i < n; ++i) s += std::visit([](auto&& x) -> int { return (int)x; }, vv[idx[i]]);
    return s;
}
[[gnu::noinline]] uint64_t probe_virtual_hot(A* const ps[4], const int* idx, int n) {
    uint64_t s = 0;
    for (int i = 0; i < n; ++i) s += ps[idx[i]]->f();
    return s;
}

int main() {
    const int N = 20'000'000;
    double ghz = tsc_ghz();
    double ns_per_cycle = 1.0 / ghz;
    printf("TSC_freq = %.3f GHz (ns/cycle=%.4f)\n", ghz, ns_per_cycle);

    A a; B b; C c; D d; A* ps[4] = { &a, &b, &c, &d };
    Var vv[4] = { 1, 2L, 3.0, (char)4 };
    std::vector<int> idx(N);
    std::mt19937 rng(1);
    for (int i = 0; i < N; ++i) idx[i] = rng() % 4;

    g_sink += probe_variant_visit_hot(vv, idx.data(), 1000);
    { uint64_t c0=rdtsc(); uint64_t r=probe_variant_visit_hot(vv, idx.data(), N); uint64_t c1=rdtsc();
      printf("%-20s : %8.3f ns/op\n", "variant_visit", (c1-c0)*ns_per_cycle/N); g_sink += r; }
    g_sink += probe_virtual_hot(ps, idx.data(), 1000);
    { uint64_t c0=rdtsc(); uint64_t r=probe_virtual_hot(ps, idx.data(), N); uint64_t c1=rdtsc();
      printf("%-20s : %8.3f ns/op\n", "virtual_call", (c1-c0)*ns_per_cycle/N); g_sink += r; }

    printf("sink=%llu\n", (unsigned long long)g_sink);
    return 0;
}
