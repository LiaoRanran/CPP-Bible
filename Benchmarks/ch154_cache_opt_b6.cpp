// ⑦ 顺序写（write-allocate+write-back）：连续 64B 只触发极少内存事务
#include <iostream>
#include <vector>
#include <chrono>

int main() {
    constexpr int N = 64'000'000;
    std::vector<char> a(N, 0);
    auto t0 = std::chrono::steady_clock::now();
    for (int i = 0; i < N; ++i) a[i] = char(i);      // 顺序写，命中 write-allocate
    auto t1 = std::chrono::steady_clock::now();
    std::cout << "seq-write=" << std::chrono::duration<double, std::milli>(t1 - t0).count()
              << "ms\n";
    return 0;
}