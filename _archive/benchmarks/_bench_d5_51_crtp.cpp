// D5 Wave 3 benchmark: ch51 CRTP — 静态多态(编译期分发/可内联) vs 虚函数派发
// 编译: g++ -O2 -std=c++23 -o bench.exe _bench_d5_51_crtp.cpp
// 目的: 量化 vtable 间接调用的开销；CRTP 把调用在编译期解析并可内联，去除间接层.
#include <iostream>
#include <chrono>
#include <vector>
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

// 虚函数多态(混合动态类型，阻止去虚拟化)
struct VBase { virtual ~VBase() = default; virtual int compute(int x) const { return x; } };
struct VDerived : VBase { int compute(int x) const override { return x * 3 + 1; } };
struct VOther : VBase { int compute(int x) const override { return x * 2; } };

// CRTP 静态多态
template <typename D>
struct CRTPBase {
    int compute(int x) const { return static_cast<const D*>(this)->compute(x); }
};
struct CDerived : CRTPBase<CDerived> {
    int compute(int x) const { return x * 3 + 1; }
};

int main() {
    const int N = 10'000'000;
    std::vector<VBase*> objs;
    objs.reserve(N);
    for (int i = 0; i < N; ++i)
        objs.push_back((i % 2) ? static_cast<VBase*>(new VDerived) : static_cast<VBase*>(new VOther));
    CDerived cd;
    std::vector<int> data(N);
    for (int i = 0; i < N; ++i) data[i] = i;

    bench("virtual_dispatch", [&] {
        int64_t s = 0;
        for (int i = 0; i < N; ++i) s += objs[i]->compute(data[i]);
        return s;
    });
    bench("crtp_static", [&] {
        int64_t s = 0;
        for (int i = 0; i < N; ++i) s += cd.compute(data[i]);
        return s;
    });

    for (VBase* b : objs) delete b;
    std::cout << "esc=" << g_esc << "\n";
    return 0;
}
