// ③' 夹具测试 std::vector 生命周期与容量增长
#include <cstdio>
#include <vector>
#include <cassert>
int main() {
    std::vector<int> v;          // setup
    v.push_back(1); v.push_back(2); v.push_back(3);
    assert(v.size() == 3);
    assert(v.capacity() >= 3);
    v.clear();                   // teardown
    assert(v.empty());
    std::printf("fixture<vector>: size after clear=%zu\n", v.size());
    return 0;
}
