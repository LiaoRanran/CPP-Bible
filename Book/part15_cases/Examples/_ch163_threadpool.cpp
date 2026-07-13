// _ch163_threadpool.cpp  [Windows Winsock2]
// 编译: g++ -std=c++23 -O2 _ch163_threadpool.cpp -lws2_32 -o _ch163_threadpool.exe -pthread
// 作用: 最小线程池 + acceptor，演示 ⑨ 关联 第159章 线程池思想（内联实现，无外部依赖）。
#include <winsock2.h>
#include <ws2tcpip.h>
#include <iostream>
#include <thread>
#include <vector>
#include <queue>
#include <mutex>
#include <functional>
#include <cstring>

class ThreadPool {
    std::vector<std::thread> workers;
    std::queue<std::function<void()>> tasks;
    std::mutex mtx;
    bool stop = false;
public:
    explicit ThreadPool(size_t n) {
        for (size_t i = 0; i < n; ++i)
            workers.emplace_back([this] {
                for (;;) {
                    std::function<void()> job;
                    {
                        std::unique_lock<std::mutex> lk(mtx);
                        if (stop) return;
                        if (tasks.empty()) { continue; }
                        job = std::move(tasks.front());
                        tasks.pop();
                    }
                    job();
                }
            });
    }
    void submit(std::function<void()> f) {
        std::lock_guard<std::mutex> lk(mtx);
        tasks.push(std::move(f));
    }
    ~ThreadPool() {
        { std::lock_guard<std::mutex> lk(mtx); stop = true; }
        for (auto& w : workers) w.join();
    }
};

int main() {
    WSADATA wsa{};
    WSAStartup(MAKEWORD(2, 2), &wsa);
    ThreadPool pool(4);
    std::cout << "[pool] 线程池(4 工作线程) 已就绪\n";
    for (int i = 0; i < 3; ++i) {
        pool.submit([i] {
            std::cout << "[pool] 任务 " << i << " 在 "
                      << std::this_thread::get_id() << " 执行\n" << std::flush;
        });
    }
    std::this_thread::sleep_for(std::chrono::milliseconds(50));
    closesocket(INVALID_SOCKET);
    WSACleanup();
    return 0;
}
