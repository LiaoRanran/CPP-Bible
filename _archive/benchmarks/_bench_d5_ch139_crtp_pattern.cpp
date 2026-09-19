// _bench_d5_ch139_crtp_pattern.cpp
// D5 benchmark: CRTP static interface vs virtual interface vs free function
#include <cstdio>
#include <chrono>

volatile int g_sink = 0;

// CRTP static polymorphism
template<typename Derived>
struct CRTPInterface {
    int compute() const { return static_cast<const Derived*>(this)->compute_impl(); }
};
struct CRTPAdd : CRTPInterface<CRTPAdd> {
    int compute_impl() const { return 1 + 1; }
};

[[gnu::noinline]] int bench_crtp(int N) {
    CRTPAdd obj;
    int acc = 0;
    for (int i = 0; i < N; i++) {
        acc += obj.compute();
    }
    return acc;
}

// Virtual interface
class VInterface {
public:
    virtual ~VInterface() = default;
    virtual int compute() const = 0;
};
class VAdd : public VInterface {
public:
    int compute() const override { return 1 + 1; }
};

[[gnu::noinline]] VInterface* get_vobj() {
    static VAdd obj;
    return (VInterface*)&obj;
}

[[gnu::noinline]] int bench_virtual(int N) {
    VInterface* obj = get_vobj();
    int acc = 0;
    for (int i = 0; i < N; i++) {
        acc += obj->compute();
    }
    return acc;
}

// Direct function call
[[gnu::noinline]] int bench_direct_fn(int N) {
    int acc = 0;
    for (int i = 0; i < N; i++) {
        acc += 2;
    }
    return acc;
}

// std::function (type-erased)
#include <functional>

[[gnu::noinline]] int bench_stdfunction(int N) {
    std::function<int()> fn = []() { return 2; };
    int acc = 0;
    for (int i = 0; i < N; i++) {
        acc += fn();
    }
    return acc;
}

int main() {
    const int N = 50000000;

    volatile int w = bench_direct_fn(1000);

    struct { const char* name; int (*fn)(int); double median; } tests[] = {
        {"direct (trivial)",     bench_direct_fn,   0},
        {"CRTP",                 bench_crtp,        0},
        {"virtual",              bench_virtual,     0},
        {"std::function",        bench_stdfunction, 0},
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

    printf("=== ch139 crtp_pattern D5 benchmark (N=%d, 5-trial median) ===\n", N);
    for (auto& t : tests)
        printf("  %-25s  %8.2f ms  (%5.1fx)\n", t.name, t.median, t.median / tests[0].median);

    g_sink = tests[3].median > 0 ? 1 : 0;
    return 0;
}
