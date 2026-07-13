// ⑧ 伪共享结构体：a、b 紧挨着，落在同一 64B 行
#include <iostream>
#include <thread>
#include <atomic>
#include <chrono>
#include <cstdint>

struct SharedBad {
    std::atomic<std::uint64_t> a{0};
    std::atomic<std::uint64_t> b{0};              // 与 a 同 cache line → 伪共享
};

int main() {
    SharedBad s;
    constexpr std::uint64_t IT = 20'000'000;
    auto t0 = std::chrono::steady_clock::now();
    std::thread t1([&] { for (std::uint64_t i = 0; i < IT; ++i) s.a.fetch_add(1, std::memory_order_relaxed); });
    std::thread t2([&] { for (std::uint64_t i = 0; i < IT; ++i) s.b.fetch_add(1, std::memory_order_relaxed); });
    t1.join(); t2.join();
    auto t1_ = std::chrono::steady_clock::now();
    std::cout << "false-sharing bad = "
              << std::chrono::duration<double, std::milli>(t1_ - t0).count() << " ms\n";
    return 0;
}