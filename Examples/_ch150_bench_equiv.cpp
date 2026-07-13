// ⑪ 基准测试等价：计时 std::vector push_back（结果经 volatile 下沉防 DCE）
#include <cstdio>
#include <vector>
#include <chrono>
int main() {
    const int N = 5'000'000;
    volatile unsigned sink = 0;  // 防止编译器把计时循环整体消除
    auto t0 = std::chrono::steady_clock::now();
    std::vector<int> v;
    for (int i = 0; i < N; ++i) v.push_back(i);
    auto t1 = std::chrono::steady_clock::now();
    sink = v.size();
    double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
    std::printf("bench-equiv: push_back x%d -> %.2f ms (size=%u)\n", N, ms, (unsigned)sink);
    return 0;
}
