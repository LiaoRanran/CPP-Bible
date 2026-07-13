// C9 服务端延迟采样：warmup 后反复测一个 handler，报告 p50/p95/p99
#include <iostream>
#include <vector>
#include <algorithm>
#include <chrono>
static long long handle(long long req) { return req * 7 + 1; }   // 模拟请求处理
int main() {
    const int N = 2000;
    std::vector<double> samples; samples.reserve(N);
    // warmup
    volatile long long w = 0; for (int i = 0; i < 100; ++i) w += handle(i);
    for (int i = 0; i < N; ++i) {
        auto t0 = std::chrono::steady_clock::now();
        volatile long long r = handle(i);
        auto t1 = std::chrono::steady_clock::now();
        samples.push_back(std::chrono::duration_cast<std::chrono::nanoseconds>(t1 - t0).count());
    }
    std::sort(samples.begin(), samples.end());
    auto pct = [&](double p){ return samples[static_cast<std::size_t>(p * (N - 1))]; };
    std::cout << "p50=" << pct(0.50) << " p95=" << pct(0.95) << " p99=" << pct(0.99)
              << " ns (sink=" << w << ")\n";
    return 0;
}