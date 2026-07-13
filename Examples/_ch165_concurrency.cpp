// _ch165_concurrency.cpp : 线程/互斥/原子 练习（高级）
#include <atomic>
#include <iostream>
#include <mutex>
#include <thread>
#include <vector>

int main() {
    // 1) 互斥量保护共享变量
    int counter = 0;
    std::mutex mtx;
    auto worker = [&]() {
        for (int i = 0; i < 1000; ++i) {
            std::lock_guard<std::mutex> lk(mtx);
            ++counter;
        }
    };
    std::thread t1(worker), t2(worker);
    t1.join(); t2.join();
    std::cout << "mutex counter = " << counter << "\n";  // 2000

    // 2) 原子变量，无锁
    std::atomic<int> ac{0};
    auto aworker = [&]() { for (int i = 0; i < 1000; ++i) ++ac; };
    std::thread a1(aworker), a2(aworker);
    a1.join(); a2.join();
    std::cout << "atomic counter = " << ac.load() << "\n";  // 2000
    return 0;
}
