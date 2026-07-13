#include <atomic>

std::atomic<bool> locked{false};

void lock() {
    bool expected = false;
    while (!locked.compare_exchange_weak(expected, true,
             std::memory_order_acquire, std::memory_order_relaxed)) {
        expected = false;
    }
}

void unlock() { locked.store(false, std::memory_order_release); }
