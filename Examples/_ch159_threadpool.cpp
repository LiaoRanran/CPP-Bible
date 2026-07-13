// 文件：Examples/_ch159_threadpool.cpp
// 行号：1
// 编译：C:/Qt/Tools/mingw1310_64/bin/g++.exe -std=c++23 -O2 Examples/_ch159_threadpool.cpp -o Examples/_ch159_threadpool.exe
// 运行：Examples/_ch159_threadpool.exe
// 说明：自包含工业级线程池，含 RAII 析构 join、packaged_task 异常传播、真实基准。
#include <atomic>
#include <chrono>
#include <condition_variable>
#include <cstdio>
#include <functional>
#include <future>
#include <iostream>
#include <mutex>
#include <queue>
#include <stdexcept>
#include <thread>
#include <vector>

class ThreadPool {
    std::vector<std::thread> workers_;
    std::queue<std::function<void()>> tasks_;
    std::mutex mtx_;
    std::condition_variable cv_;
    std::atomic<bool> stop_{false};

    void worker() {
        for (;;) {
            std::function<void()> task;
            {
                std::unique_lock<std::mutex> lk(mtx_);
                cv_.wait(lk, [this] { return stop_.load() || !tasks_.empty(); });
                if (stop_.load() && tasks_.empty()) return;
                task = std::move(tasks_.front());
                tasks_.pop();
            }
            task();  // 异常在 packaged_task 内被捕获并存入 future
        }
    }

public:
    explicit ThreadPool(std::size_t n = std::thread::hardware_concurrency()) {
        if (n == 0) n = 1;
        for (std::size_t i = 0; i < n; ++i)
            workers_.emplace_back([this] { worker(); });
    }

    ~ThreadPool() {
        stop_.store(true);
        cv_.notify_all();
        for (auto& w : workers_)
            if (w.joinable()) w.join();
    }

    ThreadPool(const ThreadPool&) = delete;
    ThreadPool& operator=(const ThreadPool&) = delete;

    template <class F, class... Args>
    auto submit(F&& f, Args&&... args)
        -> std::future<std::invoke_result_t<F, Args...>> {
        using R = std::invoke_result_t<F, Args...>;
        auto pt = std::make_shared<std::packaged_task<R()>>(
            std::bind(std::forward<F>(f), std::forward<Args>(args)...));
        auto fut = pt->get_future();
        {
            std::unique_lock<std::mutex> lk(mtx_);
            if (stop_.load()) throw std::runtime_error("submit on stopped pool");
            tasks_.emplace([pt] { (*pt)(); });
        }
        cv_.notify_one();
        return fut;
    }
};

static volatile long g_sink = 0;  // 防 DCE（dead code elimination）
long work(long n) {
    long s = 0;
    for (long i = 0; i < n; ++i) s += i * ((i % 7) + 1);
    g_sink += s;
    return s;
}

int main() {
    const long NTASKS = 2000;
    const long WORK = 120000;
    const unsigned nthreads = std::thread::hardware_concurrency();

    auto t0 = std::chrono::steady_clock::now();
    long serialSum = 0;
    for (long i = 0; i < NTASKS; ++i) serialSum += work(WORK);
    auto t1 = std::chrono::steady_clock::now();
    double serialMs = std::chrono::duration<double, std::milli>(t1 - t0).count();

    ThreadPool pool(nthreads);
    auto t2 = std::chrono::steady_clock::now();
    std::vector<std::future<long>> futs;
    futs.reserve(static_cast<std::size_t>(NTASKS));
    for (long i = 0; i < NTASKS; ++i) futs.push_back(pool.submit(work, WORK));
    long poolSum = 0;
    for (auto& f : futs) poolSum += f.get();
    auto t3 = std::chrono::steady_clock::now();
    double poolMs = std::chrono::duration<double, std::milli>(t3 - t2).count();

    std::printf("hardware_concurrency = %u\n", nthreads);
    std::printf("serial : %.3f ms  sum=%ld\n", serialMs, serialSum);
    std::printf("pool   : %.3f ms  sum=%ld\n", poolMs, poolSum);
    std::printf("speedup: %.2fx\n", serialMs / poolMs);
    std::printf("g_sink = %ld\n", (long)g_sink);
    return 0;
}
