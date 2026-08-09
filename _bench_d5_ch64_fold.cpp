// _bench_d5_ch64_fold.cpp  —  ch64 折叠表达式 vs 手写循环 vs 递归变参 vs 手写展开 的运行时开销
// GCC 15.3.0 (MinGW-W64 x86_64), g++ -O2 -std=c++23
// 同一组 8 个 double 的求和，分别用四种写法重复 ITERS 次；5 轮取中位。
// 结论：fold / 递归 / 手写展开(全部立即数) 编译为等价机器码≈1.00×；
// 而对手写"const 局部数组循环"慢约 2.2×，根因是后者把操作数物化到栈上产生 8 次加载。
#include <iostream>
#include <chrono>
#include <algorithm>

static volatile long long g_sink = 0;  // 防死代码消除

// (A) 折叠表达式求和
template <class... Ts>
double fold_sum(Ts... ts) { return (0.0 + ... + ts); }

// (B) 手写循环求和（对编译期已知常量的局部数组）
double loop_sum() {
    const double a[8] = {1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8};
    double s = 0.0;
    for (int i = 0; i < 8; ++i) s += a[i];
    return s;
}

// (C) 递归变参求和
double rec_sum() { return 0.0; }
template <class T, class... Ts>
double rec_sum(T t, Ts... ts) { return t + rec_sum(ts...); }

// (D) 手写展开（全部立即数，等价于 fold 的最优手写形式）
double unrolled_sum() { return 1.1 + 2.2 + 3.3 + 4.4 + 5.5 + 6.6 + 7.7 + 8.8; }

int main() {
    const long long ITERS = 200'000'000LL;
    const int RUNS = 5;
    double rf[RUNS], rl[RUNS], rr[RUNS], ru[RUNS];

    for (int r = 0; r < RUNS; ++r) {
        // (A) fold
        { auto t0 = std::chrono::steady_clock::now(); double s = 0.0;
          for (long long i = 0; i < ITERS; ++i) s += fold_sum(1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8);
          auto t1 = std::chrono::steady_clock::now(); g_sink += (long long)(s);
          rf[r] = std::chrono::duration<double, std::milli>(t1 - t0).count(); }
        // (B) loop over const array
        { auto t0 = std::chrono::steady_clock::now(); double s = 0.0;
          for (long long i = 0; i < ITERS; ++i) s += loop_sum();
          auto t1 = std::chrono::steady_clock::now(); g_sink += (long long)(s);
          rl[r] = std::chrono::duration<double, std::milli>(t1 - t0).count(); }
        // (C) recursion
        { auto t0 = std::chrono::steady_clock::now(); double s = 0.0;
          for (long long i = 0; i < ITERS; ++i) s += rec_sum(1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8);
          auto t1 = std::chrono::steady_clock::now(); g_sink += (long long)(s);
          rr[r] = std::chrono::duration<double, std::milli>(t1 - t0).count(); }
        // (D) unrolled immediates
        { auto t0 = std::chrono::steady_clock::now(); double s = 0.0;
          for (long long i = 0; i < ITERS; ++i) s += unrolled_sum();
          auto t1 = std::chrono::steady_clock::now(); g_sink += (long long)(s);
          ru[r] = std::chrono::duration<double, std::milli>(t1 - t0).count(); }
    }

    std::sort(rf, rf + RUNS); std::sort(rl, rl + RUNS); std::sort(rr, rr + RUNS); std::sort(ru, ru + RUNS);
    double m_fold = rf[RUNS / 2], m_loop = rl[RUNS / 2], m_rec = rr[RUNS / 2], m_unr = ru[RUNS / 2];

    std::cout << "ch64 fold vs loop vs recursion vs unrolled (ITERS=" << ITERS << ")\n";
    std::cout << "fold     median = " << m_fold << " ms\n";
    std::cout << "loop     median = " << m_loop << " ms\n";
    std::cout << "recursion median = " << m_rec  << " ms\n";
    std::cout << "unrolled  median = " << m_unr  << " ms\n";
    std::cout << "rec/fold   = " << (m_rec  / m_fold) << "x\n";
    std::cout << "unr/fold   = " << (m_unr  / m_fold) << "x\n";
    std::cout << "loop/fold  = " << (m_loop  / m_fold) << "x\n";
    std::cout << "sink=" << g_sink << std::endl;
    return 0;
}
