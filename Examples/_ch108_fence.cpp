#include <atomic>

std::atomic<int> flag{0};
int data = 0;

// 用 thread fence 建立 happens-before
void producer() {
    data = 42;
    std::atomic_thread_fence(std::memory_order_release);
    flag.store(1, std::memory_order_relaxed);
}

void consumer() {
    if (flag.load(std::memory_order_relaxed)) {
        std::atomic_thread_fence(std::memory_order_acquire);
        (void)data;
    }
}
