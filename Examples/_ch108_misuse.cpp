#include <atomic>
#include <cstdio>
#include <thread>

// 错误示例：用 relaxed 保护“数据已就绪”标志，导致消费者读到未初始化数据
std::atomic<bool> ready{false};
int payload = 0;

void producer() {
    payload = 42;                                  // ① 写数据
    ready.store(true, std::memory_order_relaxed);  // ② relaxed 标志（错误！不建立同步）
}

void consumer() {
    while (!ready.load(std::memory_order_relaxed)) { // ③ 自旋等待
        ;
    }
    std::printf("%d\n", payload);                  // ④ 可能读到 0（数据写未被同步）
}

int main() {
    std::thread t1(producer);
    std::thread t2(consumer);
    t1.join();
    t2.join();
    return 0;
}
