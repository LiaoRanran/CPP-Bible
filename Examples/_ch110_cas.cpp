#include <atomic>

struct Node { int val; Node* next; };
std::atomic<Node*> head{nullptr};

// CAS 循环：标准无锁 push，期望编译器生成 lock cmpxchg
void push(int v) {
    Node* n = new Node{v, nullptr};
    Node* old = head.load(std::memory_order_relaxed);
    do {
        n->next = old;
    } while (!head.compare_exchange_weak(old, n,
                std::memory_order_release,
                std::memory_order_relaxed));
}
