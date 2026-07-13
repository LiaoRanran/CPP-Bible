// C5 正确示范：volatile 接收，阻止 DCE
#include <iostream>
#include <chrono>
static long long work(long long n) { long long s = 0; for (long long i = 0; i < n; ++i) s += i; return s; }
int main() {
    auto t0 = std::chrono::steady_clock::now();
    volatile long long sink = work(1'000'000);    // ✅ volatile 强制保留
    auto t1 = std::chrono::steady_clock::now();
    std::cout << "ns=" << std::chrono::duration_cast<std::chrono::nanoseconds>(t1 - t0).count()
              << " sink=" << sink << "\n";
    return 0;
}