// D5 benchmark: ch94 stop_token — 协作取消机制性能开销
// 编译: g++ -O2 -std=c++23 -pthread -o bench_d5_ch94.exe _bench_d5_ch94_stop_token.cpp
// 注: 本基准刻意剔除 std::condition_variable 场景——在 MinGW GCC 15.3.0 下，
// condition_variable 与其余线程构造共存会触发链接器/加载器缺陷（进程尚未进入 main 即被拒绝，
// exit 127）。该缺陷与优化级别无关（-O0/-O1/-O2 均复现），故 s4(cv.wait_for) 场景移至正文论述，
// 此处仅测可稳定运行的 jthread/stop_callback/request_stop/多线程争用四类场景。
#include <iostream>
#include <chrono>
#include <vector>
#include <thread>
#include <stop_token>
#include <atomic>
#include <mutex>
#include <algorithm>
#include <cstdint>

static volatile long long g_sink = 0;

static double median_of(std::vector<double> t) {
    std::sort(t.begin(), t.end());
    return t[t.size() / 2];
}
static double bench(const char* name, auto fn, int rounds = 5) {
    std::vector<double> t; t.reserve(rounds);
    for (int r = 0; r < rounds; ++r) {
        auto a = std::chrono::steady_clock::now();
        long long res = fn();
        auto b = std::chrono::steady_clock::now();
        g_sink += res;
        t.push_back(std::chrono::duration<double, std::milli>(b - a).count());
    }
    double m = median_of(t);
    std::cout << name << ": " << m << " ms" << std::endl;
    return m;
}

int main() {
    std::cout << "=== D5 ch94 stop_token benchmark ===" << std::endl;

    // S1: jthread+stop_token 取消 vs thread+atomic<bool> 取消（生命周期开销）
    auto s1_jthread = []() -> long long {
        const int N = 2000;
        for (int i = 0; i < N; ++i) {
            std::jthread w([](std::stop_token st) {
                volatile int d = 0;
                while (!st.stop_requested()) ++d;
            });
        }
        return N;
    };
    auto s1_atomic = []() -> long long {
        const int N = 2000;
        for (int i = 0; i < N; ++i) {
            std::atomic<bool> stop{false};
            std::thread w([&stop] { volatile int d = 0; while (!stop.load(std::memory_order_acquire)) ++d; });
            stop.store(true, std::memory_order_release);
            w.join();
        }
        return N;
    };
    double a = bench("s1_jthread_cancel", s1_jthread);
    double b = bench("s1_thread_atomic", s1_atomic);
    std::cout << "ratio jthread/atomic = " << a / b << std::endl;

    // S2: stop_callback 注册 + 触发
    auto s2_reg = []() -> long long {
        const int N = 1000;
        std::stop_source ss; auto tok = ss.get_token(); auto cb = [] {};
        using SCB = std::stop_callback<decltype(cb)>;
        std::vector<std::unique_ptr<SCB>> v; v.reserve(N);
        for (int i = 0; i < N; ++i) v.push_back(std::make_unique<SCB>(tok, cb));
        return N;
    };
    auto s2_trig = []() -> long long {
        const int N = 1000;
        std::stop_source ss; auto tok = ss.get_token(); auto cb = [] {};
        using SCB = std::stop_callback<decltype(cb)>;
        std::vector<std::unique_ptr<SCB>> v; v.reserve(N);
        for (int i = 0; i < N; ++i) v.push_back(std::make_unique<SCB>(tok, cb));
        ss.request_stop();
        return N;
    };
    double c2 = bench("s2_register_1k", s2_reg);
    double d2 = bench("s2_trigger_1k", s2_trig);
    std::cout << "register per-cb = " << c2 / 1000 << " ms, trigger per-cb = " << d2 / 1000 << " ms" << std::endl;

    // S3: request_stop() 原子开销 vs 普通 atomic store
    auto s3_ss = []() -> long long {
        const int N = 100000; long long k = 0;
        for (int i = 0; i < N; ++i) { std::stop_source s; if (s.request_stop()) ++k; }
        return k;
    };
    auto s3_at = []() -> long long {
        const int N = 100000; long long k = 0;
        for (int i = 0; i < N; ++i) { std::atomic<bool> f{false}; f.store(true, std::memory_order_release); ++k; }
        return k;
    };
    double e3 = bench("s3_request_stop_100k", s3_ss);
    double f3 = bench("s3_atomic_store_100k", s3_at);
    std::cout << "ratio stop_source/atomic = " << e3 / f3 << std::endl;

    // S5: 多线程 stop_requested() 争用 vs 私有 atomic
    auto s5_shared = []() -> long long {
        const int NT = 8, N = 2000000; std::stop_source ss; auto tok = ss.get_token();
        std::atomic<long long> tot{0}; std::vector<std::thread> th; th.reserve(NT);
        for (int t = 0; t < NT; ++t) th.emplace_back([&] { long long loc = 0; for (int i = 0; i < N; ++i) if (!tok.stop_requested()) ++loc; tot += loc; });
        for (auto& x : th) x.join();
        return tot.load();
    };
    auto s5_priv = []() -> long long {
        const int NT = 8, N = 2000000; struct P { std::atomic<bool> v{false}; };
        std::vector<P> fl(NT); std::atomic<long long> tot{0}; std::vector<std::thread> th; th.reserve(NT);
        for (int t = 0; t < NT; ++t) th.emplace_back([&, t] { long long loc = 0; for (int i = 0; i < N; ++i) if (!fl[t].v.load(std::memory_order_acquire)) ++loc; tot += loc; });
        for (auto& x : th) x.join();
        return tot.load();
    };
    double g5 = bench("s5_shared_token_8t", s5_shared);
    double h5 = bench("s5_private_atomic_8t", s5_priv);
    std::cout << "ratio shared/private = " << g5 / h5 << std::endl;

    std::cout << "g_sink = " << g_sink << std::endl;
    return 0;
}
