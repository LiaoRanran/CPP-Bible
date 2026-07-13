// C7 std::accumulate 与手写循环：二者在 -O2 下通常生成相同汇编，但写法影响可读与编译器优化
#include <iostream>
#include <vector>
#include <numeric>
#include <chrono>
int main() {
    std::vector<long long> v(1'000'000, 1);
    // 手写
    auto t0 = std::chrono::steady_clock::now();
    long long s1 = 0; for (auto x : v) s1 += x;
    auto t1 = std::chrono::steady_clock::now();
    // 算法
    auto t2 = std::chrono::steady_clock::now();
    long long s2 = std::accumulate(v.begin(), v.end(), 0LL);
    auto t3 = std::chrono::steady_clock::now();
    volatile long long sink = s1 + s2;
    std::cout << "hand=" << (t1 - t0).count() << " algo=" << (t3 - t2).count()
              << " sink=" << sink << "\n";
    return 0;
}