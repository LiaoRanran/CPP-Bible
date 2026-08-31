#include <vector>
#include <algorithm>
// 文件：Examples/_ch95_for_each.cpp
// 行号：32
// square_inplace：无捕获 lambda 修改元素，同样被内联
void square_inplace(std::vector<int>& v) {
    std::for_each(v.begin(), v.end(), [](int& x) { x = x * x; });
}