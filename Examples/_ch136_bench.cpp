// Examples/_ch136_bench.cpp
// 微基准：对比「每次 new+delete」与「对象池复用」的分配开销。
// 关键：用内联汇编屏障（compiler barrier）强制保留堆分配，
// 防止 -O2 把无副作用的 new/delete 整段消除（DCE）。
#include <chrono>
#include <cstdio>
#include <vector>

struct Node { int v; Node* next = nullptr; };

#define BARRIER() asm volatile("" : : "r"(p) : "memory");

static long long bench_raw(std::size_t n) {
    long long total = 0;
    auto t0 = std::chrono::steady_clock::now();
    for (std::size_t i = 0; i < n; ++i) {
        Node* p = new Node{static_cast<int>(i)};
        BARRIER();          // 强制编译器保留这次分配
        total += p->v;
        delete p;
        BARRIER();
    }
    auto t1 = std::chrono::steady_clock::now();
    return std::chrono::duration_cast<std::chrono::nanoseconds>(t1 - t0).count() + total * 0;
}

static long long bench_pool(std::size_t n) {
    std::vector<Node> pool(n);    // 一次性分配
    long long total = 0;
    auto t0 = std::chrono::steady_clock::now();
    for (std::size_t i = 0; i < n; ++i) {
        pool[i].v = static_cast<int>(i);  // 复用，无堆分配
        total += pool[i].v;
    }
    auto t1 = std::chrono::steady_clock::now();
    return std::chrono::duration_cast<std::chrono::nanoseconds>(t1 - t0).count() + total * 0;
}

int main() {
    const std::size_t N = 1'000'000;
    long long r = bench_raw(N);
    long long p = bench_pool(N);
    std::printf("raw  : %lld ns\n", r);
    std::printf("pool  : %lld ns\n", p);
    std::printf("sink  : %lld %lld\n", r, p);
    return 0;
}
