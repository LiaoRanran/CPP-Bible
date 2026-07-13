// ch45_oop_object_model — 虚函数/直接调用/函数指针 开销实测
// 编译: g++ -O2 -std=c++23 -m64 _ch45_oop_perf.cpp -o _ch45_oop_perf.exe
// 运行: _ch45_oop_perf.exe  (输出见 .out)
//
// 方法: RDTSC 计时。三类调用各跑 N 次，减去等结构空循环开销得到单次调用延迟。
// probe_virtual 用 [[gnu::noipa]] 阻止跨过程去虚拟化 (devirtualization)，确保保留 vtable 查找。

#include <cstdint>
#include <cstdio>
#include <utility>
#include <windows.h>

static inline uint64_t rdtsc() {
    uint64_t t;
    __asm__ __volatile__("rdtsc" : "=A"(t));
    return t;
}
static double tsc_ghz() {
    LARGE_INTEGER freq; QueryPerformanceFrequency(&freq);
    LARGE_INTEGER a; QueryPerformanceCounter(&a);
    uint64_t r0 = rdtsc();
    Sleep(100);
    LARGE_INTEGER b; QueryPerformanceCounter(&b);
    uint64_t r1 = rdtsc();
    double secs = (double)(b.QuadPart - a.QuadPart) / (double)freq.QuadPart;
    return (double)(r1 - r0) / secs / 1e9;
}

struct Base {
    virtual ~Base() = default;
    virtual int virt(int x) { return x + 1; }
    [[gnu::noinline]] int concrete(int x) { return x * 2; }   // 非虚，编译期直接绑定；noinline 强制真实 call 指令
};
struct Derived : Base {
    int virt(int x) override { return x - 1; }
};
struct D2 : Base {
    int virt(int x) override { return x + 7; }
};
using FnPtr = int(*)(int);
int free_fn(int x) { return x + 3; }

Base* g_obj = new Derived();
Base* g_arr[2] = { new Derived(), new D2() };   // 异构对象数组，强制每次迭代重取 vtable
FnPtr g_fn = free_fn;
void* volatile g_sink = nullptr;

[[gnu::noinline, gnu::noipa]]
static uint64_t probe_nop(int n) {
    int s = 0;
    for (int i = 0; i < n; ++i) s += i;
    return s;
}
[[gnu::noinline, gnu::noipa]]
static uint64_t probe_direct(int n) {
    int s = 0;
    Derived d;
    for (int i = 0; i < n; ++i) s += d.concrete(i);   // 非虚，直接调用
    return s;
}
[[gnu::noinline, gnu::noipa]]
static uint64_t probe_virtual(int n) {
    int s = 0;
    Base* o = g_obj;                                   // 动态类型对编译器不可见 (noipa)
    for (int i = 0; i < n; ++i) s += o->virt(i);       // 虚调用，走 vtable
    return s;
}
[[gnu::noinline, gnu::noipa]]
static uint64_t probe_fnptr(int n) {
    int s = 0;
    FnPtr fn = g_fn;
    for (int i = 0; i < n; ++i) s += fn(i);            // 函数指针间接调用
    return s;
}
[[gnu::noinline, gnu::noipa]]
static uint64_t probe_virtual_reload(int n) {
    int s = 0;
    for (int i = 0; i < n; ++i) {
        Base* o = g_arr[i & 1];                        // 每次迭代对象类型不同 → vtable 无法提升出循环
        s += o->virt(i);
    }
    return s;
}

static double bench(uint64_t (*fn)(int), int n, int reps) {
    uint64_t best = ~0ULL;
    for (int r = 0; r < reps; ++r) {
        uint64_t t0 = rdtsc();
        g_sink = (void*)fn(n);
        uint64_t t1 = rdtsc();
        uint64_t dt = t1 - t0;
        if (dt < best) best = dt;
    }
    return (double)best / (double)n;
}

int main() {
    double ghz = tsc_ghz();
    printf("TSC = %.3f GHz   (MinGW GCC 13.1.0 -O2, x86_64)\n", ghz);
    const int N = 10'000'000;
    double nop     = bench(probe_nop,          N, 20);
    double direct  = bench(probe_direct,       N, 20);
    double virt    = bench(probe_virtual,      N, 20);
    double fnptr   = bench(probe_fnptr,        N, 20);
    double virtrl  = bench(probe_virtual_reload, N, 20);
    auto per = [&](double raw){ double cyc = raw - nop; return std::make_pair(cyc, cyc / ghz); };
    auto [dc, dns] = per(direct);
    auto [vc, vns] = per(virt);
    auto [fc, fns] = per(fnptr);
    auto [rc, rns] = per(virtrl);
    printf("%-18s %10s %10s %12s\n", "call", "cyc/call", "ns/call", "raw(cyc)");
    printf("%-18s %10.2f %10.3f %12.2f\n", "direct",   dc, dns, direct);
    printf("%-18s %10.2f %10.3f %12.2f\n", "virtual(hot)", vc, vns, virt);
    printf("%-18s %10.2f %10.3f %12.2f\n", "fnptr",    fc, fns, fnptr);
    printf("%-18s %10.2f %10.3f %12.2f\n", "virtual(reload)", rc, rns, virtrl);
    printf("virtual(hot)-direct extra = %.2f ns (%.1f cyc)\n", vns - dns, vc - dc);
    printf("virtual(reload)-direct extra = %.2f ns (%.1f cyc)\n", rns - dns, rc - dc);
    return 0;
}
