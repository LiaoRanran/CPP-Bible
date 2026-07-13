// B8 benchmark: smart pointer dispatch / allocation latency (MinGW GCC 13.1.0 -O2 x86_64)
// RDTSC micro-benchmark. TSC frequency calibrated by busy spin against steady_clock.
#include <cstdio>
#include <cstdint>
#include <chrono>
#include <memory>

static inline uint64_t rdtsc() {
    unsigned int lo, hi;
    __asm__ __volatile__("rdtsc" : "=a"(lo), "=d"(hi));
    return ((uint64_t)hi << 32) | lo;
}

// calibrate TSC -> ns (spin ~100ms against steady_clock)
static double tsc_ghz() {
    using namespace std::chrono;
    auto t0 = steady_clock::now();
    uint64_t c0 = rdtsc();
    while (duration_cast<milliseconds>(steady_clock::now() - t0).count() < 100) {}
    uint64_t c1 = rdtsc();
    auto t1 = steady_clock::now();
    double sec = std::chrono::duration<double>(t1 - t0).count();
    return (double)(c1 - c0) / sec / 1e9; // GHz
}

static volatile uint64_t g_sink = 0;

// ---- noinline anchors (prevent optimizer from eliminating) ----
[[gnu::noinline]] uint64_t probe_unique_deref(const std::unique_ptr<int>& up, int n) {
    uint64_t s = 0;
    for (int i = 0; i < n; ++i) s += (uint64_t)(*up + i);  // deref unique_ptr (compiler uses internal ptr directly)
    return s;
}
[[gnu::noinline]] uint64_t probe_shared_copy(const std::shared_ptr<int>& sp, int n) {
    uint64_t s = 0;
    for (int i = 0; i < n; ++i) {
        std::shared_ptr<int> c = sp;  // copy ctor: atomic refcount inc
        s += c.use_count();
    }
    return s;  // forces copy to persist
}
[[gnu::noinline]] uint64_t probe_make_shared(int n) {
    uint64_t s = 0;
    for (int i = 0; i < n; ++i) {
        auto sp = std::make_shared<int>(i);  // single heap alloc + control block
        s += (uint64_t)sp.get();
        sp.reset();  // free (atomic dec + maybe dealloc)
    }
    return s;
}
[[gnu::noinline]] uint64_t probe_shared_from_new(int n) {
    uint64_t s = 0;
    for (int i = 0; i < n; ++i) {
        std::shared_ptr<int> sp(new int(i));  // TWO allocs: object + separate control block
        s += (uint64_t)sp.get();
        sp.reset();
    }
    return s;
}
[[gnu::noinline]] uint64_t probe_raw_new_delete(int n) {
    uint64_t s = 0;
    for (int i = 0; i < n; ++i) {
        int* p = new int(i);
        s += (uint64_t)p;
        delete p;
    }
    return s;
}

int main() {
    const int N = 1'000'000;
    double ghz = tsc_ghz();
    double ns_per_cycle = 1.0 / ghz;  // ns per CPU cycle
    printf("TSC_freq = %.3f GHz  (ns/cycle = %.4f)\n", ghz, ns_per_cycle);

    std::unique_ptr<int> up(new int(7));
    std::shared_ptr<int> sp(new int(7));

    // unique_deref
    g_sink += probe_unique_deref(up, 1000);  // warmup
    {
        uint64_t c0 = rdtsc(); uint64_t r = probe_unique_deref(up, N); uint64_t c1 = rdtsc();
        printf("%-22s : %8.3f ns/op\n", "unique_deref", (c1 - c0) * ns_per_cycle / N);
        g_sink += r;
    }
    // shared_copy
    g_sink += probe_shared_copy(sp, 1000);
    {
        uint64_t c0 = rdtsc(); uint64_t r = probe_shared_copy(sp, N); uint64_t c1 = rdtsc();
        printf("%-22s : %8.3f ns/op\n", "shared_copy", (c1 - c0) * ns_per_cycle / N);
        g_sink += r;
    }
    // make_shared
    g_sink += probe_make_shared(1000);
    {
        uint64_t c0 = rdtsc(); uint64_t r = probe_make_shared(N); uint64_t c1 = rdtsc();
        printf("%-22s : %8.3f ns/op\n", "make_shared", (c1 - c0) * ns_per_cycle / N);
        g_sink += r;
    }
    // shared_from_new
    g_sink += probe_shared_from_new(1000);
    {
        uint64_t c0 = rdtsc(); uint64_t r = probe_shared_from_new(N); uint64_t c1 = rdtsc();
        printf("%-22s : %8.3f ns/op\n", "shared_from_new", (c1 - c0) * ns_per_cycle / N);
        g_sink += r;
    }
    // raw_new_delete
    g_sink += probe_raw_new_delete(1000);
    {
        uint64_t c0 = rdtsc(); uint64_t r = probe_raw_new_delete(N); uint64_t c1 = rdtsc();
        printf("%-22s : %8.3f ns/op\n", "raw_new_delete", (c1 - c0) * ns_per_cycle / N);
        g_sink += r;
    }

    printf("sink=%llu\n", (unsigned long long)g_sink);
    return 0;
}
