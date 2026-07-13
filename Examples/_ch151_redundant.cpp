// ⑭' 反模式：测量了"重复代码"而非"被测代码"
// 见 Examples/_ch151_redundant.cpp（错误示范：建表计入被测段）
#include <cstdio>
#include <vector>
#include <chrono>

int main() {
    const int N = 2'000'000;
    // 错误：把 vector 构造/填充也计时了，掩盖了真正要测的求和
    auto t0 = std::chrono::steady_clock::now();
    std::vector<int> v(N);
    for (int i = 0; i < N; ++i) v[i] = i;     // ← 这部分不该算进"求和基准"
    volatile long long s = 0;
    for (int x : v) s += x;
    auto t1 = std::chrono::steady_clock::now();
    std::printf("redundant: ms=%.3f (含建表开销，数字不可信)\n",
                std::chrono::duration<double, std::milli>(t1 - t0).count());
    return 0;
}
