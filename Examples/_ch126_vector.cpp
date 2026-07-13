// 文件：Examples/_ch126_vector.cpp
// 演示 std::vector 遍历被内联为指针算术（证明容器逻辑是 header-only 模板）。
// 真实 g++ 编译取汇编（见 ⑧/⑱）。
#include <vector>

int sum_vector(const std::vector<int>& v) {
    int s = 0;
    for (int x : v) s += x;   // 期望被完全内联
    return s;
}

int main() {
    std::vector<int> v{1, 2, 3, 4, 5};
    return sum_vector(v);
}
