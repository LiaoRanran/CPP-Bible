// 文件：Examples/_ch161_async.cpp
// 取证：g++ -std=c++20 -O2 真实编译运行（本机）；后台线程 + 队列实现异步日志
#include <atomic>
#include <chrono>
#include <condition_variable>
#include <iostream>
#include <mutex>
#include <queue>
#include <string>
#include <thread>
#include <vector>

// ⑥ 异步日志：生产者（业务线程）只把消息推入队列，消费者（后台线程）负责落地
struct AsyncLogger {
    std::queue<std::string> q;
    std::mutex m;
    std::condition_variable cv;
    std::atomic<bool> stop{false};
    std::thread worker;

    AsyncLogger() {
        worker = std::thread([this] {
            while (true) {
                std::unique_lock<std::mutex> lk(m);
                cv.wait(lk, [this] { return stop.load() || !q.empty(); });
                while (!q.empty()) {
                    std::cout << q.front() << std::endl;  // 落地（这里用 console 代替文件）
                    q.pop();
                }
                if (stop.load() && q.empty()) break;
            }
        });
    }
    void push(std::string msg) {
        {
            std::lock_guard<std::mutex> lk(m);
            q.push(std::move(msg));
        }
        cv.notify_one();
    }
    ~AsyncLogger() {
        stop.store(true);
        cv.notify_one();
        if (worker.joinable()) worker.join();
    }
};

int main() {
    AsyncLogger log;
    for (int i = 0; i < 5; ++i)
        log.push("async msg #" + std::to_string(i));
    std::this_thread::sleep_for(std::chrono::milliseconds(50));  // 等后台线程消费完
    return 0;
}
