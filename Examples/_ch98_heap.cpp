#include <vector>
#include <algorithm>

// 用于取证 push_heap（sift-up）的真实汇编
void do_push(std::vector<int>& v, int x) {
    v.push_back(x);
    std::push_heap(v.begin(), v.end());
}

// 用于取证 pop_heap（sift-down）的真实汇编
int do_pop(std::vector<int>& v) {
    std::pop_heap(v.begin(), v.end());
    int x = v.back();
    v.pop_back();
    return x;
}

// 用于取证 make_heap
void do_make(std::vector<int>& v) {
    std::make_heap(v.begin(), v.end());
}

// 用于取证 sort_heap
void do_sort(std::vector<int>& v) {
    std::sort_heap(v.begin(), v.end());
}
