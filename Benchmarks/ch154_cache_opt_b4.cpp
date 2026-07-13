// ⑤ 冲突未命中演示：下标间隔 = 关联度×行大小 时反复同槽
#include <iostream>
#include <vector>
#include <chrono>

int main() {
    constexpr int N = 1 << 24;                 // 16M int = 64MB
    std::vector<int> a(N, 1);
    constexpr int STEP = 1 << 16;              // 256K int = 1MB 跨步，易撞同组
    long s = 0;
    auto t0 = std::chrono::steady_clock::now();
    for (int i = 0; i < N; i += STEP) s += a[i];
    auto t1 = std::chrono::steady_clock::now();
    std::cout << "conflict-walk=" << std::chrono::duration<double, std::milli>(t1 - t0).count()
              << "ms sum=" << s << "\n";
    return 0;
}