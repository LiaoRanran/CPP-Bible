// _bench_d5_15_profiling.cpp  (GCC 15.3.0, g++ -O2 -std=c++23)
// 真实基准：profiling 章节的核心教训——测一次 now() 本身要花多少钱。
// 若把时间戳打在热循环内部，测量开销会淹没被测工作。
// 循环内用 asm volatile fence 阻止 DCE。
#include <chrono>
#include <iostream>

static long long sink = 0;

int main() {
    const int N = 50'000'000;
    using namespace std::chrono;

    // 基线：循环内什么都不测
    {
        auto t0 = steady_clock::now();
        long long s = 0; for (int i = 0; i < N; ++i) { s += i; asm volatile("" : "+r"(s) :: "memory"); }
        auto t1 = steady_clock::now();
        sink += s;
        std::cout << "baseline (no clock) : " << (t1 - t0).count() / 1e6 << " ms" << std::endl;
    }
    // 循环内每次都取一次 now()
    {
        auto t0 = steady_clock::now();
        long long s = 0; for (int i = 0; i < N; ++i) { auto t = steady_clock::now(); s += i;
            asm volatile("" : "+r"(s), "+r"(t) :: "memory"); }
        auto t1 = steady_clock::now();
        sink += s;
        std::cout << "now() inside loop  : " << (t1 - t0).count() / 1e6 << " ms" << std::endl;
    }
    std::cout << "sink=" << sink << std::endl;
    return 0;
}
