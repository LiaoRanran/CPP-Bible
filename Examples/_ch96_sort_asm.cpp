#include <algorithm>
#include <vector>

// 触发 std::sort 真实实例化，观察 __introsort / __unguarded_partition 相关符号
void sort_demo(std::vector<int>& v) {
    std::sort(v.begin(), v.end());
}

int main() {
    std::vector<int> v{5, 3, 8, 1, 9, 2, 7, 4, 6, 0};
    sort_demo(v);
    return v.front();
}
