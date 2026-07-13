// 文件：Examples/_ch160_cacheline.cpp
// 行号：1
// 缓存行对齐与 false sharing：两个被不同线程频繁写的计数器
#include <cstddef>
#include <cstdio>
#include <thread>
#include <chrono>
#include <atomic>

struct Packed {            // 两个计数器在同一缓存行 -> false sharing
    std::atomic<int> a{0};
    std::atomic<int> b{0};   // a 与 b 共享 64 字节缓存行
};

struct Padded {            // [经验] 各自独占缓存行
    alignas(64) std::atomic<int> a{0};
    alignas(64) std::atomic<int> b{0};
};

template <class T>
double run(const char* name) {
    T s;
    auto work = [&](std::atomic<int> T::*m) {
        for (int i = 0; i < 50000000; ++i) (s.*m).fetch_add(1, std::memory_order_relaxed);
    };
    auto t0 = std::chrono::high_resolution_clock::now();
    std::thread t1(work, &T::a);
    std::thread t2(work, &T::b);
    t1.join(); t2.join();
    auto t1t = std::chrono::high_resolution_clock::now();
    double ms = std::chrono::duration<double, std::milli>(t1t - t0).count();
    std::printf("%-10s: %.1f ms (a=%d b=%d)\n", name, ms,
                s.a.load(), s.b.load());
    return ms;
}

int main() {
    run<Packed>("Packed");
    run<Padded>("Padded");
    return 0;
}
