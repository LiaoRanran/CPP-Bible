// 文件：Examples/_ch99_ranges.cpp
// 行号：9 (rng_sum) / 15 (rng_fold)
#include <ranges>
#include <numeric>
#include <algorithm>
#include <execution>
#include <vector>
#include <iostream>

// ranges + views 管线后求和（惰性，无临时大容器）
double rng_sum(const std::vector<double>& v) {
    auto view = v | std::views::filter([](double x){ return x > 0; })
                   | std::views::transform([](double x){ return x * x; });
    return std::reduce(std::execution::seq, view.begin(), view.end(), 0.0);
}

// 用 ranges::fold_left（C++23）替代 accumulate
double rng_fold(const std::vector<int>& v) {
    return std::ranges::fold_left(v, 0, std::plus<>());
}

int main() {
    std::vector<double> v{1,-2,3,-4,5};
    std::vector<int> w{1,2,3};
    std::cout << rng_sum(v) << " " << rng_fold(w) << "\n";
}
