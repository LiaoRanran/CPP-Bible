// _bench_d5_52_ebo.cpp — ch52 EBO：空成员压缩如何减半缓存足迹
// g++ -O2 -std=c++23
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <vector>
#include <algorithm>
#include <random>
#include <memory>

static double now_ms() {
    using namespace std::chrono;
    return duration<double, std::milli>(steady_clock::now().time_since_epoch()).count();
}
template <class F>
static double bench(const char* name, F&& f) {
    std::vector<double> t;
    for (int r = 0; r < 5; ++r) { double t0 = now_ms(); f(); t.push_back(now_ms() - t0); }
    std::sort(t.begin(), t.end());
    std::printf("%-40s %10.3f ms\n", name, t[2]);
    return t[2];
}
volatile std::uint64_t g_sink;

struct Empty { void operator()(int*) const noexcept {} };

// 普通空成员：占 1 字节 + 7 字节填充 → 16B
struct Plain    { std::uint64_t v; Empty e; };
// [[no_unique_address]] 压缩 → 8B
struct Squeezed { std::uint64_t v; [[no_unique_address]] Empty e; };
// EBO 继承压缩 → 8B（libstdc++ compressed_pair 的手法）
struct Inherit : Empty { std::uint64_t v; };

constexpr std::size_t N = 16'000'000;
constexpr int REPS = 10;

template <class T>
static void run(const char* name, std::mt19937_64& rng) {
    std::vector<T> a(N);
    std::uniform_int_distribution<std::uint64_t> d(0, 1000);
    for (auto& e : a) e.v = d(rng);
    bench(name, [&] {
        std::uint64_t s = 0;
        for (int r = 0; r < REPS; ++r)
            for (std::size_t i = 0; i < N; ++i) s += a[i].v;
        g_sink = s;
    });
}

int main() {
    std::printf("sizeof: Plain=%zu Squeezed=%zu Inherit=%zu\n",
                sizeof(Plain), sizeof(Squeezed), sizeof(Inherit));
    std::printf("sizeof: unique_ptr<int>=%zu  unique_ptr<int,void(*)(int*)>=%zu\n",
                sizeof(std::unique_ptr<int>),
                sizeof(std::unique_ptr<int, void (*)(int*)>));
    std::mt19937_64 rng(42);
    run<Squeezed>("traverse Squeezed (8B, NUA)", rng);
    run<Inherit> ("traverse Inherit  (8B, EBO)", rng);
    run<Plain>   ("traverse Plain    (16B)", rng);
    std::printf("sink=%llu\n", (unsigned long long)g_sink);
    return 0;
}
