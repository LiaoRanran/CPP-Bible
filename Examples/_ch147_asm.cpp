// _ch147_asm.cpp —— 编译期优化取证（RAII 作用域退出）
// 取证命令:
//   g++ -std=c++23 -O2 -S -masm=intel _ch147_asm.cpp -o _ch147_asm.asm
#include <mutex>

std::mutex g_mtx;

void critical_section() {
    std::lock_guard<std::mutex> lk(g_mtx);   // 构造加锁，析构解锁
    // ... 临界区（此处为空，便于观察 RAII 展开）
}
