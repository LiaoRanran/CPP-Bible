// 文件：Examples/_ch13_use.cpp
// 行号：1
// 消费「被包管理器提供的头-only 包」的使用程序。
// 它演示：一旦包被解析并暴露 include 路径，用户代码仅需 #include 即用。
#include "_ch13_packlib.hpp"
#include <array>

int main() {
    using pkg::span_view;
    using pkg::println;

    std::array<int, 4> a{1, 2, 3, 4};
    span_view<int> v(a.data(), a.size());   // 非拥有视图

    int sum = 0;
    for (std::size_t i = 0; i < v.size(); ++i) sum += v[i];

    println("sum={}, n={}", sum, v.size());   // fmt 风格输出
    return sum;
}
