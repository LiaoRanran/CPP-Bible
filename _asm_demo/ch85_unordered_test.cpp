// ASM-85-unordered : std::unordered_map 节点布局真机汇编实证（GCC 15.3.0, C++26, -O2）
// 目标：证明 std::unordered_map 是哈希表——节点堆分配 + 桶数组堆分配 + 可能 rehash；
//       find 先哈希定位桶，再沿桶内 next 指针链遍历，平均 O(1) 但最坏退化为链。
#include <unordered_map>
#include <iostream>

// 构造：节点堆分配 + 桶数组堆分配（元素增多触发 rehash → 桶数组再分配）
std::unordered_map<int, int> build() {
    std::unordered_map<int, int> m;
    m[1] = 10;
    m[2] = 20;
    m[3] = 30;
    return m;
}

// 查找：hash(key) → 桶索引 → 沿桶内 next 指针链遍历
int find_it(const std::unordered_map<int, int>& m, int k) {
    auto it = m.find(k);
    return it != m.end() ? it->second : -1;
}

int main() {
    auto m = build();
    volatile int sink = find_it(m, 2);   // 期望：多次 call operator new + rehash + 链表遍历
    return (int)sink;
}
