// _bench_d5_ch45_final_devirt.cpp
// D5 角度: 虚函数调用(vtable 间接) vs CRTP 静态分派(完全内联)
// 实测: AMD Ryzen 9 7940HX, g++ 15.3.0 -O2 -std=c++23
//
// 关键: 通过 [[gnu::noinline]] 不透明工厂隐藏对象动态类型, 防止编译器
// 去虚化(virtual)调用, 使其保留真正的 vtable 间接调用开销.
// CRTP 通过编译期多态消除间接调用, 允许完全内联.
#include <chrono>
#include <cstdio>
#include <cstdint>

static volatile long long g_sink = 0;

// ---- A. 虚函数派发: 编译器无法去虚化(类型来自不透明工厂) ----
struct Base {
    virtual ~Base() = default;
    virtual int work(int x) const { return x * 2 + 1; }
};
struct Derived : Base {
    int work(int x) const override { return x * 2 + 1; }
};

[[gnu::noinline]]
static Base* make_virtual() {
    static Derived obj;
    return &obj;     // 编译器在此函数外看不到返回的确切类型
}

long long run_virtual(Base* p, int const* data, long long n) {
    long long acc = 0;
    for (long long i = 0; i < n; ++i) acc += p->work(data[i]);
    return acc;
}

// ---- B. CRTP 静态分派: 模板单态化, 调用完全内联 ----
template <typename Derived>
struct CRTPBase {
    int work(int x) const {
        return static_cast<Derived const*>(this)->work_impl(x);
    }
};

struct CRTPDerived : CRTPBase<CRTPDerived> {
    int work_impl(int x) const { return x * 2 + 1; }
};

long long run_crtp(CRTPDerived const& obj, int const* data, long long n) {
    long long acc = 0;
    for (long long i = 0; i < n; ++i) acc += obj.work(data[i]);
    return acc;
}

int main() {
    const long long N = 20000000LL;

    // 数据缓冲区(复用于两次, 防DCE)
    static int data[20000000];
    for (long long i = 0; i < N; ++i) data[i] = static_cast<int>(i & 0xFF);

    Base* vb = make_virtual();    // 虚函数对象(不透明类型)
    CRTPDerived crtp_obj;         // CRTP 对象(静态已知)

    for (int trial = 0; trial < 5; ++trial) {
        auto t0 = std::chrono::steady_clock::now();
        long long r1 = run_virtual(vb, data, N);
        auto t1 = std::chrono::steady_clock::now();
        long long r2 = run_crtp(crtp_obj, data, N);
        auto t2 = std::chrono::steady_clock::now();
        g_sink = r1 + r2;
        double dt_v = std::chrono::duration<double, std::milli>(t1 - t0).count();
        double dt_c = std::chrono::duration<double, std::milli>(t2 - t1).count();
        std::printf("trial %d: virtual(vtable)=%.3f ms  crtp(static)=%.3f ms  ratio=%.2fx\n",
                    trial, dt_v, dt_c, dt_v / dt_c);
    }
    std::printf("SUMMARY virtual_vs_crtp\n");
    return 0;
}
