// _bench_d5_ch29_friend.cpp
// D5 benchmark: friend access vs public method vs getter — with large data to prevent DCE
#include <cstdio>
#include <chrono>

volatile int g_sink = 0;

class Container {
    int data_[8192];  // 32KB — won't fit L1, forces real memory access
public:
    Container() { for (int i = 0; i < 8192; i++) data_[i] = i * 3 + 1; }

    int sum_public() const {
        int s = 0;
        for (int i = 0; i < 8192; i++) s += data_[i];
        return s;
    }

    const int* get_data() const { return data_; }

    friend int sum_friend(const Container& c);
};

[[gnu::noinline]] int sum_friend(const Container& c) {
    int s = 0;
    for (int i = 0; i < 8192; i++) s += c.data_[i];
    return s;
}

[[gnu::noinline]] int sum_getter(const Container& c) {
    int s = 0;
    const int* d = c.get_data();
    for (int i = 0; i < 8192; i++) s += d[i];
    return s;
}

[[gnu::noinline]] int sum_public_call(const Container& c) {
    return c.sum_public();
}

int main() {
    const int N = 10000;
    Container c;

    volatile int w = sum_public_call(c);

    struct { const char* name; int (*fn)(const Container&); double median; } tests[] = {
        {"friend (direct priv)",   sum_friend,       0},
        {"public member fn",       sum_public_call,  0},
        {"getter + external",      sum_getter,       0},
    };

    for (auto& t : tests) {
        double times[5];
        for (int trial = 0; trial < 5; trial++) {
            auto s = std::chrono::high_resolution_clock::now();
            volatile int r = t.fn(c);
            (void)r;
            auto e = std::chrono::high_resolution_clock::now();
            times[trial] = std::chrono::duration<double, std::milli>(e - s).count();
        }
        for (int i = 0; i < 5; i++)
            for (int j = i+1; j < 5; j++)
                if (times[j] < times[i]) { double tmp = times[i]; times[i] = times[j]; times[j] = tmp; }
        t.median = times[2];
    }

    printf("=== ch29 friend D5 benchmark (N=%d, 5-trial median) ===\n", N);
    for (auto& t : tests)
        printf("  %-25s  %8.2f ms\n", t.name, t.median);

    g_sink = tests[2].median > 0 ? 1 : 0;
    return 0;
}
