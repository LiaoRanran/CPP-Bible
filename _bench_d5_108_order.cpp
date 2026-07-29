// _bench_d5_108_order.cpp — ch108 D5: x86-64 上各 memory_order 的真实成本
// g++ -O2 -std=c++17 -pthread
#include <algorithm>
#include <atomic>
#include <chrono>
#include <cstdio>
#include <thread>
#include <vector>

using Clock = std::chrono::steady_clock;
static double ms(Clock::time_point a, Clock::time_point b) {
    return std::chrono::duration<double, std::milli>(b - a).count();
}
template <class F> static double median5(F f) {
    std::vector<double> t;
    for (int i = 0; i < 5; ++i) t.push_back(f());
    std::sort(t.begin(), t.end());
    return t[2];
}
volatile long long g_sink = 0;

int main() {
    const long long R = 200'000'000;

    // ---- 1) 单线程 store：relaxed/release = mov，seq_cst = xchg（关键差异）----
    std::atomic<long long> x{0};
    double t_rlx = median5([&] {
        auto a = Clock::now();
        for (long long i = 0; i < R; ++i) x.store(i, std::memory_order_relaxed);
        g_sink = x.load(std::memory_order_relaxed);
        return ms(a, Clock::now());
    });
    double t_rel = median5([&] {
        auto a = Clock::now();
        for (long long i = 0; i < R; ++i) x.store(i, std::memory_order_release);
        g_sink = x.load(std::memory_order_relaxed);
        return ms(a, Clock::now());
    });
    double t_sc = median5([&] {
        auto a = Clock::now();
        for (long long i = 0; i < R; ++i) x.store(i, std::memory_order_seq_cst);
        g_sink = x.load(std::memory_order_relaxed);
        return ms(a, Clock::now());
    });
    std::printf("store_200M,relaxed,%.3f\n", t_rlx);
    std::printf("store_200M,release,%.3f,ratio_vs_rlx=%.2f\n", t_rel, t_rel / t_rlx);
    std::printf("store_200M,seq_cst,%.3f,ratio_vs_rlx=%.2f\n", t_sc, t_sc / t_rlx);

    // ---- 2) 单线程 load：x86 上三种序均为 mov（应≈1×）----
    double l_rlx = median5([&] {
        auto a = Clock::now();
        long long s = 0;
        for (long long i = 0; i < R; ++i) s += x.load(std::memory_order_relaxed);
        g_sink = s;
        return ms(a, Clock::now());
    });
    double l_sc = median5([&] {
        auto a = Clock::now();
        long long s = 0;
        for (long long i = 0; i < R; ++i) s += x.load(std::memory_order_seq_cst);
        g_sink = s;
        return ms(a, Clock::now());
    });
    std::printf("load_200M,relaxed,%.3f\n", l_rlx);
    std::printf("load_200M,seq_cst,%.3f,ratio=%.2f\n", l_sc, l_sc / l_rlx);

    // ---- 3) 单线程 fetch_add：x86 RMW 全为 lock xadd（应≈1×，非显然）----
    const long long F = 100'000'000;
    double f_rlx = median5([&] {
        x.store(0);
        auto a = Clock::now();
        for (long long i = 0; i < F; ++i) x.fetch_add(1, std::memory_order_relaxed);
        g_sink = x.load(std::memory_order_relaxed);
        return ms(a, Clock::now());
    });
    double f_sc = median5([&] {
        x.store(0);
        auto a = Clock::now();
        for (long long i = 0; i < F; ++i) x.fetch_add(1, std::memory_order_seq_cst);
        g_sink = x.load(std::memory_order_relaxed);
        return ms(a, Clock::now());
    });
    std::printf("fetch_add_100M,relaxed,%.3f\n", f_rlx);
    std::printf("fetch_add_100M,seq_cst,%.3f,ratio=%.2f\n", f_sc, f_sc / f_rlx);

    // ---- 4) 普通非原子内存累加对照（经逃逸指针强制每轮 load+add+store，
    //          与 lock xadd 同为"内存 RMW"，差异只在 lock 前缀）----
    long long plain_c = 0;
    long long* volatile pc = &plain_c;  // 逃逸，阻止寄存器化/闭式求值
    double n_plain = median5([&] {
        *pc = 0;
        auto a = Clock::now();
        for (long long i = 0; i < F; ++i) ++*pc;
        g_sink = *pc;
        return ms(a, Clock::now());
    });
    std::printf("plain_add_100M,nonatomic_mem,%.3f,atomic_penalty=%.1fx\n", n_plain, f_rlx / n_plain);

    // ---- 5) 双线程真争用 fetch_add（MESI 弹动叠加）----
    auto contend = [&](std::memory_order mo) {
        std::atomic<long long> c{0};
        auto a = Clock::now();
        std::thread t1([&] { for (long long i = 0; i < F / 2; ++i) c.fetch_add(1, mo); });
        std::thread t2([&] { for (long long i = 0; i < F / 2; ++i) c.fetch_add(1, mo); });
        t1.join();
        t2.join();
        g_sink = c.load();
        return ms(a, Clock::now());
    };
    double c_rlx = median5([&] { return contend(std::memory_order_relaxed); });
    double c_sc = median5([&] { return contend(std::memory_order_seq_cst); });
    std::printf("contend2_100M,relaxed,%.3f,vs_single=%.2fx\n", c_rlx, c_rlx / f_rlx);
    std::printf("contend2_100M,seq_cst,%.3f,ratio_vs_rlx=%.2f\n", c_sc, c_sc / c_rlx);
    return 0;
}
