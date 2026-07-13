// ⑬ 用一维 vector 模拟二维，对比行优先 / 列优先求和
#include <iostream>
#include <vector>
#include <chrono>

int main() {
    constexpr int M = 4096;
    std::vector<int> a(M * M, 1);
    long sr = 0, sc = 0;

    auto t0 = std::chrono::steady_clock::now();
    for (int i = 0; i < M; ++i)                 // 行优先：a[i*M+j] 连续
        for (int j = 0; j < M; ++j) sr += a[i * M + j];
    auto t1 = std::chrono::steady_clock::now();

    for (int j = 0; j < M; ++j)                 // 列优先：a[i*M+j] 跨行，步长 M*4B
        for (int i = 0; i < M; ++i) sc += a[i * M + j];
    auto t2 = std::chrono::steady_clock::now();

    std::cout << "row =" << std::chrono::duration<double, std::milli>(t1 - t0).count() << "ms\n";
    std::cout << "col =" << std::chrono::duration<double, std::milli>(t2 - t1).count() << "ms\n";
    return 0;
}