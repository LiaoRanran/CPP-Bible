// ⑩' 列主序遍历（cache 不友好）—— 真实时序见正文
// 见 Examples/_ch151_cache_colmajor.cpp
#include <cstdio>
#include <vector>
#include <chrono>

int main() {
    const int R = 4000, C = 4000;
    std::vector<std::vector<int>> m(R, std::vector<int>(C, 1));
    auto t0 = std::chrono::steady_clock::now();
    volatile long long s = 0;
    for (int j = 0; j < C; ++j)            // 外层列
        for (int i = 0; i < R; ++i)
            s += m[i][j];                   // 跨行跳步访问
    auto t1 = std::chrono::steady_clock::now();
    std::printf("col-major: ms=%.3f s=%lld\n",
                std::chrono::duration<double, std::milli>(t1 - t0).count(), (long long)s);
    return 0;
}
