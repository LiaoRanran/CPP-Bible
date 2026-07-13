// ch144 ⑧ 范围 for 与下标/迭代器循环生成等价机器码
// 编译：g++ -std=c++23 -O2 -S -masm=intel _ch144_rangefor.cpp -o _ch144_rangefor_O2.asm
#include <vector>

void by_index(const std::vector<int>& v, long& acc) {
    for (std::size_t i = 0; i < v.size(); ++i) acc += v[i];
}

void by_iterator(const std::vector<int>& v, long& acc) {
    for (auto it = v.begin(); it != v.end(); ++it) acc += *it;
}

void by_range(const std::vector<int>& v, long& acc) {
    for (auto x : v) acc += x;   // ✅ 范围 for
}
