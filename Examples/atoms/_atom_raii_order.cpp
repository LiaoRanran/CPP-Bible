// Examples/_atom_raii_order.cpp
// 服务 ATOM-MEM-RAII-001（第二卡）：RAII 清理是"基于作用域"的——多个对象在同一作用域，
// 栈展开时按构造的逆序析构。这证明"资源生命周期绑定对象生命周期"是逐对象、逆序、跨栈帧的通用机制。
#include <iostream>

struct Tag {
    const char* n;
    Tag(const char* s) : n(s) { std::cout << "ctor " << n << "\n"; }
    ~Tag() { std::cout << "dtor " << n << "\n"; }
};

void f() {
    Tag a("A");
    Tag b("B");
    Tag c("C");
    throw 0;                            // 栈展开：c -> b -> a 逆序析构
}

int main() {
    try { f(); } catch (...) { /* 跨栈帧捕获；dtor C/B/A 已证明栈已展开 */ }
    return 0;
}
