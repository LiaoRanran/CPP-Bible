// _ch165_threadpool.cpp : 极简线程池片段（从零项目骨架，见第159章 线程池）
#include <condition_variable>
#include <functional>
#include <mutex>
#include <queue>
#include <thread>
#include <vector>
#include <iostream>

class ThreadPool {
    std::vector<std::thread> workers;
    std::queue<std::function<void()>> tasks;
    std::mutex mtx;
    std::condition_variable cv;
    bool stop = false;
public:
    ThreadPool(size_t n) {
        for (size_t i = 0; i < n; ++i)
            workers.emplace_back([this] {
                for (;;) {
                    std::function<void()> t;
                    {
                        std::unique_lock<std::mutex> lk(mtx);
                        cv.wait(lk, [this] { return stop || !tasks.empty(); });
                        if (stop && tasks.empty()) return;
                        t = std::move(tasks.front()); tasks.pop();
                    }
                    t();
                }
            });
    }
    void submit(std::function<void()> f) {
        { std::lock_guard<std::mutex> lk(mtx); tasks.push(std::move(f)); }
        cv.notify_one();
    }
    ~ThreadPool() {
        { std::lock_guard<std::mutex> lk(mtx); stop = true; }
        cv.notify_all();
        for (auto& w : workers) w.join();
    }
};

int main() {
    ThreadPool pool(4);
    for (int i = 0; i < 8; ++i) pool.submit([i] { std::cout << "job " << i << "\n"; });
    return 0;   // 析构时等待全部完成
}
