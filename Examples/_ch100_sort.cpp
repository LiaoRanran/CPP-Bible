// 文件：Examples/_ch100_sort.cpp
// 用途：ranges::sort（含投影）与 ranges 管道写法，取真实 -O2 汇编证据
#include <algorithm>
#include <vector>
#include <ranges>

// 用 ranges::sort 直接排序（算法式调用）
void sort_plain(std::vector<int>& v) {
    std::ranges::sort(v);
}

// 用 ranges::sort + 投影：按绝对值排序
void sort_by_abs(std::vector<int>& v) {
    std::ranges::sort(v, std::ranges::less{}, [](int x) { return x < 0 ? -x : x; });
}

// 管道写法：filter 正数 -> transform *2 -> 累加（惰性，无临时容器）
int pipe_sum(const std::vector<int>& v) {
    auto r = v
           | std::views::filter([](int x) { return x > 0; })
           | std::views::transform([](int x) { return x * 2; });
    int s = 0;
    for (int x : r) s += x;
    return s;
}
