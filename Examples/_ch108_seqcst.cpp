#include <atomic>

std::atomic<int> x{0};

// seq_cst 存储 + 加载
void writer() {
    x.store(1, std::memory_order_seq_cst);
}

int reader() {
    return x.load(std::memory_order_seq_cst);
}
