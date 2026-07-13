// 文件：Examples/_ch161_fix5.cpp
// 主题：⑥ 异步队列实现 —— 有界阻塞队列（生产者满则等，消费者空则等）
#include <condition_variable>
#include <cstdio>
#include <mutex>
#include <queue>
#include <string>
#include <thread>

class BoundedQueue {
    std::queue<std::string> q;
    mutable std::mutex m;
    std::condition_variable cv_full, cv_empty;
    std::size_t cap;
public:
    explicit BoundedQueue(std::size_t c) : cap(c) {}
    void push(std::string s) {
        std::unique_lock lk(m);
        cv_full.wait(lk, [&] { return q.size() < cap; });
        q.push(std::move(s));
        cv_empty.notify_one();
    }
    std::string pop() {
        std::unique_lock lk(m);
        cv_empty.wait(lk, [&] { return !q.empty(); });
        auto s = std::move(q.front()); q.pop();
        cv_full.notify_one();
        return s;
    }
};

int main() {
    BoundedQueue q(2);
    std::thread prod([&] { for (int i = 0; i < 4; ++i) q.push("msg" + std::to_string(i)); });
    std::thread cons([&] { for (int i = 0; i < 4; ++i) std::printf("got %s\n", q.pop().c_str()); });
    prod.join(); cons.join();
    return 0;
}
