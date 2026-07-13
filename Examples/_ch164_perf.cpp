// ⑬ 性能考量：用 steady_clock 测单 tick 开销（关联 第151章 性能）
// 本机 g++ -std=c++23 -O2 编译运行通过
#include <iostream>
#include <chrono>
#include <vector>
#include <functional>

double bench(const std::string& name, int iters, std::function<void()> fn) {
    auto t0 = std::chrono::steady_clock::now();
    for (int i = 0; i < iters; ++i) fn();
    auto t1 = std::chrono::steady_clock::now();
    double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
    std::cout << "[perf] " << name << ": " << ms << " ms / " << iters
              << " iters = " << (ms / iters * 1e6) << " ns/iter\n";
    return ms;
}

int main() {
    std::vector<int> v;
    bench("vector_push_back", 1'000'000, [&] { v.push_back(1); });
    bench("empty_lambda",      1'000'000, [] {});
    return 0;
}
