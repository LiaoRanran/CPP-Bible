// D5 Wave 3 benchmark: ch48 RTTI — dynamic_cast / typeid 相比虚函数派发的真实代价
// 编译: g++ -O2 -std=c++23 -o bench.exe _bench_d5_48_rtti.cpp
// 目的: 量化 虚函数派发(零 RTTI) vs dynamic_cast(运行时类型遍历) vs typeid 比较.
#include <iostream>
#include <chrono>
#include <vector>
#include <typeinfo>
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

struct Base { virtual ~Base() = default; virtual int op(int x) const { return x; } };
struct Derived : Base { int op(int x) const override { return x + 1; } };
struct Other : Base { int op(int x) const override { return x * 2; } };

int main() {
    const int N = 5'000'000;
    std::vector<Base*> objs;
    objs.reserve(N);
    for (int i = 0; i < N; ++i)
        objs.push_back((i % 2) ? static_cast<Base*>(new Derived) : static_cast<Base*>(new Other));

    bench("virtual_dispatch", [&] {
        int64_t s = 0;
        for (int i = 0; i < N; ++i) s += objs[i]->op(i);
        return s;
    });
    bench("dynamic_cast", [&] {
        int64_t s = 0;
        for (int i = 0; i < N; ++i) {
            Derived* d = dynamic_cast<Derived*>(objs[i]);
            if (d) s += d->op(i);
            else s += objs[i]->op(i);
        }
        return s;
    });
    bench("typeid_compare", [&] {
        int64_t s = 0;
        const std::type_info& td = typeid(Derived);
        for (int i = 0; i < N; ++i) {
            if (typeid(*objs[i]) == td) s += 1;
            else s += 2;
        }
        return s;
    });

    for (Base* b : objs) delete b;
    std::cout << "esc=" << g_esc << "\n";
    return 0;
}
