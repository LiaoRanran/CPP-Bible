// C16 易错点1：未预热——前几次含冷启动开销，污染中位数
#include <iostream>
#include <chrono>
static long long work() { long long s = 0; for (int i = 0; i < 100000; ++i) s += i; return s; }
int main() {
    // ❌ 直接采样，第一次可能含页错误/缓存冷
    for (int r = 0; r < 5; ++r) {
        auto t0 = std::chrono::steady_clock::now();
        volatile long long x = work();
        auto t1 = std::chrono::steady_clock::now();
        std::cout << "run" << r << "=" << (t1 - t0).count() << "ns x=" << x << "\n";
    }
    return 0;
}
// ✅ 正确做法：循环开始前先跑 100 次 warmup（见 C9）。