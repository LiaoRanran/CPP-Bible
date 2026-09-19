// 真实基准 D5 — ch159 线程池（GCC 15.3.0, -pthread）
// 维度：① 串行 vs 每任务新建 std::thread vs 固定线程池 vs std::async
//       ② 任务粒度扫描（任务数变化，观察池化收益如何随粒度放大）
// 防 DCE：结果累加到 volatile g_sink；并交叉校验 pool.sum == serial.sum（语义正确性）。
#include <algorithm>
#include <atomic>
#include <chrono>
#include <condition_variable>
#include <cstdio>
#include <cassert>
#include <functional>
#include <future>
#include <mutex>
#include <queue>
#include <thread>
#include <vector>

static volatile long g_sink = 0;

long work(long n) {
    long s = 0;
    for (long i = 0; i < n; ++i) s += i * ((i % 7) + 1);
    g_sink += s;
    return s;
}

// ---- 与 ch159 §17 同构的固定线程池（此处用于基准）----
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
            task();
        }
    }
public:
    explicit ThreadPool(std::size_t n = std::thread::hardware_concurrency()) {
        if (n == 0) n = 1;
        for (std::size_t i = 0; i < n; ++i)
            workers_.emplace_back([this] { worker(); });
    }
    ~ThreadPool() {
        stop_.store(true); cv_.notify_all();
        for (auto& w : workers_) if (w.joinable()) w.join();
    }
    template <class F, class... Args>
    auto submit(F&& f, Args&&... args) -> std::future<std::invoke_result_t<F, Args...>> {
        using R = std::invoke_result_t<F, Args...>;
        auto pt = std::make_shared<std::packaged_task<R()>>(
            std::bind(std::forward<F>(f), std::forward<Args>(args)...));
        auto fut = pt->get_future();
        { std::unique_lock<std::mutex> lk(mtx_); tasks_.emplace([pt] { (*pt)(); }); }
        cv_.notify_one();
        return fut;
    }
};

struct Result { double ms; long sum; };

Result measure_serial(long NTASKS, long WORK) {
    auto t0 = std::chrono::steady_clock::now();
    long sum = 0;
    for (long i = 0; i < NTASKS; ++i) sum += work(WORK);
    auto t1 = std::chrono::steady_clock::now();
    return { std::chrono::duration<double, std::milli>(t1 - t0).count(), sum };
}
Result measure_per_task(long NTASKS, long WORK) {
    auto t0 = std::chrono::steady_clock::now();
    std::vector<std::thread> ts; ts.reserve((std::size_t)NTASKS);
    std::vector<long> local((std::size_t)NTASKS, 0);
    for (long i = 0; i < NTASKS; ++i)
        ts.emplace_back([&, i] { local[(std::size_t)i] = work(WORK); });
    for (auto& t : ts) t.join();
    long sum = 0; for (long v : local) sum += v;
    auto t1 = std::chrono::steady_clock::now();
    return { std::chrono::duration<double, std::milli>(t1 - t0).count(), sum };
}
Result measure_pool(long NTASKS, long WORK) {
    const unsigned n = std::thread::hardware_concurrency();
    if (n == 0) return {0,0};
    ThreadPool pool(n);
    auto t0 = std::chrono::steady_clock::now();
    std::vector<std::future<long>> futs; futs.reserve((std::size_t)NTASKS);
    for (long i = 0; i < NTASKS; ++i) futs.push_back(pool.submit(work, WORK));
    long sum = 0; for (auto& f : futs) sum += f.get();
    auto t1 = std::chrono::steady_clock::now();
    return { std::chrono::duration<double, std::milli>(t1 - t0).count(), sum };
}
Result measure_async(long NTASKS, long WORK) {
    auto t0 = std::chrono::steady_clock::now();
    std::vector<std::future<long>> futs; futs.reserve((std::size_t)NTASKS);
    for (long i = 0; i < NTASKS; ++i)
        futs.push_back(std::async(std::launch::async, work, WORK));
    long sum = 0; for (auto& f : futs) sum += f.get();
    auto t1 = std::chrono::steady_clock::now();
    return { std::chrono::duration<double, std::milli>(t1 - t0).count(), sum };
}

int main() {
    const long NTASKS = 2000, WORK = 120000;
    const int ROUNDS = 5;
    std::vector<double> s_ser, s_per, s_pool, s_async;
    long sumSer = 0, sumPool = 0;

    for (int t = 0; t < ROUNDS; ++t) {
        auto a = measure_serial(NTASKS, WORK);   s_ser.push_back(a.ms);
        auto b = measure_per_task(NTASKS, WORK);  s_per.push_back(b.ms);
        auto c = measure_pool(NTASKS, WORK);      s_pool.push_back(c.ms);
        auto d = measure_async(NTASKS, WORK);     s_async.push_back(d.ms);
        if (t == 0) { sumSer = a.sum; sumPool = c.sum; }
    }
    auto median = [](std::vector<double> v) {
        std::sort(v.begin(), v.end()); return v[v.size()/2];
    };
    double mser = median(s_ser), mper = median(s_per),
           mpool = median(s_pool), masync = median(s_async);

    std::printf("hardware_concurrency = %u\n", std::thread::hardware_concurrency());
    std::printf("serial : %.3f ms  (median of %d)\n", mser, ROUNDS);
    std::printf("per-task: %.3f ms  speedup=%.2fx\n", mper, mser / mper);
    std::printf("pool    : %.3f ms  speedup=%.2fx\n", mpool, mser / mpool);
    std::printf("async   : %.3f ms  speedup=%.2fx\n", masync, mser / masync);
    std::printf("correctness: pool.sum == serial.sum ? %s\n",
                (sumPool == sumSer) ? "YES" : "NO");

    // ---- 维度②：任务粒度扫描（固定总工作量，观察池化 vs 每任务线程 的加速比变化）----
    std::printf("\n[granularity sweep: fixed WORK=%ld, vary NTASKS]\n", WORK);
    for (long nt : { (long)500, (long)2000, (long)8000 }) {
        std::vector<double> ps, pp;
        long ss = 0, sp = 0;
        for (int t = 0; t < ROUNDS; ++t) {
            auto x = measure_serial(nt, WORK);  ps.push_back(x.ms);
            auto y = measure_pool(nt, WORK);     pp.push_back(y.ms);
            if (t == 0) { ss = x.sum; sp = y.sum; }
        }
        double ms = median(ps), mp = median(pp);
        std::printf("NTASKS=%-5ld serial=%.1f pool=%.1f speedup=%.2fx correct=%s\n",
                    nt, ms, mp, ms / mp, (ss == sp) ? "YES" : "NO");
    }
    return 0;
}
