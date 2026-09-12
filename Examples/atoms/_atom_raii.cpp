// Examples/_atom_raii.cpp
// 服务 ATOM-MEM-RAII-001：RAII 在异常路径也不泄漏。
// 核心：资源生命周期绑定到对象生命周期——构造获取、析构释放；栈展开时（即使异常）析构自动调用。
// 对照：裸 new/delete 在异常路径跳过 delete => 泄漏（g_live 计数不归零）。
#include <iostream>
#include <stdexcept>

volatile int g_live = 0;                 // volatile：防 -O2 把计数折叠（M2 §5）

struct RAII {
    RAII() { g_live = g_live + 1; }
    ~RAII() { g_live = g_live - 1; }   // 栈展开时仍被调用（g_live 是唯一下减量 => 归 0 即证明析构执行）
};

void safe_path() {
    RAII r;                              // 构造获取资源
    throw std::runtime_error("boom");    // 栈展开时 r 的析构自动调用
}

void leak_path() {
    g_live = g_live + 1;                 // 裸分配计数 +1
    int* p = new int[100];              // 裸资源
    (void)p;
    throw std::runtime_error("boom");    // 异常跳过后面的 delete => 泄漏
    // delete[] p;                      // 不可达
}

int main() {
    try { safe_path(); } catch (...) { /* 捕获，继续 */ }
    std::cout << "after safe_path g_live=" << g_live << "\n";   // 0 => RAII 析构已调用（无泄漏）
    try { leak_path(); } catch (...) { /* 捕获 */ }
    std::cout << "after leak_path g_live=" << g_live << "\n";  // 1 => 裸分配未释放（泄漏）
    return 0;
}
