// 文件：Examples/_ch97_lower_bound.cpp
// 编译：g++ -std=c++23 -O2 -S -masm=intel _ch97_lower_bound.cpp -o _ch97_lower_bound.asm
#include <algorithm>

// 在 [first, first+n) 升序区间中，返回第一个 >= value 的下标。
// 用裸指针避免 std::vector 间接层，使 lower_bound 的展开更清晰可见。
int lower_bound_idx(const int* first, int n, int value) {
    auto it = std::lower_bound(first, first + n, value);
    return static_cast<int>(it - first);
}
