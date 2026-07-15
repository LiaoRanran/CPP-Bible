#include <list>

// 批 L2：list 每元素 operator new 节点{prev,next,value} + 遍历纯指针追逐
int main() {
    std::list<int> l;
    for (int i = 0; i < 100; ++i) l.push_back(i);  // 100 次 operator new
    int s = 0;
    for (auto it = l.begin(); it != l.end(); ++it) s += *it;  // 沿 next 指针追逐
    volatile int sink = s;
    (void)sink;
    return 0;
}
