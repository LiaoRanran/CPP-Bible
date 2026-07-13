#include <atomic>

// Dekker 算法：需要 seq_cst 全局总序才能正确互斥
std::atomic<int> flag0{0}, flag1{0};
std::atomic<int> turn{0};

void thread_a() {
    flag0.store(1, std::memory_order_seq_cst);
    if (flag1.load(std::memory_order_seq_cst) == 0) {
        // 进入临界区
    }
}

void thread_b() {
    flag1.store(1, std::memory_order_seq_cst);
    if (flag0.load(std::memory_order_seq_cst) == 0) {
        // 进入临界区
    }
}
