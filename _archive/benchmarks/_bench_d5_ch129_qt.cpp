// _bench_d5_ch129_qt.cpp
// D5 benchmark: Qt-style signal-slot (std::function-based) vs direct call vs virtual callback vs raw function pointer
#include <cstdio>
#include <chrono>
#include <functional>
#include <vector>

volatile int g_sink = 0;

struct Event { int x, y; };

// --- Direct call (baseline) ---
[[gnu::noinline]] int bench_direct(const Event& e, int N) {
    int acc = 0;
    for (int i = 0; i < N; i++) acc += e.x + e.y;
    return acc;
}

// --- Function pointer callback ---
int handler_fn(const Event& e) { return e.x + e.y; }
[[gnu::noinline]] int bench_fnptr(const Event& e, int N) {
    int (*fn)(const Event&) = handler_fn;
    int acc = 0;
    for (int i = 0; i < N; i++) acc += fn(e);
    return acc;
}

// --- std::function (simulates Qt moc signal-slot binding) ---
[[gnu::noinline]] int bench_stdfunction(const Event& e, int N) {
    std::function<int(const Event&)> fn = [](const Event& ee) { return ee.x + ee.y; };
    int acc = 0;
    for (int i = 0; i < N; i++) acc += fn(e);
    return acc;
}

// --- Virtual slot (simulates QObject::emit -> QObject::slot) ---
class Slot {
public:
    virtual int process(const Event& e) = 0;
    virtual ~Slot() = default;
};
class ConcreteSlot : public Slot {
public:
    int process(const Event& e) override { return e.x + e.y; }
};

[[gnu::noinline]] Slot* get_slot() {
    static ConcreteSlot inst;
    return (Slot*)&inst;
}

[[gnu::noinline]] int bench_virtual_slot(const Event& e, int N) {
    Slot* s = get_slot();
    int acc = 0;
    for (int i = 0; i < N; i++) acc += s->process(e);
    return acc;
}

// --- std::function vector (simulates signal emitting to multiple slots) ---
[[gnu::noinline]] int bench_multi_slot(const Event& e, int N) {
    std::vector<std::function<int(const Event&)>> slots;
    slots.reserve(4);
    slots.push_back([](const Event& ee) { return ee.x + ee.y; });
    slots.push_back([](const Event& ee) { return ee.x + ee.y; });
    slots.push_back([](const Event& ee) { return ee.x + ee.y; });
    slots.push_back([](const Event& ee) { return ee.x + ee.y; });

    int acc = 0;
    for (int i = 0; i < N; i++) {
        for (auto& fn : slots) acc += fn(e);
    }
    return acc;
}

int main() {
    const int N = 100000000;
    Event e = {7, 13};

    volatile int w = bench_direct(e, 1000);

    struct { const char* name; int (*fn)(const Event&, int); double median; } tests[] = {
        {"direct call",           bench_direct,        0},
        {"function pointer",      bench_fnptr,         0},
        {"std::function (slot)",  bench_stdfunction,   0},
        {"virtual slot",          bench_virtual_slot,  0},
        {"multi-slot (4x)",       bench_multi_slot,    0},
    };

    for (auto& t : tests) {
        double times[5];
        for (int trial = 0; trial < 5; trial++) {
            auto s = std::chrono::high_resolution_clock::now();
            volatile int r = t.fn(e, N);
            (void)r;
            auto e2 = std::chrono::high_resolution_clock::now();
            times[trial] = std::chrono::duration<double, std::milli>(e2 - s).count();
        }
        for (int i = 0; i < 5; i++)
            for (int j = i+1; j < 5; j++)
                if (times[j] < times[i]) { double tmp = times[i]; times[i] = times[j]; times[j] = tmp; }
        t.median = times[2];
    }

    printf("=== ch129 qt D5 benchmark (N=%d, 5-trial median) ===\n", N);
    for (auto& t : tests)
        printf("  %-25s  %8.2f ms  (%5.2fx)\n", t.name, t.median, t.median / tests[0].median);

    g_sink = tests[4].median > 0 ? 1 : 0;
    return 0;
}
