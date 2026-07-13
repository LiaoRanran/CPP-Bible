// 文件：Examples/_ch161_benchmark.cpp
// 取证：g++ -std=c++20 -O2 -pthread 真实编译运行（本机）；std::chrono 真实基准
// ⑯ 性能测量：同步日志 vs 异步日志，1,000,000 条消息真实耗时对比
#include <atomic>
#include <chrono>
#include <cstdio>
#include <mutex>
#include <queue>
#include <string>
#include <thread>

static std::mutex g_mtx;
static std::queue<std::string> g_q;
static std::atomic<bool> g_stop{false};
static std::thread g_worker;

// 异步消费者：后台线程持续取出（模拟落地），与生产者并发
void start_consumer() {
    g_worker = std::thread([] {
        while (true) {
            std::unique_lock<std::mutex> lk(g_mtx);
            while (!g_q.empty()) g_q.pop();   // 取出即丢弃（仅测生产者吞吐）
            lk.unlock();
            if (g_stop.load()) break;
        }
    });
}

int main() {
    const int N = 1'000'000;

    // 同步：每条消息生产者自己加锁并"落地"（这里用 pop 模拟写入完成）
    auto t0 = std::chrono::steady_clock::now();
    for (int i = 0; i < N; ++i) {
        std::lock_guard<std::mutex> lk(g_mtx);
        g_q.push("x");
        g_q.pop();   // 同步：必须等本次写入完成才返回
    }
    auto t1 = std::chrono::steady_clock::now();
    double sync_ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
    std::printf("sync  : %d msgs in %.1f ms (%.2f Mmsg/s)\n",
                N, sync_ms, N / sync_ms / 1000.0);

    // 异步：启动后台消费者，生产者仅 push 后立即返回
    g_q = std::queue<std::string>{};
    start_consumer();
    auto t2 = std::chrono::steady_clock::now();
    for (int i = 0; i < N; ++i) {
        std::lock_guard<std::mutex> lk(g_mtx);
        g_q.push("x");   // 异步：入队即返回，落地由后台线程负责
    }
    auto t3 = std::chrono::steady_clock::now();
    double async_ms = std::chrono::duration<double, std::milli>(t3 - t2).count();
    g_stop = true;
    if (g_worker.joinable()) g_worker.join();
    std::printf("async : %d msgs in %.1f ms (%.2f Mmsg/s)\n",
                N, async_ms, N / async_ms / 1000.0);
    std::printf("speedup (producer) = %.2fx\n", sync_ms / async_ms);
    return 0;
}
