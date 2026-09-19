// _bench_d5_ch141_di.cpp
// D5 benchmark: DI via template (compile-time) vs DI via virtual interface vs DI via std::function
#include <cstdio>
#include <chrono>
#include <functional>
#include <memory>

volatile int g_sink = 0;

struct Data { int x, y, z; };

// --- Template DI (compile-time binding) ---
template<typename Service>
struct Client {
    int run(const Data& d, int N) {
        Service svc;
        int acc = 0;
        for (int i =  0; i < N; i++) acc += svc.process(d);
        return acc;
    }
};
struct ConcreteSvc { int process(const Data& d) { return d.x * d.y + d.z; } };

[[gnu::noinline]] int bench_di_template(const Data& d, int N) {
    Client<ConcreteSvc> c;
    return c.run(d, N);
}

// --- Virtual interface DI ---
class IService {
public:
    virtual int process(const Data& d) = 0;
    virtual ~IService() = default;
};
class ConcreteV : public IService {
public:
    int process(const Data& d) override { return d.x * d.y + d.z; }
};

[[gnu::noinline]] IService* get_service() {
    static ConcreteV inst;
    return (IService*)&inst;
}

[[gnu::noinline]] int bench_di_virtual(const Data& d, int N) {
    IService* svc = get_service();
    int acc = 0;
    for (int i = 0; i < N; i++) acc += svc->process(d);
    return acc;
}

// --- std::function DI ---
[[gnu::noinline]] int bench_di_stdfunction(const Data& d, int N) {
    std::function<int(const Data&)> svc = [](const Data& dd) { return dd.x * dd.y + dd.z; };
    int acc = 0;
    for (int i = 0; i < N; i++) acc += svc(d);
    return acc;
}

// --- unique_ptr DI (virtual + heap) ---
[[gnu::noinline]] int bench_di_unique_ptr(const Data& d, int N) {
    auto svc = std::make_unique<ConcreteV>();
    int acc = 0;
    for (int i = 0; i < N; i++) acc += svc->process(d);
    return acc;
}

int main() {
    const int N = 100000000;
    Data d = {7, 13, 5};

    volatile int w = bench_di_template(d, 1000);

    struct { const char* name; int (*fn)(const Data&, int); double median; } tests[] = {
        {"template DI",          bench_di_template,     0},
        {"virtual DI (ref)",     bench_di_virtual,      0},
        {"std::function DI",     bench_di_stdfunction,  0},
        {"unique_ptr DI (heap)", bench_di_unique_ptr,   0},
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

    printf("=== ch141 DI D5 benchmark (N=%d, 5-trial median) ===\n", N);
    for (auto& t : tests)
        printf("  %-25s  %8.2f ms  (%5.2fx)\n", t.name, t.median, t.median / tests[0].median);

    g_sink = tests[3].median > 0 ? 1 : 0;
    return 0;
}
