// D5 Wave 4 benchmark: ch30 volatile — plain / volatile / atomic 计数的真实差价
// 编译: g++ -O2 -std=c++23 -o bench.exe _bench_d5_30_volatile.cpp
// 设计要点: plain 局部计数会被 -O2 闭式折叠(整段循环消失), 这本身就是测量结论之一;
//   volatile 强制每轮 load+add+store; atomic fetch_add 是 lock xadd(x86 上 relaxed 与 seq_cst 同指令)。
#include <iostream>
#include <chrono>
#include <atomic>
#include <cstdint>

static volatile long long g_esc = 0;

int main() {
    const long long N = 100'000'000;
    auto ms = [](auto a, auto b) { return std::chrono::duration<double, std::milli>(b - a).count(); };

    // 1) plain: 优化器可将整个循环折叠为 c = N
    auto t0 = std::chrono::steady_clock::now();
    long long c1 = 0;
    for (long long i = 0; i < N; ++i) c1++;
    auto t1 = std::chrono::steady_clock::now();

    // 2) volatile: 每轮强制内存 load + add + store
    volatile long long c2 = 0;
    for (long long i = 0; i < N; ++i) c2 = c2 + 1;
    auto t2 = std::chrono::steady_clock::now();

    // 3) atomic relaxed
    std::atomic<long long> c3{0};
    for (long long i = 0; i < N; ++i) c3.fetch_add(1, std::memory_order_relaxed);
    auto t3 = std::chrono::steady_clock::now();

    // 4) atomic seq_cst
    std::atomic<long long> c4{0};
    for (long long i = 0; i < N; ++i) c4.fetch_add(1, std::memory_order_seq_cst);
    auto t4 = std::chrono::steady_clock::now();

    g_esc = c1 + c2 + c3.load() + c4.load();
    std::cout << "plain_counter    " << ms(t0, t1) << " ms\n";
    std::cout << "volatile_counter " << ms(t1, t2) << " ms\n";
    std::cout << "atomic_relaxed   " << ms(t2, t3) << " ms\n";
    std::cout << "atomic_seq_cst   " << ms(t3, t4) << " ms\n";
    std::cout << "esc=" << g_esc << "\n";
    return 0;
}
