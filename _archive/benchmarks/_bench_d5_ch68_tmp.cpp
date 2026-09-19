// _bench_d5_ch68_tmp.cpp — ch68 模板元编程(TMP) / constexpr / 运行时 计算同一值的开销对比
// GCC 15.3.0 (MinGW-W64 x86_64), g++ -O2 -std=c++23
// 结论预期：TMP 与 constexpr 在编译期把 Fib<30> 折成常量 832040，运行时只是"加一个常量"（几乎免费）；
// 运行时版本每轮都要重算，开销显著。TMP 与 constexpr 的运行时代码完全相同，差异只在编译期（实例化膨胀 vs 无）。
#include <iostream>
#include <chrono>
#include <algorithm>

static volatile long long g_sink = 0;

// (A) TMP：编译期递归计算 Fib<30>
template <int N> struct Fib { static const long long value = Fib<N-1>::value + Fib<N-2>::value; };
template <> struct Fib<0> { static const long long value = 0; };
template <> struct Fib<1> { static const long long value = 1; };

// (B) constexpr：编译期 arg 同样折成常量
constexpr long long fib_ce(int n) { return n < 2 ? n : fib_ce(n-1) + fib_ce(n-2); }

// (C) 运行时：迭代版，arg 运行时变化，每轮重算
long long fib_rt_iter(int n) { long long a = 0, b = 1; for (int k = 0; k < n; ++k) { long long t = a + b; a = b; b = t; } return a; }

int main() {
    const long long ITERS = 50'000'000LL;
    const int RUNS = 5;

    double r_tmp[RUNS], r_ce[RUNS], r_rt[RUNS];

    for (int r = 0; r < RUNS; ++r) {
        // (A) TMP：Fib<30>::value 是编译期常量，循环只是在运行时"加一个常量"
        { auto t0=std::chrono::steady_clock::now(); long long s=0;
          for (long long i=0;i<ITERS;++i){ s += Fib<30>::value; s += (i & 1); }
          auto t1=std::chrono::steady_clock::now(); g_sink+=s; r_tmp[r]=std::chrono::duration<double,std::milli>(t1-t0).count(); }
        // (B) constexpr：值同样在编译期折成常量
        { constexpr long long V = fib_ce(30);
          auto t0=std::chrono::steady_clock::now(); long long s=0;
          for (long long i=0;i<ITERS;++i){ s += V; s += (i & 1); }
          auto t1=std::chrono::steady_clock::now(); g_sink+=s; r_ce[r]=std::chrono::duration<double,std::milli>(t1-t0).count(); }
        // (C) 运行时：每轮用运行时 arg 重算 fib
        { auto t0=std::chrono::steady_clock::now(); long long s=0;
          for (long long i=0;i<ITERS;++i){ s += fib_rt_iter((int)(i % 30)); s += (i & 1); }
          auto t1=std::chrono::steady_clock::now(); g_sink+=s; r_rt[r]=std::chrono::duration<double,std::milli>(t1-t0).count(); }
    }

    std::sort(r_tmp,r_tmp+RUNS); std::sort(r_ce,r_ce+RUNS); std::sort(r_rt,r_rt+RUNS);
    double m_tmp=r_tmp[2], m_ce=r_ce[2], m_rt=r_rt[2];

    std::cout << "ch68 TMP vs constexpr vs runtime (ITERS=" << ITERS << ")\n";
    std::cout << "TMP   (compile-time) median = " << m_tmp << " ms\n";
    std::cout << "constexpr(compiled-time) median = " << m_ce  << " ms\n";
    std::cout << "runtime             median = " << m_rt  << " ms\n";
    std::cout << "ce/tmp = " << (m_ce/m_tmp) << "x\n";
    std::cout << "rt/tmp = " << (m_rt/m_tmp) << "x\n";
    std::cout << "sink=" << g_sink << std::endl;
    return 0;
}
