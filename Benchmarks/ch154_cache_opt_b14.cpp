// ⑭ 反例：用 vector<vector<int>> 既破坏连续，又叠加列优先 → 双重惩罚
#include <iostream>
#include <vector>
#include <chrono>

int main() {
    constexpr int M = 2048;
    std::vector<std::vector<int>> a(M, std::vector<int>(M, 1));
    long s = 0;
    auto t0 = std::chrono::steady_clock::now();
    for (int j = 0; j < M; ++j)                 // 列优先 + 每层独立分配
        for (int i = 0; i < M; ++i) s += a[i][j];
    auto t1 = std::chrono::steady_clock::now();
    std::cout << "jagged-col =" << std::chrono::duration<double, std::milli>(t1 - t0).count()
              << "ms sum=" << s << "\n";
    return 0;
}