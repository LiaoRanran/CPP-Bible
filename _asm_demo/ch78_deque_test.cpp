#include <deque>

// 批 L1：deque 分块映射 + push_back 块分配
// libstdc++ deque 每块容量 = 512 / sizeof(T) = 128 个 int，跨块需二级指针。
int main() {
    std::deque<int> d;
    for (int i = 0; i < 200; ++i) d.push_back(i);  // 跨 2 个块 -> 触发块分配
    int s = 0;
    for (int i = 0; i < 200; ++i) s += d[i];        // operator[] 双间接
    volatile int sink = s + d[42];
    (void)sink;
    return 0;
}
