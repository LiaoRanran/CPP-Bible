#include <atomic>

std::atomic_flag f = ATOMIC_FLAG_INIT;

void acquire() {
    while (f.test_and_set(std::memory_order_acquire)) { }
}

void release() {
    f.clear(std::memory_order_release);
}
