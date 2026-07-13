// 补-E 顺序写大数组（write-allocate 友好），计时
#include <iostream>
#include <vector>
#include <chrono>

int main() {
    constexpr int N = 50'000'000;
    std::vector<int> a(N);
    auto t0 = std::chrono::steady_clock::now();
    for (int i = 0; i < N; ++i) a[i] = i;
    auto t1 = std::chrono::steady_clock::now();
    std::cout << "fill=" << std::chrono::duration<double, std::milli>(t1 - t0).count() << "ms\n";
    return 0;
}