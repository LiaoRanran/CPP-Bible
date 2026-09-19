// _bench_d5_ch138_behavioral.cpp
// D5 benchmark: Strategy via virtual vs std::variant visit vs if constexpr vs function pointer
#include <cstdio>
#include <chrono>
#include <variant>
#include <functional>

volatile int g_sink = 0;

struct Data { int a, b; };

// --- Virtual strategy ---
class Strat {
public:
    virtual int apply(const Data& d) const = 0;
    virtual ~Strat() = default;
};
class SAdd : public Strat {
public:
    int apply(const Data& d) const override { return d.a + d.b; }
};
class SMul : public Strat {
public:
    int apply(const Data& d) const override { return d.a * d.b; }
};

[[gnu::noinline]] Strat* get_strat(int id) {
    static SAdd sa; static SMul sm;
    return id == 0 ? (Strat*)&sa : (Strat*)&sm;
}

[[gnu::noinline]] int bench_virtual(const Data& d, int N) {
    Strat* s = get_strat(0);
    int acc = 0;
    for (int i = 0; i < N; i++) acc += s->apply(d);
    return acc;
}

// --- std::variant + visit ---
using VArith = std::variant<SAdd, SMul>;

[[gnu::noinline]] int bench_variant_visit(const Data& d, int N) {
    VArith v{SAdd{}};
    int acc = 0;
    for (int i = 0; i < N; i++) {
        acc += std::visit([&](const auto& s) { return s.apply(d); }, v);
    }
    return acc;
}

// --- if constexpr ---
template<int Id>
int bench_if_constexpr(const Data& d, int N) {
    int acc = 0;
    for (int i = 0; i < N; i++) {
        if constexpr (Id == 0) acc += d.a + d.b;
        else acc += d.a * d.b;
    }
    return acc;
}

// --- function pointer ---
int fn_add(const Data& d) { return d.a + d.b; }
[[gnu::noinline]] int bench_fnptr(const Data& d, int N) {
    int (*fp)(const Data&) = fn_add;
    int acc = 0;
    for (int i = 0; i < N; i++) acc += fp(d);
    return acc;
}

// --- std::function ---
[[gnu::noinline]] int bench_stdfunction(const Data& d, int N) {
    std::function<int(const Data&)> fn = [](const Data& dd) { return dd.a + dd.b; };
    int acc = 0;
    for (int i = 0; i < N; i++) acc += fn(d);
    return acc;
}

int main() {
    const int N = 100000000;
    Data d = {7, 13};

    volatile int w = bench_virtual(d, 1000);

    struct { const char* name; int (*fn)(const Data&, int); double median; } tests[] = {
        {"virtual",             bench_virtual,        0},
        {"std::variant visit",  bench_variant_visit,  0},
        {"function pointer",    bench_fnptr,          0},
        {"std::function",       bench_stdfunction,    0},
        {"if constexpr",        [](const Data& d, int N)->int{ return bench_if_constexpr<0>(d,N); }, 0},
    };

    for (auto& t : tests) {
        double times[5];
        for (int trial = 0; trial < 5; trial++) {
            auto s = std::chrono::high_resolution_clock::now();
            volatile int r = t.fn(d, N);
            (void)r;
            auto e = std::chrono::high_resolution_clock::now();
            times[trial] = std::chrono::duration<double, std::milli>(e - s).count();
        }
        for (int i = 0; i < 5; i++)
            for (int j = i+1; j < 5; j++)
                if (times[j] < times[i]) { double tmp = times[i]; times[i] = times[j]; times[j] = tmp; }
        t.median = times[2];
    }

    printf("=== ch138 behavioral D5 benchmark (N=%d, 5-trial median) ===\n", N);
    for (auto& t : tests)
        printf("  %-25s  %8.2f ms  (%5.2fx)\n", t.name, t.median, t.median / tests[4].median);

    g_sink = tests[4].median > 0 ? 1 : 0;
    return 0;
}
