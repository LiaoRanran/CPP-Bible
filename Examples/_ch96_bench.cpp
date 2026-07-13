#include <algorithm>
#include <chrono>
#include <iostream>
#include <random>
#include <vector>

// 真实性能取证：用 chrono 测量 std::sort 在不同规模下的耗时
int main() {
    std::mt19937 rng(42);
    const int N[] = {1000, 100000, 1000000};
    for (int n : N) {
        std::vector<int> v(n);
        std::generate(v.begin(), v.end(), rng);
        auto t0 = std::chrono::steady_clock::now();
        std::sort(v.begin(), v.end());
        auto t1 = std::chrono::steady_clock::now();
        auto ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
        std::cout << "N=" << n << " sort耗时=" << ms << " ms"
                  << " 已序校验=" << std::is_sorted(v.begin(), v.end()) << "\n";
    }
    return 0;
}
