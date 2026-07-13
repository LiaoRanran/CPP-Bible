// C1 最小可测：用 steady_clock 测一个函数耗时（纳秒）
#include <iostream>
#include <chrono>
static long long work(long long n) { long long s = 0; for (long long i = 0; i < n; ++i) s += i; return s; }
int main() {
    auto t0 = std::chrono::steady_clock::now();
    volatile long long sink = work(1'000'000);     // volatile 防止被优化掉
    auto t1 = std::chrono::steady_clock::now();
    auto ns = std::chrono::duration_cast<std::chrono::nanoseconds>(t1 - t0).count();
    std::cout << "work took " << ns << " ns  sink=" << sink << "\n";
    return 0;
}