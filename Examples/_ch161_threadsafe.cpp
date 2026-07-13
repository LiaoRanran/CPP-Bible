// 文件：Examples/_ch161_threadsafe.cpp
// 取证：g++ -std=c++20 -O2 -pthread 真实编译运行（本机）
#include <atomic>
#include <iostream>
#include <thread>
#include <vector>

// ⑧ 线程安全：用 std::atomic 做无锁计数器，对比 mutex 保护的版本
struct AtomicCounter {
    std::atomic<long long> v{0};
    void inc() { v.fetch_add(1, std::memory_order_relaxed); }
    long long get() const { return v.load(); }
};

int main() {
    AtomicCounter c;
    std::vector<std::thread> ts;
    for (int t = 0; t < 8; ++t)
        ts.emplace_back([&c] { for (int i = 0; i < 100'000; ++i) c.inc(); });
    for (auto& t : ts) t.join();
    std::cout << "atomic counter = " << c.get() << " (期望 800000)\n";
    return 0;
}
