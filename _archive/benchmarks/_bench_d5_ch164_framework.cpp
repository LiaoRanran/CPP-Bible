// _bench_d5_ch164_framework.cpp
// D5 benchmark: Framework dispatch — virtual plugin vs CRTP static plugin vs function pointer callback
#include <cstdio>
#include <chrono>
#include <functional>

volatile int g_sink = 0;

struct Ctx { int x, y, z; };

// --- Virtual plugin interface ---
class Plugin {
public:
    virtual int handle(const Ctx& c) = 0;
    virtual ~Plugin() = default;
};
class PluginA : public Plugin {
public:
    int handle(const Ctx& c) override { return c.x * c.y + c.z; }
};

[[gnu::noinline]] Plugin* get_plugin() {
    static PluginA inst;
    return (Plugin*)&inst;
}

[[gnu::noinline]] int bench_virtual_plugin(const Ctx& c, int N) {
    Plugin* p = get_plugin();
    int acc = 0;
    for (int i = 0; i < N; i++) acc += p->handle(c);
    return acc;
}

// --- CRTP static plugin ---
template<typename Derived>
class StaticPlugin {
public:
    int handle(const Ctx& c) { return static_cast<Derived*>(this)->handle_impl(c); }
};
class StaticPluginA : public StaticPlugin<StaticPluginA> {
public:
    int handle_impl(const Ctx& c) { return c.x * c.y + c.z; }
};

[[gnu::noinline]] int bench_crtp_plugin(const Ctx& c, int N) {
    StaticPluginA p;
    int acc = 0;
    for (int i = 0; i < N; i++) acc += p.handle(c);
    return acc;
}

// --- Function pointer callback ---
int callback_fn(const Ctx& c) { return c.x * c.y + c.z; }

[[gnu::noinline]] int bench_fnptr_callback(const Ctx& c, int N) {
    int (*cb)(const Ctx&) = callback_fn;
    int acc = 0;
    for (int i = 0; i < N; i++) acc += cb(c);
    return acc;
}

// --- std::function callback ---
[[gnu::noinline]] int bench_stdfunction_callback(const Ctx& c, int N) {
    std::function<int(const Ctx&)> cb = [](const Ctx& cc) { return cc.x * cc.y + cc.z; };
    int acc = 0;
    for (int i = 0; i < N; i++) acc += cb(c);
    return acc;
}

int main() {
    const int N = 100000000;
    Ctx c = {7, 13, 5};

    volatile int w = bench_virtual_plugin(c, 1000);

    struct { const char* name; int (*fn)(const Ctx&, int); double median; } tests[] = {
        {"virtual plugin",      bench_virtual_plugin,      0},
        {"CRTP static plugin",  bench_crtp_plugin,         0},
        {"function pointer cb", bench_fnptr_callback,      0},
        {"std::function cb",    bench_stdfunction_callback,0},
    };

    for (auto& t : tests) {
        double times[5];
        for (int trial = 0; trial < 5; trial++) {
            auto s = std::chrono::high_resolution_clock::now();
            volatile int r = t.fn(c, N);
            (void)r;
            auto e = std::chrono::high_resolution_clock::now();
            times[trial] = std::chrono::duration<double, std::milli>(e - s).count();
        }
        for (int i = 0; i < 5; i++)
            for (int j = i+1; j < 5; j++)
                if (times[j] < times[i]) { double tmp = times[i]; times[i] = times[j]; times[j] = tmp; }
        t.median = times[2];
    }

    printf("=== ch164 framework D5 benchmark (N=%d, 5-trial median) ===\n", N);
    for (auto& t : tests)
        printf("  %-25s  %8.2f ms  (%5.2fx)\n", t.name, t.median, t.median / tests[1].median);

    g_sink = tests[3].median > 0 ? 1 : 0;
    return 0;
}
