// _bench_d5_42_aliasing.cpp — ch42 严格别名：别名假设如何阻碍优化
// g++ -O2 -std=c++23
#include <chrono>
#include <cstdint>
#include <cstdio>
#include <cstring>
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
    std::printf("%-40s %10.3f ms\n", name, t[2]);
    return t[2];
}
volatile std::uint64_t g_sink;

// 1) char* 可别名一切：计数器经指针写回，编译器每轮必须 load/store *counter
__attribute__((noinline))
void count_via_ptr(const char* buf, std::size_t n, std::uint64_t* counter) {
    for (std::size_t i = 0; i < n; ++i)
        if (buf[i]) ++*counter;      // *counter 可能与 buf 别名 → 无法寄存器化
}
// 2) 局部累加，一次写回（等价语义，别名歧义消除）
__attribute__((noinline))
void count_via_local(const char* buf, std::size_t n, std::uint64_t* counter) {
    std::uint64_t c = 0;
    for (std::size_t i = 0; i < n; ++i)
        if (buf[i]) ++c;
    *counter += c;
}
// 3) __restrict 显式承诺不别名
__attribute__((noinline))
void count_via_restrict(const char* __restrict buf, std::size_t n,
                        std::uint64_t* __restrict counter) {
    for (std::size_t i = 0; i < n; ++i)
        if (buf[i]) ++*counter;
}

// 4) 三数组加法：无 restrict（GCC 生成运行时重叠检查+双版本） vs restrict
__attribute__((noinline))
void add3(float* a, const float* b, const float* c, std::size_t n) {
    for (std::size_t i = 0; i < n; ++i) a[i] = b[i] + c[i];
}
__attribute__((noinline))
void add3_restrict(float* __restrict a, const float* __restrict b,
                   const float* __restrict c, std::size_t n) {
    for (std::size_t i = 0; i < n; ++i) a[i] = b[i] + c[i];
}

int main() {
    constexpr std::size_t N = 16'000'000;
    constexpr int REPS = 10;
    std::vector<char> buf(N);
    std::mt19937_64 rng(42);
    for (auto& c : buf) c = static_cast<char>(rng() & 1);

    std::uint64_t counter = 0;
    bench("count: ++*counter (aliasable)", [&] {
        counter = 0;
        for (int r = 0; r < REPS; ++r) count_via_ptr(buf.data(), N, &counter);
        g_sink = counter;
    });
    std::uint64_t c1 = counter;
    bench("count: local then store", [&] {
        counter = 0;
        for (int r = 0; r < REPS; ++r) count_via_local(buf.data(), N, &counter);
        g_sink = counter;
    });
    std::uint64_t c2 = counter;
    bench("count: __restrict counter", [&] {
        counter = 0;
        for (int r = 0; r < REPS; ++r) count_via_restrict(buf.data(), N, &counter);
        g_sink = counter;
    });
    std::uint64_t c3 = counter;
    std::printf("checksums: %llu %llu %llu (must equal)\n",
                (unsigned long long)c1, (unsigned long long)c2, (unsigned long long)c3);

    constexpr std::size_t M = 8'000'000;
    std::vector<float> fa(M), fb(M), fc(M);
    for (std::size_t i = 0; i < M; ++i) { fb[i] = float(i & 255); fc[i] = float((i >> 3) & 255); }
    bench("add3: no restrict", [&] {
        for (int r = 0; r < REPS; ++r) add3(fa.data(), fb.data(), fc.data(), M);
        g_sink = static_cast<std::uint64_t>(fa[M / 2]);
    });
    bench("add3: __restrict", [&] {
        for (int r = 0; r < REPS; ++r) add3_restrict(fa.data(), fb.data(), fc.data(), M);
        g_sink = static_cast<std::uint64_t>(fa[M / 2]);
    });
    return 0;
}
