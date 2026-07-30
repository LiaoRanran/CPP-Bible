// _bench_d5_35_layout.cpp — ch35 内存布局：成员排序/填充对遍历性能的影响
// g++ -O2 -std=c++23
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <vector>
#include <algorithm>
#include <random>

static double now_ms() {
    using namespace std::chrono;
    return duration<double, std::milli>(steady_clock::now().time_since_epoch()).count();
}
template <class F>
static double bench(const char* name, F&& f) {
    std::vector<double> t;
    for (int r = 0; r < 5; ++r) { double t0 = now_ms(); f(); t.push_back(now_ms() - t0); }
    std::sort(t.begin(), t.end());
    std::printf("%-32s %10.3f ms\n", name, t[2]);
    return t[2];
}
volatile std::uint64_t g_sink;

struct Bad  { char c1; double d; char c2; int i; };                    // 期望 24B（对齐洞）
struct Good { double d; int i; char c1; char c2; };                    // 期望 16B
struct Fat  { double d; int i; char c1; char c2; char pad[48]; };      // 64B（整缓存行）

constexpr std::size_t N = 4'000'000;
constexpr int REPS = 10;

template <class T>
static void run(const char* name, std::mt19937_64& rng) {
    std::vector<T> v(N);
    std::uniform_int_distribution<int> di(0, 1000);
    for (auto& e : v) { e.d = di(rng) * 0.5; e.i = di(rng); }
    bench(name, [&] {
        std::uint64_t s = 0;
        for (int r = 0; r < REPS; ++r)
            for (std::size_t k = 0; k < N; ++k)
                s += static_cast<std::uint64_t>(v[k].d) + static_cast<std::uint64_t>(v[k].i);
        g_sink = s;
    });
}

int main() {
    std::printf("sizeof(Bad)=%zu sizeof(Good)=%zu sizeof(Fat)=%zu\n",
                sizeof(Bad), sizeof(Good), sizeof(Fat));
    std::mt19937_64 rng(42);
    run<Good>("traverse Good (16B)", rng);
    run<Bad> ("traverse Bad  (24B)", rng);
    run<Fat> ("traverse Fat  (64B)", rng);
    std::printf("sink=%llu\n", (unsigned long long)g_sink);
    return 0;
}
