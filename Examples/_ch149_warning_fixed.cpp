// ② 修复后版本：同一个逻辑，干净通过 -Werror
#include <cstdio>
#include <vector>

int safe_sum(const std::vector<unsigned>& v) {
    int total = 0;
    for (std::size_t i = 0; i < v.size(); ++i)
        total += static_cast<int>(v[i]);
    return total;
}

int main() {
    std::vector<unsigned> v{1, 2, 3};
    std::printf("%d\n", safe_sum(v));
}
