// ch95 示例：排序算法 sort / stable_sort / nth_element 的汇编取证
// 编译（仅生成汇编，不链接）：
//   g++ -std=c++23 -O2 -S -masm=intel _ch95_sort.cpp -o _ch95_sort.asm
// 目的：展示 sort 调用 libstdc++ 内省排序（introsort）实现，stable_sort 解析到归并路径。
#include <algorithm>
#include <vector>

// 1) 默认升序 sort -> 内省排序 introsort
void sort_asc(std::vector<int>& v) {
    std::sort(v.begin(), v.end());
}

// 2) 自定义比较器 sort
void sort_desc(std::vector<int>& v) {
    std::sort(v.begin(), v.end(), [](int a, int b) { return a > b; });
}

// 3) stable_sort -> 需要稳定性的归并实现
void stable_sort_asc(std::vector<int>& v) {
    std::stable_sort(v.begin(), v.end());
}

// 4) nth_element：仅对第 n 个位置划分
void median_partition(std::vector<int>& v) {
    if (!v.empty())
        std::nth_element(v.begin(), v.begin() + v.size() / 2, v.end());
}
