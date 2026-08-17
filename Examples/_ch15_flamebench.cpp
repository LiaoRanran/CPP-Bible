// _ch15_flamebench.cpp — 火焰图取证：真实调用树 + 本机实测自时间
// 编译：g++ -std=c++23 -O2 -g _ch15_flamebench.cpp -o _ch15_flamebench
// 说明：用 [[gnu::noinline]] 冻结调用栈，使 perf/火焰图能看到真实栈帧；
//       自时间用 steady_clock 确定性计时（非采样），再按包含时间归一为宽度。
#include <chrono>
#include <cmath>
#include <cstdio>

[[gnu::noinline]] double kernel_a1(double x) {
    double s = 0;
    for (int i = 0; i < 1000; ++i) s += std::sin(x + i) * std::cos(x - i);
    return s;
}
[[gnu::noinline]] double kernel_b1(double x) {
    double s = 0;
    for (int i = 0; i < 300; ++i) s += std::sin(x + i) * std::cos(x - i);
    return s;
}
[[gnu::noinline]] double helper_b2(double x) {
    double s = 0;
    for (int i = 0; i < 20; ++i) s += x + i;
    return s;
}
[[gnu::noinline]] double kernel_c1(double x) {
    double s = 0;
    for (int i = 0; i < 200; ++i) s += std::sin(x + i) * 0.5;
    return s;
}
[[gnu::noinline]] double phase_a(double x) {
    double a = 0;
    for (int k = 0; k < 200; ++k) a += kernel_a1(x + k);
    return a;
}
[[gnu::noinline]] double phase_b(double x) {
    double b = 0;
    for (int k = 0; k < 500; ++k) b += kernel_b1(x + k);
    for (int k = 0; k < 5; ++k)   b += helper_b2(x + k);
    return b;
}
[[gnu::noinline]] double phase_c(double x) {
    double c = 0;
    for (int k = 0; k < 200; ++k) c += kernel_c1(x + k);
    return c;
}
[[gnu::noinline]] double workload(double x) {
    return phase_a(x) + phase_b(x) + phase_c(x);
}

template <class F>
double bench_ns(F f, long iters) {
    volatile double sink = 0;
    for (long w = 0; w < iters / 10; ++w) sink += f();      // 预热
    double acc = 0;
    auto t0 = std::chrono::steady_clock::now();
    for (long i = 0; i < iters; ++i) acc += f();
    auto t1 = std::chrono::steady_clock::now();
    sink += acc; (void)sink;
    return std::chrono::duration<double, std::nano>(t1 - t0).count() / iters;
}

int main() {
    const long K = 50000, M = 30, R = 30;
    double x = 0;
    double ta  = bench_ns([&] { x += 0.1; return kernel_a1(x); }, K);
    double tb  = bench_ns([&] { x += 0.1; return kernel_b1(x); }, K);
    double tb2 = bench_ns([&] { x += 0.1; return helper_b2(x); }, K);
    double tc  = bench_ns([&] { x += 0.1; return kernel_c1(x); }, K);
    double pa  = bench_ns([&] { x += 0.1; return phase_a(x); }, M);
    double pb  = bench_ns([&] { x += 0.1; return phase_b(x); }, M);
    double pc  = bench_ns([&] { x += 0.1; return phase_c(x); }, M);
    double wl  = bench_ns([&] { x += 0.1; return workload(x); }, R);

    // 单次调用的包含时间（inclusive）；自时间 = 包含 - Σ(子调用次数 × 子包含)
    double self_a  = pa - 200 * ta;
    double self_b  = pb - (500 * tb + 5 * tb2);
    double self_c  = pc - 200 * tc;
    double self_wl = wl - (pa + pb + pc);

    printf("SELF kernel_a1 %.3f\n", ta);
    printf("SELF kernel_b1 %.3f\n", tb);
    printf("SELF helper_b2 %.3f\n", tb2);
    printf("SELF kernel_c1 %.3f\n", tc);
    printf("INCL phase_a %.3f\n", pa);
    printf("INCL phase_b %.3f\n", pb);
    printf("INCL phase_c %.3f\n", pc);
    printf("INCL workload %.3f\n", wl);
    printf("SELF phase_a %.3f\n", self_a);
    printf("SELF phase_b %.3f\n", self_b);
    printf("SELF phase_c %.3f\n", self_c);
    printf("SELF workload %.3f\n", self_wl);
    return 0;
}
