// _bench_d5_ch137_structural.cpp
// D5 benchmark: decorator pattern (runtime) vs CRTP (compile-time) vs direct
// Structural patterns: decorator, facade, adapter — measure indirection overhead
#include <cstdio>
#include <chrono>

volatile int g_sink = 0;

// === Direct (baseline) ===
struct Number { int v; };
[[gnu::noinline]] int bench_direct(int N) {
    Number n = {42};
    int acc = 0;
    for (int i = 0; i < N; i++) {
        acc += n.v;
    }
    return acc;
}

// === Virtual decorator (single indirection) ===
class NumBase {
public:
    virtual ~NumBase() = default;
    virtual int get() const = 0;
};
class NumImpl : public NumBase {
public:
    int v;
    NumImpl(int v_) : v(v_) {}
    int get() const override { return v; }
};
class NumDouble : public NumBase {
public:
    NumBase* inner;
    NumDouble(NumBase* i) : inner(i) {}
    int get() const override { return inner->get() * 2; }
};

[[gnu::noinline]] NumBase* get_num_dec() {
    static NumImpl impl(42);
    static NumDouble dec(&impl);
    return (NumBase*)&dec;
}

[[gnu::noinline]] int bench_virtual_dec(int N) {
    NumBase* n = get_num_dec();
    int acc = 0;
    for (int i = 0; i < N; i++) {
        acc += n->get();
    }
    return acc;
}

// === CRTP decorator (compile-time) ===
template<typename Derived>
struct CRTPBase {
    int get() const { return static_cast<const Derived*>(this)->get(); }
};
struct CRTPNum : CRTPBase<CRTPNum> {
    int v;
    int get() const { return v; }
};
struct CRTPImplement : CRTPBase<CRTPImplement> {
    int v;
    int get() const { return v; }
    CRTPImplement(int v_) : v(v_) {}
};

[[gnu::noinline]] int bench_crtp(int N) {
    CRTPImplement n(42);
    int acc = 0;
    for (int i = 0; i < N; i++) {
        acc += n.get();
    }
    return acc;
}

// === Template wrapper (static dispatch via lambda) ===
template<typename F>
[[gnu::noinline]] int bench_template_wrapper(int N, F fn) {
    int v = 42;
    int acc = 0;
    for (int i = 0; i < N; i++) {
        acc += fn(v);
    }
    return acc;
}

int main() {
    const int N = 50000000;

    volatile int w = bench_direct(1000);

    struct { const char* name; int (*fn)(int); double median; } tests[] = {
        {"direct",              bench_direct,        0},
        {"virtual decorator",   bench_virtual_dec,   0},
        {"CRTP",                bench_crtp,          0},
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

    // Template wrapper (special call form)
    double times[5];
    auto lam = [](int v) { return v; };
    for (int trial = 0; trial < 5; trial++) {
        auto s = std::chrono::high_resolution_clock::now();
        volatile int r = bench_template_wrapper(N, lam);
        (void)r;
        auto e = std::chrono::high_resolution_clock::now();
        times[trial] = std::chrono::duration<double, std::milli>(e - s).count();
    }
    for (int i = 0; i < 5; i++)
        for (int j = i+1; j < 5; j++)
            if (times[j] < times[i]) { double tmp = times[i]; times[i] = times[j]; times[j] = tmp; }
    double tm = times[2];

    printf("=== ch137 structural D5 benchmark (N=%d, 5-trial median) ===\n", N);
    for (auto& t : tests)
        printf("  %-25s  %8.2f ms  (%5.1fx)\n", t.name, t.median, t.median / tests[0].median);
    printf("  %-25s  %8.2f ms  (%5.1fx)\n", "template wrapper", tm, tm / tests[0].median);

    g_sink = tests[2].median > 0 ? 1 : 0;
    return 0;
}
