#include <set>

// 批 L4：set 红黑树每元素 operator new + find 沿左右指针追逐（键即值@0）
int main() {
    std::set<int> s;
    for (int i = 0; i < 100; ++i) s.insert(i);  // 红黑树节点分配
    volatile bool found = (s.find(42) != s.end());
    (void)found;
    return 0;
}
