// Wave8 D5 bench: std::variant 访问分发 vs 手写 tagged union + switch
// 编译: g++ -O2 -std=c++23 _bench_d5_ch25_union_variant.cpp -o _bench_d5_ch25_union_variant.exe
// 运行: ./_bench_d5_ch25_union_variant.exe  (输出毫秒, 不断言时间/倍数)
#include <cstdio>
#include <cstdint>
#include <chrono>
#include <variant>

static volatile std::uint64_t g_sink = 0;

using Var = std::variant<int, double, long long>;

std::uint64_t visit_var(const Var& v) {
    return std::visit([](auto&& x) -> std::uint64_t {
        auto y = static_cast<long long>(x);
        return static_cast<std::uint64_t>(y > 0 ? y : -y) + 1u;
    }, v);
}

struct Tagged {
    enum Kind { I, D, L } kind;
    union { int i; double d; long long l; };
};

std::uint64_t visit_tagged(const Tagged& t) {
    switch (t.kind) {
        case Tagged::I: { auto y = static_cast<long long>(t.i); return static_cast<std::uint64_t>(y > 0 ? y : -y) + 1u; }
        case Tagged::D: { auto y = static_cast<long long>(t.d); return static_cast<std::uint64_t>(y > 0 ? y : -y) + 1u; }
        case Tagged::L: { auto y = t.l;                       return static_cast<std::uint64_t>(y > 0 ? y : -y) + 1u; }
    }
    return 0u;
}

int main() {
    constexpr int N = 5'000'000;
    std::uint32_t s = 123456789u;

    auto t0 = std::chrono::steady_clock::now();
    for (int i = 0; i < N; ++i) {
        s = s * 1103515245u + 12345u;
        int k = static_cast<int>(s % 3);
        Var v = (k == 1) ? Var(static_cast<double>(k)) : (k == 2 ? Var(static_cast<long long>(k)) : Var(k));
        g_sink += visit_var(v);
    }
    auto t1 = std::chrono::steady_clock::now();
    std::printf("variant %.3f ms\n", std::chrono::duration<double, std::milli>(t1 - t0).count());

    auto t2 = std::chrono::steady_clock::now();
    for (int i = 0; i < N; ++i) {
        s = s * 1103515245u + 12345u;
        int k = static_cast<int>(s % 3);
        Tagged t;
        if (k == 1) { t.kind = Tagged::D; t.d = static_cast<double>(k); }
        else if (k == 2) { t.kind = Tagged::L; t.l = k; }
        else { t.kind = Tagged::I; t.i = k; }
        g_sink += visit_tagged(t);
    }
    auto t3 = std::chrono::steady_clock::now();
    std::printf("tagged_union %.3f ms\n", std::chrono::duration<double, std::milli>(t3 - t2).count());

    std::printf("g_sink=%llu\n", static_cast<unsigned long long>(g_sink));
    return 0;
}
