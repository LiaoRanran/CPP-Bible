// _bench_d5_ch24_enum.cpp
// D5 benchmark: enum class vs C-style enum vs int — storage, switch dispatch
#include <cstdio>
#include <chrono>

volatile int g_sink = 0;

// enum class (scoped, type-safe)
enum class Op : int { Add, Sub, Mul, Div };

[[gnu::noinline]] int bench_enum_class(int N) {
    int acc = 0;
    for (int i = 0; i < N; i++) {
        Op op = static_cast<Op>(i & 3);
        switch (op) {
            case Op::Add: acc += i; break;
            case Op::Sub: acc -= i; break;
            case Op::Mul: acc ^= i; break;
            case Op::Div: acc += (i >> 1); break;
        }
    }
    return acc;
}

// C-style enum (unscoped)
enum COp { CAdd, CSub, CMul, CDiv };

[[gnu::noinline]] int bench_c_enum(int N) {
    int acc = 0;
    for (int i = 0; i < N; i++) {
        COp op = static_cast<COp>(i & 3);
        switch (op) {
            case CAdd: acc += i; break;
            case CSub: acc -= i; break;
            case CMul: acc ^= i; break;
            case CDiv: acc += (i >> 1); break;
        }
    }
    return acc;
}

// Raw int
[[gnu::noinline]] int bench_raw_int(int N) {
    int acc = 0;
    for (int i = 0; i < N; i++) {
        int op = i & 3;
        switch (op) {
            case 0: acc += i; break;
            case 1: acc -= i; break;
            case 2: acc ^= i; break;
            case 3: acc += (i >> 1); break;
        }
    }
    return acc;
}

// Function pointer table (alternative dispatch)
using FnPtr = int(*)(int);
[[gnu::noinline]] int fn_add(int x) { return x; }
[[gnu::noinline]] int fn_sub(int x) { return -x; }
[[gnu::noinline]] int fn_mul(int x) { return x ^ 1; }
[[gnu::noinline]] int fn_div(int x) { return x >> 1; }

[[gnu::noinline]] int bench_fntable(int N) {
    static FnPtr table[] = {fn_add, fn_sub, fn_mul, fn_div};
    int acc = 0;
    for (int i = 0; i < N; i++) {
        acc += table[i & 3](i);
    }
    return acc;
}

int main() {
    const int N = 50000000;

    volatile int w = bench_raw_int(1000);

    struct { const char* name; int (*fn)(int); double median; } tests[] = {
        {"enum class",              bench_enum_class, 0},
        {"C-style enum",            bench_c_enum,      0},
        {"raw int switch",          bench_raw_int,     0},
        {"fn pointer table",        bench_fntable,     0},
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

    printf("=== ch24 enum D5 benchmark (N=%d, 5-trial median) ===\n", N);
    for (auto& t : tests)
        printf("  %-25s  %8.2f ms\n", t.name, t.median);

    g_sink = tests[3].median > 0 ? 1 : 0;
    return 0;
}
