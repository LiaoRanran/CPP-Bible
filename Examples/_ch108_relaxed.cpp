#include <atomic>

std::atomic<int> c{0};

// relaxed 只保证原子性，不保证同步/顺序
void bump() {
    c.fetch_add(1, std::memory_order_relaxed);
}

int get() {
    return c.load(std::memory_order_relaxed);
}
