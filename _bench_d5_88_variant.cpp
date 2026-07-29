// D5 Wave 3 benchmark: ch88 optional/expected/variant — 可辨别联合 vs 虚多态；optional vs 裸指针
// 编译: g++ -O2 -std=c++23 -o bench.exe _bench_d5_88_variant.cpp
// 目的: 量化 std::variant 访问器 vs 虚函数派发；std::optional 访问 vs 裸指针空检查.
#include <iostream>
#include <chrono>
#include <vector>
#include <variant>
#include <optional>
#include <random>
#include <cstdint>

static volatile long long g_esc = 0;

template <class F>
double bench(const char* name, F f, int rounds = 5) {
    double best = 1e18;
    for (int r = 0; r < rounds; ++r) {
        auto t0 = std::chrono::steady_clock::now();
        long long res = f();
        auto t1 = std::chrono::steady_clock::now();
        g_esc += res;
        double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
        if (ms < best) best = ms;
    }
    std::cout << name << ": " << best << " ms\n";
    return best;
}

struct VBase { virtual ~VBase() = default; virtual int op(int x) const { return x; } };
struct VA : VBase { int op(int x) const override { return x + 1; } };
struct VB : VBase { int op(int x) const override { return x * 2; } };

using Var = std::variant<VA, VB>;

int main() {
    const int N = 5'000'000;
    std::mt19937 rng(11);
    std::uniform_int_distribution<int> dist(0, 1);
    std::vector<VBase*> objs; objs.reserve(N);
    std::vector<Var> vars; vars.reserve(N);
    for (int i = 0; i < N; ++i) {
        bool pick = dist(rng);
        objs.push_back(pick ? static_cast<VBase*>(new VA) : static_cast<VBase*>(new VB));
        vars.push_back(pick ? Var(VA{}) : Var(VB{}));
    }
    std::vector<int> args(N);
    for (int i = 0; i < N; ++i) args[i] = i;

    bench("virtual_call", [&] {
        int64_t s = 0;
        for (int i = 0; i < N; ++i) s += objs[i]->op(args[i]);
        return s;
    });
    bench("variant_visit", [&] {
        int64_t s = 0;
        for (int i = 0; i < N; ++i) s += std::visit([](const auto& v) { return v.op(0); }, vars[i]);
        return s;
    });

    std::vector<std::optional<int>> opts; opts.reserve(N);
    std::vector<int*> ptrs; ptrs.reserve(N);
    for (int i = 0; i < N; ++i) {
        bool has = dist(rng);
        opts.push_back(has ? std::optional<int>(args[i]) : std::nullopt);
        ptrs.push_back(has ? &args[i] : nullptr);
    }
    bench("optional_access", [&] {
        int64_t s = 0;
        for (int i = 0; i < N; ++i) if (opts[i]) s += *opts[i];
        return s;
    });
    bench("pointer_access", [&] {
        int64_t s = 0;
        for (int i = 0; i < N; ++i) if (ptrs[i]) s += *ptrs[i];
        return s;
    });

    for (auto p : objs) delete p;
    std::cout << "esc=" << g_esc << "\n";
    return 0;
}
