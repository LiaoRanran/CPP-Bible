// 文件：Examples/_ch100_bench.cpp
// 用途：chrono 实测 惰性管道 vs 及早旧写法（避免临时容器 / 单次遍历）
#include <vector>
#include <ranges>
#include <algorithm>
#include <iterator>
#include <numeric>
#include <chrono>
#include <iostream>
#include <random>

int main() {
    std::mt19937 rng(42);
    std::vector<int> v(2'000'000);
    for (auto& x : v) x = static_cast<int>(rng() % 100) - 50;  // ~[-50,49]

    // 旧写法：两次临时容器 + 两次遍历 + 堆分配
    {
        auto t0 = std::chrono::steady_clock::now();
        std::vector<int> pos;
        std::copy_if(v.begin(), v.end(), std::back_inserter(pos),
                     [](int x) { return x > 0; });
        std::vector<int> doubled(pos.size());
        std::transform(pos.begin(), pos.end(), doubled.begin(),
                       [](int x) { return x * 2; });
        long long s = 0;
        for (int x : doubled) s += x;
        auto t1 = std::chrono::steady_clock::now();
        std::cout << "eager: " << std::chrono::duration<double, std::milli>(t1 - t0).count()
                  << " ms  sum=" << s << "\n";
    }

    // 惰性管道：单次遍历 + 零临时容器
    {
        auto t0 = std::chrono::steady_clock::now();
        long long s = 0;
        for (int x : v
                 | std::views::filter([](int x) { return x > 0; })
                 | std::views::transform([](int x) { return x * 2; })) {
            s += x;
        }
        auto t1 = std::chrono::steady_clock::now();
        std::cout << "lazy:  " << std::chrono::duration<double, std::milli>(t1 - t0).count()
                  << " ms  sum=" << s << "\n";
    }
}
