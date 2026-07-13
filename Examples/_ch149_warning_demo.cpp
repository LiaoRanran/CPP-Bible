// ② CI 门禁实例：未初始化变量 + 有符号/无符号比较
#include <cstdio>
#include <vector>

int risk_sum(const std::vector<unsigned>& v) {
    int total;                 // ❌ 未初始化
    for (unsigned i = 0; i < v.size(); ++i)
        total += static_cast<int>(v[i]);   // ❌ 有/无符号混用
    return total;
}

int main() {
    std::vector<unsigned> v{1, 2, 3};
    std::printf("%d\n", risk_sum(v));
}
