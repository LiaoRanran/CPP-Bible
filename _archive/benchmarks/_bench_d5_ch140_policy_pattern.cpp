// _bench_d5_ch140_policy_pattern.cpp
// D5 benchmark: Policy-based design (template) vs virtual policy vs std::function policy
#include <cstdio>
#include <chrono>
#include <functional>

volatile int g_sink = 0;

struct Data { int x, y; };

// --- Policy-based design (compile-time, template parameter) ---
template<typename Policy>
struct Host {
    int run(const Data& d, int N) const {
        int acc = 0;
        for (int i = 0; i < N; i++)
            acc += Policy::apply(d);
        return acc;
    }
};

struct PolicyMul { static int apply(const Data& d) { return d.x * d.y; } };
struct PolicyAdd { static int apply(const Data& d) { return d.x + d.y; } };

[[gnu::noinline]] int bench_policy_template(const Data& d, int N) {
    Host<PolicyMul> h;
    return h.run(d, N);
}

// --- Virtual policy ---
class VPolicy {
public:
    virtual int apply(const Data& d) const = 0;
    virtual ~VPolicy() = default;
};
class VMul : public VPolicy {
public:
    int apply(const Data& d) const override { return d.x * d.y; }
};

[[gnu::noinline]] VPolicy* get_vmul() {
    static VMul inst;
    return (VPolicy*)&inst;
}

[[gnu::noinline]] int bench_policy_virtual(const Data& d, int N) {
    VPolicy* p = get_vmul();
    int acc = 0;
    for (int i = 0; i < N; i++)
        acc += p->apply(d);
    return acc;
}

// --- std::function policy ---
[[gnu::noinline]] int bench_policy_stdfunction(const Data& d, int N) {
    std::function<int(const Data&)> fn = [](const Data& dd) { return dd.x * dd.y; };
    int acc = 0;
    for (int i = 0; i < N; i++)
        acc += fn(d);
    return acc;
}

// --- if constexpr compile-time dispatch ---
template<int Id>
int dispatch_if(const Data& d, int N) {
    int acc = 0;
    for (int i = 0; i < N; i++) {
        if constexpr (Id == 0) acc += d.x * d.y;
        else if constexpr (Id == 1) acc += d.x + d.y;
        else acc += d.x - d.y;
    }
    return acc;
}

int main() {
    const int N = 100000000;
    Data d = {7, 13};

    volatile int w = bench_policy_template(d, 1000);

    struct { const char* name; int (*fn)(const Data&, int); double median; } tests[] = {
        {"template policy",     bench_policy_template,    0},
        {"virtual policy",      bench_policy_virtual,     0},
        {"std::function policy",bench_policy_stdfunction, 0},
        {"if constexpr dispatch",[](const Data& d, int N) -> int { return dispatch_if<0>(d, N); }, 0},
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

    printf("=== ch140 policy_pattern D5 benchmark (N=%d, 5-trial median) ===\n", N);
    for (auto& t : tests)
        printf("  %-25s  %8.2f ms  (%5.2fx)\n", t.name, t.median, t.median / tests[0].median);

    g_sink = tests[3].median > 0 ? 1 : 0;
    return 0;
}
