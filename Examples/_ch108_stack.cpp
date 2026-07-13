#include <atomic>
#include <cstdio>

struct Node {
    int value;
    Node* next;
};

std::atomic<Node*> head{nullptr};

void push(int v) {
    Node* n = new Node{v, nullptr};
    n->next = head.load(std::memory_order_relaxed);
    while (!head.compare_exchange_weak(n->next, n,
            std::memory_order_release,
            std::memory_order_relaxed)) {
        ;
    }
}

bool pop(int& out) {
    Node* old = head.load(std::memory_order_acquire);
    while (old && !head.compare_exchange_weak(old, old->next,
            std::memory_order_acquire,
            std::memory_order_relaxed)) {
        ;
    }
    if (!old) return false;
    out = old->value;
    delete old;
    return true;
}

int main() {
    push(10);
    push(20);
    int a = 0, b = 0;
    pop(a);
    pop(b);
    std::printf("%d %d\n", a, b);
    return 0;
}
