// C2 前置示例：重复 N 次求平均，体现"多次测量"的雏形
#include <iostream>
#include <chrono>
static long long dot(const long long* a, const long long* b, int n) {
    long long s = 0; for (int i = 0; i < n; ++i) s += a[i] * b[i]; return s;
}
int main() {
    const int N = 1000; long long a[N], b[N];
    for (int i = 0; i < N; ++i) { a[i] = i; b[i] = N - i; }
    const int REPEAT = 1000;
    auto t0 = std::chrono::steady_clock::now();
    volatile long long sink = 0;
    for (int r = 0; r < REPEAT; ++r) sink += dot(a, b, N);
    auto t1 = std::chrono::steady_clock::now();
    double us = std::chrono::duration_cast<std::chrono::microseconds>(t1 - t0).count();
    std::cout << "avg per call = " << (us * 1000.0 / REPEAT) << " ns\n";
    return 0;
}