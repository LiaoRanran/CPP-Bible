// _bench_d5_ch28_lifetime_ub.cpp
// D5 benchmark: safe lifetime (RAII) vs raw pointer + manual delete vs dangling
// Measures the overhead of correct lifetime management vs UB-prone patterns.
#include <cstdio>
#include <chrono>
#include <memory>

volatile int g_sink_val = 0;

struct Payload {
    int data[16];
    int compute() const { int s = 0; for (int i = 0; i < 16; i++) s += data[i] * (i+1); return s; }
};

// RAII managed unique_ptr allocation/deallocation
[[gnu::noinline]] int bench_unique_ptr(int N) {
    int acc = 0;
    for (int i = 0; i < N; i++) {
        auto p = std::make_unique<Payload>();
        p->data[0] = i;
        acc += p->compute();
    }
    return acc;
}

// Raw new/delete with correct lifetime
[[gnu::noinline]] int bench_raw_new_delete(int N) {
    int acc = 0;
    for (int i = 0; i < N; i++) {
        Payload* p = new Payload();
        p->data[0] = i;
        acc += p->compute();
        delete p;
    }
    return acc;
}

// Stack allocation (no heap) — optimal lifetime
[[gnu::noinline]] int bench_stack(int N) {
    int acc = 0;
    for (int i = 0; i < N; i++) {
        Payload p;
        p.data[0] = i;
        acc += p.compute();
    }
    return acc;
}

int main() {
    const int N = 500000;

    // Warmup
    volatile int w = bench_stack(1000);

    struct { const char* name; int (*fn)(int); double median; } tests[] = {
        {"stack (RAII auto)",     bench_stack,         0},
        {"unique_ptr (RAII heap)", bench_unique_ptr,   0},
        {"raw new/delete",        bench_raw_new_delete, 0},
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
        // bubble sort for median
        for (int i = 0; i < 5; i++)
            for (int j = i+1; j < 5; j++)
                if (times[j] < times[i]) { double tmp = times[i]; times[i] = times[j]; times[j] = tmp; }
        t.median = times[2];
    }

    printf("=== ch28 lifetime_ub D5 benchmark (N=%d, 5-trial median) ===\n", N);
    for (auto& t : tests)
        printf("  %-25s  %8.2f ms\n", t.name, t.median);

    g_sink_val = tests[2].median > 0 ? 1 : 0;
    return 0;
}
