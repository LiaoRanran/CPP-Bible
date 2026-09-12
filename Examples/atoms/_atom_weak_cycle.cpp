// Examples/_atom_weak_cycle.cpp
// 服务 ATOM-MEM-WEAK-001（证伪卡的反面）：用 weak_ptr 打破 shared_ptr 循环引用。
// 父->子用 shared_ptr、子->父用 weak_ptr，离开作用域后计数能归零，两节点都析构（无泄漏）。
// 对照 EV-MEM-014：同样的结构若子->父也用 shared_ptr 则泄漏。
#include <memory>
#include <iostream>

volatile int g_destroy = 0;                 // volatile：防折叠（M2 §5）
struct Node;
using SP = std::shared_ptr<Node>;
using WP = std::weak_ptr<Node>;
struct Node { ~Node() { g_destroy = g_destroy + 1; } WP parent; SP child; };

int main() {
    {
        SP a = std::make_shared<Node>();
        SP b = std::make_shared<Node>();
        a->child = b;                         // 父 -> 子：shared_ptr（拥有）
        b->parent = a;                        // 子 -> 父：weak_ptr（旁观，不拥有 => 打破循环）
        std::cout << "a use_count=" << a.use_count() << "\n";   // 1（b 只 weak 指向 a）
        std::cout << "b use_count=" << b.use_count() << "\n";   // 2（a 拥有 b + 局部 b）
    }                                        // a,b 离开：a 计数 1->0 释放 -> 释放 a->child(b) -> b 计数归零释放
    std::cout << "nodes destroyed count=" << g_destroy << "\n";  // 2 => 循环被打破，无泄漏
    return 0;
}
