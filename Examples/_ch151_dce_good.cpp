// ①' 正确做法：用 volatile 汇点防止 DCE（汇编见 _ch151_dce_good.asm）
// 见 Examples/_ch151_dce_good.cpp
#include <cstdio>
#include <chrono>

int main() {
    const int N = 100'000'000;
    volatile long long sink = 0;   // volatile：强制每次写入真实内存
    auto t0 = std::chrono::steady_clock::now();
    for (int i = 0; i < N; ++i) {
        sink += i;
    }
    auto t1 = std::chrono::steady_clock::now();
    std::printf("dce_good: elapsed_ms=%.3f sink=%lld\n",
                std::chrono::duration<double, std::milli>(t1 - t0).count(),
                (long long)sink);
    return 0;
}
