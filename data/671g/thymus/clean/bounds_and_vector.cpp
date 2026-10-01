// 已知无缺陷：边界与容器（D3 胸腺正确代码库；人工确认）
#include <numeric>
#include <vector>

long long sum_first_n(const std::vector<int>& v, std::size_t n) {
    const std::size_t take = n < v.size() ? n : v.size();   // 边界先夹紧，无越界
    return std::accumulate(v.begin(), v.begin() + static_cast<std::ptrdiff_t>(take), 0LL);
}

int main() {
    std::vector<int> v{1, 2, 3};
    return sum_first_n(v, 10) == 6 ? 0 : 1;
}
