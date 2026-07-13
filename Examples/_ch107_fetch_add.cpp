#include <atomic>

std::atomic<int> g{0};

void add_one() {
    g.fetch_add(1, std::memory_order_relaxed);
}

int read() {
    return g.load(std::memory_order_relaxed);
}
