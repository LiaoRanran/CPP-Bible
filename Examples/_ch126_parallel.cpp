// 文件：Examples/_ch126_parallel.cpp
// 演示并行算法 API（std::execution::par）。MS STL 的并行后端是
// Intel oneTBB + Concurrency Runtime（见 ⑦）；此处用 g++/libstdc++ 仅验证 API 可编译。
#include <algorithm>
#include <execution>
#include <vector>
#include <cmath>

int main() {
    std::vector<double> a(1024);
    for (std::size_t i = 0; i < a.size(); ++i) a[i] = static_cast<double>(i);
    std::sort(std::execution::par, a.begin(), a.end(),
              [](double x, double y) { return std::fabs(x) < std::fabs(y); });
    return static_cast<int>(a.size());
}
