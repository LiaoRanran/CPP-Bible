#include <atomic>
#include <cstdint>

struct Pair { std::uint64_t a; std::uint64_t b; };
std::atomic<Pair> g_pair{};

// 128 位（双字）CAS，期望编译器生成 lock cmpxchg16b（需 -mcx16）
void swap_dw(std::uint64_t a, std::uint64_t b) {
    Pair expected = g_pair.load(std::memory_order_relaxed);
    Pair desired{a, b};
    g_pair.compare_exchange_weak(expected, desired,
                                 std::memory_order_acq_rel,
                                 std::memory_order_relaxed);
}
