// Examples/_atom_shared_cycle.cpp
// 服务 ATOM-MEM-SHARED-001（证伪卡）：两个对象互相 shared_ptr 持有 => 循环引用，计数永不归零 => 泄漏。
// 这证明"shared_ptr 总能管好生命周期"是错的——循环引用必须靠 weak_ptr 打破（见 ATOM-MEM-WEAK-001）。
#include <memory>
#include <iostream>

volatile int g_destroy = 0;                 // volatile：防折叠（M2 §5）
struct Node;
using P = std::shared_ptr<Node>;
struct Node { ~Node() { g_destroy = g_destroy + 1; } P next; };

int main() {
    {
        P a = std::make_shared<Node>();
        P b = std::make_shared<Node>();
        a->next = b;                         // a 持有 b
        b->next = a;                         // b 持有 a  -> 循环引用
        std::cout << "a use_count=" << a.use_count() << "\n";   // 2
        std::cout << "b use_count=" << b.use_count() << "\n";   // 2
    }                                        // a,b 离开作用域：各自计数 2->1（互相仍持有），都不归零 -> 泄漏
    std::cout << "nodes destroyed count=" << g_destroy << "\n";  // 0 => 循环引用泄漏
    return 0;
}
