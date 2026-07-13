// 文件：Examples/_ch100_custom_view.cpp
// 用途：一个最简可编译的自定义 view（C++20 range adaptor closure）
#include <ranges>
#include <vector>
#include <iostream>

// 把每个元素乘以固定因子：用 views::transform 包装成管道算子
template <std::integral T>
auto scale(T factor) {
    return std::views::transform(
        [factor](T x) { return static_cast<T>(x * factor); });
}

int main() {
    std::vector<int> v = {1, 2, 3, 4};
    for (int x : v | scale(10)) std::cout << x << ' ';  // 10 20 30 40
    std::cout << '\n';
}
