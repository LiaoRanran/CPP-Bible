#include <vector>
// ① reserve 后 push_back——无分配
void push_after_reserve() {
    std::vector<int> v; v.reserve(3);
    v.push_back(1); v.push_back(2); v.push_back(3);
}
// ② 无 reserve 的第一个 push_back——触发分配
void observe_capacity_after_push(std::vector<int>& v) {
    v.push_back(42);
}