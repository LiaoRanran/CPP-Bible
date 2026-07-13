// _ch165_memory.cpp : 内存模型/对齐/placement new 练习（高级）
#include <atomic>
#include <cstddef>
#include <iostream>
#include <new>

struct Align16 { alignas(16) int x; char pad[12]; };

int main() {
    std::cout << "alignof(Align16) = " << alignof(Align16) << "\n";   // 16
    std::cout << "sizeof(Align16)  = " << sizeof(Align16) << "\n";    // 16

    // placement new：在已有缓冲区构造对象
    alignas(int) char buf[sizeof(int)];
    int* p = new (buf) int(99);
    std::cout << "*p = " << *p << "\n";   // 99
    // 标量类型无需手动析构；若放置的是类对象，须显式调用 p->~T();

    // 内存序初探（acquire/release 配对）
    int data = 0;
    std::atomic<bool> ready{false};
    // 生产线程: data = 1; ready.store(true, std::memory_order_release);
    // 消费线程: if (ready.load(std::memory_order_acquire)) use(data);
    (void)data; (void)ready;
    return 0;
}
