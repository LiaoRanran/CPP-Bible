// ch95 示例：std::for_each / transform / count_if / accumulate 的内联取证
// 编译（仅生成汇编，不链接）：
//   g++ -std=c++23 -O2 -S -masm=intel _ch95_for_each.cpp -o _ch95_for_each.asm
// 目的：证明高层算法在 -O2 下被完全内联为等价手写循环，零抽象开销。
#include <algorithm>
#include <numeric>
#include <vector>

// 1) for_each + 有状态 lambda：编译器把 lambda 体原样内联进循环
long sum_of_squares(const std::vector<int>& v) {
    long s = 0;
    std::for_each(v.begin(), v.end(),
                  [&s](int x) { s += static_cast<long>(x) * x; });
    return s;
}

// 2) transform：原地缩放
void scale_by(std::vector<double>& v, double k) {
    std::transform(v.begin(), v.end(), v.begin(),
                   [k](double x) { return x * k; });
}

// 3) count_if：统计偶数个数
long count_even(const std::vector<int>& v) {
    return std::count_if(v.begin(), v.end(),
                         [](int x) { return x % 2 == 0; });
}

// 4) accumulate：求和（与手写循环等价）
long total(const std::vector<int>& v) {
    return std::accumulate(v.begin(), v.end(), 0L);
}

// 5) for_each + 无捕获 lambda：纯计算
void square_inplace(std::vector<int>& v) {
    std::for_each(v.begin(), v.end(), [](int& x) { x = x * x; });
}
