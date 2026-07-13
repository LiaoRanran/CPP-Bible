// ⑩ 行主序遍历（cache 友好）—— 真实时序见正文
// 见 Examples/_ch151_cache_rowmajor.cpp
#include <cstdio>
#include <vector>
#include <chrono>

int main() {
    const int R = 4000, C = 4000;
    std::vector<std::vector<int>> m(R, std::vector<int>(C, 1));
    auto t0 = std::chrono::steady_clock::now();
    volatile long long s = 0;
    for (int i = 0; i < R; ++i)            // 外层行
        for (int j = 0; j < C; ++j)
            s += m[i][j];                   // 连续内存访问
    auto t1 = std::chrono::steady_clock::now();
    std::printf("row-major: ms=%.3f s=%lld\n",
                std::chrono::duration<double, std::milli>(t1 - t0).count(), (long long)s);
    return 0;
}
