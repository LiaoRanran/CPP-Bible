// Examples/_ch22_auto_zero_cost.cpp
// 真机证据：auto 与显式类型在 -O2 下零开销同构（GCC 15.3.0）
// 编译：g++ -O2 -std=c++20 -masm=intel -S 本文件
#include <vector>

int compute() { return 42; }

int via_auto() {
    auto x = compute();   // 推导为 int
    return x;
}

int via_explicit() {
    int x = compute();    // 显式 int
    return x;
}

// decltype(auto) 转发工厂：保留引用性、零开销
int& front_ref(std::vector<int>& v) { return v.front(); }

decltype(auto) fwd_front(std::vector<int>& v) {
    return front_ref(v);   // decltype(auto) 保留 int&
}
