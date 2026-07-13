#include <atomic>

std::atomic<int> g{0};

// release 存储 + acquire 加载（发布-订阅模式）
void publish(int v) {
    g.store(v, std::memory_order_release);
}

int consume() {
    return g.load(std::memory_order_acquire);
}
