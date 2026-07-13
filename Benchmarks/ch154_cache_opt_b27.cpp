// 补-F 软件预取：`__builtin_prefetch` 对顺序访问的加速验证
#include <iostream>
#include <vector>
#include <chrono>
int main() {
    constexpr int N = 1000000, DIST = 64;
    std::vector<int> v(N * DIST, 0);
    for (int i = 0; i < N; ++i) v[i * DIST + (i & 31)] = i;
    volatile long long s = 0;
    auto t0 = std::chrono::steady_clock::now();
    for (int i = 0; i < N; ++i) {
        __builtin_prefetch(&v[(i + 8) * DIST], 0, 3); // 提前 8 步预取
        s += v[i * DIST];
    }
    auto t1 = std::chrono::steady_clock::now();
    std::cout << "prefetch=" << std::chrono::duration<double, std::milli>(t1 - t0).count()
              << "ms s=" << s << "\n";
    return 0;
}