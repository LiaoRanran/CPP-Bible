// ch93 thread_async 汇编实证 —— std::thread 的真实 syscall 成本
#include <thread>
#include <atomic>
#include <mutex>

// 观测 1: 创建线程的真实指令
std::thread* make_thread() {
    return new std::thread([]{
        volatile int x = 0;
        for (int i = 0; i < 100; ++i) x += i;
    });
}

// 观测 2: std::mutex lock/unlock 真实指令
std::mutex mtx;
void lock_work(int& counter) {
    std::lock_guard<std::mutex> lk(mtx);              // lock vs 无锁对比
    ++counter;
}

// 观测 3: std::atomic 无锁递增
std::atomic<int> atomic_counter{0};
void atomic_inc() {
    atomic_counter.fetch_add(1, std::memory_order_relaxed);  // x86: lock xadd
}

// 观测 4: 主线程 join 成本
void join_thread(std::thread& t) {
    t.join();                                         // → pthread_join → wait4 syscall
}

// 观测 5: async future 成本
#include <future>
int compute_value() { return 42; }
int use_async() {
    auto fut = std::async(std::launch::async, compute_value);
    return fut.get();                                 // 隐式同步
}

// 观测 6: thread_local 变量访问
thread_local int tl_var = 0;
int read_tl() { return tl_var; }                      // → __tls_get_addr
