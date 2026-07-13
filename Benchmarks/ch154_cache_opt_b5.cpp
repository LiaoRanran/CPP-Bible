// ⑥ 软件预取：提前 k 步搬数据， hide 延迟（rw=0 读，locality=3 尽量留多级缓存）
#include <iostream>
#include <vector>
#include <chrono>

int main() {
    constexpr int N = 32'000'000;
    std::vector<int> a(N);
    for (int i = 0; i < N; ++i) a[i] = i;
    constexpr int P = 16;                      // 提前 16 个元素预取
    long s = 0;
    auto t0 = std::chrono::steady_clock::now();
    for (int i = 0; i < N; ++i) {
        if (i + P < N) __builtin_prefetch(&a[i + P], 0, 3);
        s += a[i];
    }
    auto t1 = std::chrono::steady_clock::now();
    std::cout << "prefetch=" << std::chrono::duration<double, std::milli>(t1 - t0).count()
              << "ms sum=" << s << "\n";
    return 0;
}