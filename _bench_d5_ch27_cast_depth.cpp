// _bench_d5_ch27_cast_depth.cpp
// D5 角度: static_cast (零开销, 编译期指针偏移) vs dynamic_cast (RTTI 验证开销)
// 实测: AMD Ryzen 9 7940HX, g++ 15.3.0 -O2 -std=c++23
//
// 关键防优化:
//   1. [[gnu::noinline]] 不透明工厂隐藏对象动态类型 → 编译器无法去虚化 id()
//   2. 两个函数均执行相同虚调用(d->id()), 仅差 static_cast(指针偏移) vs
//      dynamic_cast(RTTI type_info 比对) → 隔离 RTTI 开销
//   3. volatile sink 防DCE
#include <chrono>
#include <cstdio>
#include <cstdint>

static volatile long long g_sink = 0;

// 单继承链: Base -> D1 -> D2 -> D3 -> D4 (继承深度 4)
struct Base {
    virtual ~Base() = default;
    virtual int id() const { return 0; }
};
struct D1 : Base { int id() const override { return 1; } };
struct D2 : D1  { int id() const override { return 2; } };
struct D3 : D2  { int id() const override { return 3; } };
struct D4 : D3  { int id() const override { return 4; } };

// 不透明工厂: 编译器无法确定返回的确切类型 → 无法去虚化后续调用
[[gnu::noinline]]
static Base* get_base() {
    static D4 obj;
    return &obj;
}

// ---- A. static_cast: 编译期偏移调整, 零运行期检查 ----
[[gnu::noinline]]
long long run_static(long long n) {
    Base* p = get_base();          // 隐藏动态类型
    long long acc = 0;
    for (long long i = 0; i < n; ++i) {
        D4* d = static_cast<D4*>(p);   // 仅指针偏移, 无 RTTI
        acc += d->id();                // 虚调用(不可去虚化)
    }
    return acc;
}

// ---- B. dynamic_cast: RTTI type_info 比对 + 继承链遍历 ----
[[gnu::noinline]]
long long run_dynamic(long long n) {
    Base* p = get_base();
    long long acc = 0;
    for (long long i = 0; i < n; ++i) {
        D4* d = dynamic_cast<D4*>(p);   // RTTI 验证
        if (d) acc += d->id();           // 虚调用(不可去虚化)
    }
    return acc;
}

int main() {
    const long long N = 20000000LL;       // 2e7

    for (int trial = 0; trial < 5; ++trial) {
        auto t0 = std::chrono::steady_clock::now();
        long long r1 = run_static(N);
        auto t1 = std::chrono::steady_clock::now();
        long long r2 = run_dynamic(N);
        auto t2 = std::chrono::steady_clock::now();
        g_sink = r1 + r2;
        double dt_s = std::chrono::duration<double, std::milli>(t1 - t0).count();
        double dt_d = std::chrono::duration<double, std::milli>(t2 - t1).count();
        std::printf("trial %d: static_cast=%.3f ms  dynamic_cast=%.3f ms  ratio=%.2fx\n",
                    trial, dt_s, dt_d, dt_d / dt_s);
    }
    std::printf("SUMMARY static_vs_dynamic\n");
    return 0;
}
