#include <atomic>
#include <vector>
#include <thread>

// 风险指针(Hazard Pointer)骨架：第112章完整实现
// 核心思想：线程在解引用共享指针前，先"声明"自己正在用这个指针
struct Node { int data; std::atomic<Node*> next; };
alignas(64) static std::atomic<Node*> g_hazard{nullptr};

Node* protect(std::atomic<Node*>& src) {
    Node* p = src.load(std::memory_order_acquire);
    while (true) {
        g_hazard.store(p, std::memory_order_seq_cst);
        Node* p2 = src.load(std::memory_order_acquire);
        if (p == p2) return p;
        p = p2;
    }
}
void retire(Node* p) { /* 延迟回收：确认无人 hazard 后再 delete（见 ch112） */ (void)p; }
