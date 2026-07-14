// ch77 vector 汇编实证 —— push_back 扩容的几何增长与真实分配代价
#include <vector>
#include <cstdint>

// 观测 1: push_back 触发的扩容路径 —— 运算符 new 的摊还代价
void push_three(std::vector<int>& v) {
    v.push_back(1);  // capacity=0 → 分配 1 个 int
    v.push_back(2);  // capacity=1 → 扩容到 2 → realloc: new[2] + copy 1 + delete[1]
    v.push_back(3);  // capacity=2 → 扩容到 4 → realloc: new[4] + copy 2 + delete[2]
}

// 观测 2: reserve 预分配后的 push_back —— 无分配、纯 in-place
void push_after_reserve() {
    std::vector<int> v;
    v.reserve(3);    // 一次性分配 3*sizeof(int)=12 字节
    v.push_back(1);  // 无分配! 仅 1 条 mov
    v.push_back(2);  // 无分配!
    v.push_back(3);  // 无分配!
}

// 观测 3: growth factor —— GCC libstdc++ 的扩容策略
// 默认 2x: capacity=4 → 8 → 16 → 32 ...
// MSVC 用 1.5x: 4 → 6 → 9 → 14 ...
// 2x 浪费内存(峰值 100% waste)、1.5x 更安全(≤50% waste, 可复用旧块)
void observe_capacity_after_push(std::vector<int>& v) {
    size_t old_cap = v.capacity();
    v.push_back(42);
    // capacity() 变化反映增长因子
}

// 观测 4: emplace_back vs push_back —— 如果参数类型匹配，汇编等价
struct Point { int x, y, z; Point(int a, int b, int c) : x(a), y(b), z(c) {} };
void emplace_vs_push_value(std::vector<Point>& v) {
    v.emplace_back(1, 2, 3);     // 原地构造 (1 次 new 调用)
    v.push_back(Point{4, 5, 6}); // 临时对象移动构造 (但 RVO 优化后等价)
}

// 观测 5: shrink_to_fit —— 真的能回收吗? (libstdc++ 实现: 总是建新块 copy)
void shrink_test() {
    std::vector<int> v;
    for (int i = 0; i < 100; ++i) v.push_back(i);   // capacity=128
    v.resize(10);
    v.shrink_to_fit();                                // → new[10] + copy 10 + delete[128]
}
