// ⑭ 反模式：时钟分辨率不够 → 测出 0 纳秒
// 见 Examples/_ch151_clock_res.cpp
#include <cstdio>
#include <chrono>

int main() {
    // 用最快时钟测一次极短操作，多次尝试看"分辨率地板"
    long long zero = 0;
    for (int k = 0; k < 5; ++k) {
        auto a = std::chrono::steady_clock::now();
        volatile int x = 1 + 1;            // 极短操作
        (void)x;
        auto b = std::chrono::steady_clock::now();
        auto ns = std::chrono::duration_cast<std::chrono::nanoseconds>(b - a).count();
        if (ns == 0) ++zero;
        std::printf("  sample %d: %lld ns\n", k, (long long)ns);
    }
    std::printf("clock_res: zero_ns_samples=%lld/5 (分辨率地板，需用大循环平均)\n", (long long)zero);
    return 0;
}
