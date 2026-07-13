#include <atomic>

volatile int v = 0;
std::atomic<int> a{0};

void volatile_inc() { v++; }

void atomic_inc() { a.fetch_add(1, std::memory_order_relaxed); }
