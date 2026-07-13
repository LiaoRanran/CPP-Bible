// _ch147_refactor.cpp —— 坏味道：过长函数 / 重复代码（对照重构）
#include <string>
#include <vector>

// 坏味道：一个函数做太多事
int bad_report(const std::vector<int>& a, const std::vector<int>& b) {
    int sa = 0;
    for (auto x : a) sa += x;
    int sb = 0;
    for (auto x : b) sb += x;
    return sa + sb;
}

// 重构：抽取命名函数，消除重复
int sum_of(const std::vector<int>& v) {
    int s = 0;
    for (auto x : v) s += x;
    return s;
}
int good_report(const std::vector<int>& a, const std::vector<int>& b) {
    return sum_of(a) + sum_of(b);
}
