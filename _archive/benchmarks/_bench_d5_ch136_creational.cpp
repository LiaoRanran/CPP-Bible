// _bench_d5_ch136_creational.cpp
// D5 benchmark: factory method (virtual) vs template factory vs direct construction
#include <cstdio>
#include <chrono>

volatile int g_sink = 0;

struct Product {
    int type_id;
    int data[8];
    int compute() const { int s = 0; for (int i = 0; i < 8; i++) s += data[i]; return s; }
};

// Direct construction (baseline)
[[gnu::noinline]] int bench_direct(int N) {
    int acc = 0;
    for (int i = 0; i < N; i++) {
        Product p;
        p.type_id = i & 3;
        for (int j = 0; j < 8; j++) p.data[j] = j;
        acc += p.compute();
    }
    return acc;
}

// Virtual factory
class FactoryBase {
public:
    virtual ~FactoryBase() = default;
    virtual Product create() const = 0;
};
class FactoryA : public FactoryBase {
public:
    Product create() const override {
        Product p; p.type_id = 0;
        for (int j = 0; j < 8; j++) p.data[j] = j;
        return p;
    }
};

[[gnu::noinline]] FactoryBase* get_factory() {
    static FactoryA fa;
    return (FactoryBase*)&fa;
}

[[gnu::noinline]] int bench_virtual_factory(int N) {
    FactoryBase* f = get_factory();
    int acc = 0;
    for (int i = 0; i < N; i++) {
        Product p = f->create();
        acc += p.compute();
    }
    return acc;
}

// Template factory (compile-time)
template<typename F>
[[gnu::noinline]] int bench_template_factory(int N, F factory) {
    int acc = 0;
    for (int i = 0; i < N; i++) {
        Product p = factory();
        acc += p.compute();
    }
    return acc;
}

// Function pointer factory
using CreateFn = Product(*)();
Product make_product() {
    Product p; p.type_id = 0;
    for (int j = 0; j < 8; j++) p.data[j] = j;
    return p;
}

[[gnu::noinline]] int bench_fnptr_factory(int N) {
    CreateFn f = make_product;
    int acc = 0;
    for (int i = 0; i < N; i++) {
        Product p = f();
        acc += p.compute();
    }
    return acc;
}

int main() {
    const int N = 5000000;

    volatile int w = bench_direct(1000);

    struct { const char* name; int (*fn)(int); double median; } tests[] = {
        {"direct construction",      bench_direct,          0},
        {"virtual factory",          bench_virtual_factory, 0},
        {"fn pointer factory",       bench_fnptr_factory,   0},
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

    // Template factory
    auto lam = []() {
        Product p; p.type_id = 0;
        for (int j = 0; j < 8; j++) p.data[j] = j;
        return p;
    };
    double times[5];
    for (int trial = 0; trial < 5; trial++) {
        auto s = std::chrono::high_resolution_clock::now();
        volatile int r = bench_template_factory(N, lam);
        (void)r;
        auto e = std::chrono::high_resolution_clock::now();
        times[trial] = std::chrono::duration<double, std::milli>(e - s).count();
    }
    for (int i = 0; i < 5; i++)
        for (int j = i+1; j < 5; j++)
            if (times[j] < times[i]) { double tmp = times[i]; times[i] = times[j]; times[j] = tmp; }
    double tm = times[2];

    printf("=== ch136 creational D5 benchmark (N=%d, 5-trial median) ===\n", N);
    for (auto& t : tests)
        printf("  %-25s  %8.2f ms  (%5.1fx)\n", t.name, t.median, t.median / tests[0].median);
    printf("  %-25s  %8.2f ms  (%5.1fx)\n", "template factory", tm, tm / tests[0].median);

    g_sink = tests[2].median > 0 ? 1 : 0;
    return 0;
}
