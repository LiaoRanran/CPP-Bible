#include <atomic>

// 经典无锁栈节点
struct Node { int data; Node* next; };

// 全局无锁栈顶（仅指针，无标签）
std::atomic<Node*> top{nullptr};

// 无保护的 pop：A->B->A 会让 CAS 误判成功
Node* pop_unsafe() {
    Node* old = top.load(std::memory_order_acquire);
    while (old) {
        Node* nxt = old->next;
        if (top.compare_exchange_strong(old, nxt,
                                        std::memory_order_acq_rel,
                                        std::memory_order_acquire))
            return old;
    }
    return nullptr;
}
