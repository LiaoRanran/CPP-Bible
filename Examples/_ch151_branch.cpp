// ⑪'' 分支（汇编见 _ch151_branch.asm）
// 见 Examples/_ch151_branch.cpp
#include <cstdio>
#include <chrono>

int main() {
    const int N = 100'000'000;
    auto t0 = std::chrono::steady_clock::now();
    volatile int r = 0;
    for (int i = 0; i < N; ++i) {
        if (i & 1) r += i * 2;        // 数据相关分支
        else       r += i + 7;
    }
    auto t1 = std::chrono::steady_clock::now();
    std::printf("branch: ms=%.3f r=%d\n",
                std::chrono::duration<double, std::milli>(t1 - t0).count(), r);
    return 0;
}
