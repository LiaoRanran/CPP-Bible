// Examples/_atom_unique_move.cpp
// 服务 ATOM-MEM-UNIQUE-001：unique_ptr 移动转移所有权（源置空），析构恰好一次（唯一所有权，无双释放）。
// 拷贝被删除：取消注释 `std::unique_ptr<Box> c = a;` 会编译红（[unique.ownership] copy deleted）。
#include <memory>
#include <iostream>

volatile int g_destroy = 0;               // volatile：防折叠（M2 §5）
struct Box { int v; Box(int i) : v(i) {} ~Box() { g_destroy = g_destroy + 1; } };

int main() {
    {
        std::unique_ptr<Box> a = std::make_unique<Box>(7);
        std::unique_ptr<Box> b = std::move(a);   // 移动转移所有权
        std::cout << "after move a empty=" << (!a) << "\n";   // 源被置空
        std::cout << "b->v=" << b->v << "\n";                 // 所有权已转移到 b
        // std::unique_ptr<Box> c = a;   // 编译错误：拷贝构造被删除（证伪"unique_ptr 可拷贝"）
    }                                          // b 离开作用域，Box 析构恰好一次
    std::cout << "box destroyed count=" << g_destroy << "\n";  // 1 => 唯一所有权，无双释放
    return 0;
}
