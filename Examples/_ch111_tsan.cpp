#include <atomic>
#include <thread>

// 一个故意存在 ABA 隐患的无锁计数器（ThreadSanitizer 可辅助发现数据竞争）
struct Node { int val; Node* next; };
std::atomic<Node*> head{nullptr};

void reader() {
    Node* h = head.load(std::memory_order_relaxed);  // ❌ relaxed 在回收场景危险
    if (h) (void)h->val;
}

void writer() {
    Node n{42, nullptr};
    n.next = head.load(std::memory_order_relaxed);
    head.store(&n, std::memory_order_relaxed);        // 临时对象，危险！
}
