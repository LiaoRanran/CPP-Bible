// ③ 防止优化（一）：volatile 汇点 + 编译器屏障
// 见 Examples/_ch151_dce_volatile.cpp
#include <cstdio>
#include <chrono>

// 编译器屏障：阻止编译器跨该行重排/删除（不影响 CPU 乱序）
#define COMPILER_BARRIER() asm volatile("" ::: "memory")

int main() {
    const int N = 50'000'000;
    long long acc = 0;
    auto t0 = std::chrono::steady_clock::now();
    for (int i = 0; i < N; ++i) {
        acc += i;
        COMPILER_BARRIER();          // 每次迭代都"可见"，防止循环被优化掉
    }
    auto t1 = std::chrono::steady_clock::now();
    std::printf("barrier: elapsed_ms=%.3f acc=%lld\n",
                std::chrono::duration<double, std::milli>(t1 - t0).count(), acc);
    return 0;
}
