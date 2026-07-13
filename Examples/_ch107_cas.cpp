#include <atomic>

std::atomic<int> g{0};

bool try_set(int expected, int desired) {
    int e = expected;
    return g.compare_exchange_strong(e, desired, std::memory_order_acq_rel);
}
