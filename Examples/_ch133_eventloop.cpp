// _ch133_eventloop.cpp
// Redis 风格单线程 Reactor（ae.c 等价）：一个就绪事件队列 + 单线程分发回调
// 编译：g++ -std=c++20 -O2 -S -masm=intel _ch133_eventloop.cpp -o Examples/_ch133_eventloop.asm
#include <cstddef>

struct FileEvent { int fd; void (*cb)(int fd, void* data); void* data; };

// aeProcessEvents 的单线程等价：遍历就绪集合，逐个回调（无锁、无线程切换）
void process_events(FileEvent* fired, std::size_t count) {
    for (std::size_t i = 0; i < count; ++i) {
        FileEvent& e = fired[i];
        if (e.cb) e.cb(e.fd, e.data);   // 事件循环中唯一的「多路分发」点
    }
}

// beforeSleep / 单次 tick：Redis 主线程每轮只做一件事——清空就绪队列
int main() {
    static FileEvent ev[4];
    ev[0] = {1, nullptr, nullptr};
    return (int)(ev[0].fd);
    (void)process_events;
}
