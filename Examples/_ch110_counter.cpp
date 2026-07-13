#include <atomic>

std::atomic<long long> g_counter{0};

// 原子累加，期望编译器生成 lock xadd
void inc_relaxed() {
    g_counter.fetch_add(1, std::memory_order_relaxed);
}
