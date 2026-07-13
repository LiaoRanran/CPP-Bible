// C26: Google Benchmark 等价体——手动 warmup + iteration 计时
#include <iostream>
#include <chrono>
#include <vector>
static void BM_VectorSum(int n) {
    std::vector<int> v(n, 1);
    volatile long long s = 0;
    for (int i = 0; i < n; ++i) s += v[i];
}
int main() {
    const int N = 1000000, ITERS = 10;
    BM_VectorSum(1000);  // warmup (触达稳定频率)
    auto t0 = std::chrono::steady_clock::now();
    for (int iter = 0; iter < ITERS; ++iter) BM_VectorSum(N);
    auto t1 = std::chrono::steady_clock::now();
    double ms = std::chrono::duration<double, std::milli>(t1 - t0).count() / ITERS;
    std::cout << "avg per iteration = " << ms << " ms\n";
    return 0;
}