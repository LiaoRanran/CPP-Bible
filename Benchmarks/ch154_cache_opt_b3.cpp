// ④ 空间局部性：顺序访问 vs 大步长访问（后者每行只用一个字，浪费 63 字节）
#include <iostream>
#include <vector>
#include <chrono>

int main() {
    constexpr int N = 16'000'000;
    std::vector<int> a(N, 1);
    auto t0 = std::chrono::steady_clock::now();
    long s1 = 0; for (int i = 0; i < N; i += 1) s1 += a[i];   // 步长1，空间局部好
    auto t1 = std::chrono::steady_clock::now();
    long s2 = 0; for (int i = 0; i < N; i += 16) s2 += a[i];  // 步长16*4B=64B，每行1元素
    auto t2 = std::chrono::steady_clock::now();
    std::cout << "stride1 =" << std::chrono::duration<double, std::milli>(t1 - t0).count() << "ms\n";
    std::cout << "stride64=" << std::chrono::duration<double, std::milli>(t2 - t1).count() << "ms\n";
    return 0;
}