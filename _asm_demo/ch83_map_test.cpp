// ASM-83-map : std::map 节点布局真机汇编实证（GCC 15.3.0, C++26, -O2）
// 目标：证明 std::map 是红黑树——每个元素独立堆分配（operator new），find 是 O(log n) 指针追逐，
//       与 vector/array 的连续内存、零分配、O(1) 随机访问形成对比。
#include <map>
#include <iostream>

// 构造：每个元素一次堆分配（红黑树节点）
std::map<int, int> build() {
    std::map<int, int> m;
    m[1] = 10;
    m[2] = 20;
    m[3] = 30;
    return m;
}

// 查找：沿左右子指针比较键，O(log n) 指针追逐
int find_it(const std::map<int, int>& m, int k) {
    auto it = m.find(k);
    return it != m.end() ? it->second : -1;
}

int main() {
    auto m = build();
    volatile int sink = find_it(m, 2);   // 期望：call operator new（构造）+ 指针追逐（查找）
    return (int)sink;
}
