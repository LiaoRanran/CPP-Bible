// _bench_d5_ch135_patterns_intro.cpp
// D5 benchmark: strategy pattern — virtual vs template vs switch
// All functions do real work (opaque data) to prevent DCE
#include <cstdio>
#include <chrono>

volatile long g_sink = 0;

struct Data { int x, y, z; };

// Virtual strategy (runtime polymorphism) — forces indirect call
class StrategyBase {
public:
    virtual ~StrategyBase() = default;
    virtual int apply(const Data& d) const = 0;
};
class AddStrat : public StrategyBase {
public:
    int apply(const Data& d) const override { return d.x + d.y + d.z; }
};
class MulStrat : public StrategyBase {
public:
    int apply(const Data& d) const override { return d.x * d.y * d.z; }
};

[[gnu::noinline]] StrategyBase* get_strat(int sel) {
    static AddStrat add;
    static MulStrat mul;
    return sel ? (StrategyBase*)&mul : (StrategyBase*)&add;
}

[[gnu::noinline]] long bench_virtual_strategy(int N) {
    Data d = {7, 13, 19};
    StrategyBase* s = get_strat(g_sink);
    long acc = 0;
    for (int i = 0; i < N; i++) {
        acc += s->apply(d);
    }
    g_sink ^= acc;
    return acc;
}

// Template strategy — fully inlined, but does real multiplication
template<typename S>
[[gnu::noinline]] long bench_template_strategy_t(int N) {
    Data d = {7, 13, 19};
    S strat;
    long acc = 0;
    for (int i = 0; i < N; i++) {
        acc += strat(d);
    }
    g_sink ^= acc;
    return acc;
}

struct TMul { int operator()(const Data& d) const { return d.x * d.y * d.z; } };

// Switch dispatch
[[gnu::noinline]] long bench_switch_dispatch(int N) {
    Data d = {7, 13, 19};
    int sel = g_sink;
    long acc = 0;
    for (int i = 0; i < N; i++) {
        switch (sel) {
            case 0: acc += d.x + d.y + d.z; break;
            case 1: acc += d.x * d.y * d.z; break;
            default: acc += 0; break;
        }
    }
    g_sink ^= acc;
    return acc;
}

int main() {
    const int N = 500000000;

    volatile long w = bench_switch_dispatch(1000);

    struct { const char* name; long (*fn)(int); double median; } tests[] = {
        {"virtual strategy",       bench_virtual_strategy,             0},
        {"raw switch",             bench_switch_dispatch,              0},
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

    // Template strategy (separate since it's templated)
    double times[5];
    for (int trial = 0; trial < 5; trial++) {
        auto s = std::chrono::high_resolution_clock::now();
        volatile long r = bench_template_strategy_t<TMul>(N);
        (void)r;
        auto e = std::chrono::high_resolution_clock::now();
        times[trial] = std::chrono::duration<double, std::milli>(e - s).count();
    }
    for (int i = 0; i < 5; i++)
        for (int j = i+1; j < 5; j++)
            if (times[j] < times[i]) { double tmp = times[i]; times[i] = times[j]; times[j] = tmp; }
    double tm = times[2];

    printf("=== ch135 patterns_intro D5 benchmark (N=%d, 5-trial median) ===\n", N);
    for (auto& t : tests)
        printf("  %-25s  %8.2f ms\n", t.name, t.median);
    printf("  %-25s  %8.2f ms\n", "template strategy", tm);

    g_sink = tests[1].median > 0 ? 1 : 0;
    return 0;
}
