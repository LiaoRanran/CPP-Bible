// _bench_d5_41_sptr.cpp — ch41 D5: 智能指针分配/传递真实开销
// g++ -O2 -std=c++17
#include <algorithm>
#include <chrono>
#include <cstdio>
#include <memory>
#include <vector>

using Clock = std::chrono::steady_clock;
static double ms(Clock::time_point a, Clock::time_point b) {
    return std::chrono::duration<double, std::milli>(b - a).count();
}
template <class F> static double median5(F f) {
    std::vector<double> t;
    for (int i = 0; i < 5; ++i) t.push_back(f());
    std::sort(t.begin(), t.end());
    return t[2];
}
volatile long long g_sink = 0;
void* volatile g_escape = nullptr;  // 指针逃逸口：阻止 allocation elision

struct Node { long long payload[4]; };  // 32B 对象

int main() {
    const int N = 1'000'000;

    // ---- 0) 逃逸版分配对照（指针写入 volatile，new/delete 不可消除）----
    double e_raw = median5([&] {
        auto a = Clock::now();
        long long s = 0;
        for (int i = 0; i < N; ++i) {
            Node* p = new Node{{i, 0, 0, 0}};
            g_escape = p;                    // 逃逸
            s += p->payload[0];
            delete p;
        }
        g_sink = s;
        return ms(a, Clock::now());
    });
    double e_uni = median5([&] {
        auto a = Clock::now();
        long long s = 0;
        for (int i = 0; i < N; ++i) {
            auto p = std::make_unique<Node>(Node{{i, 0, 0, 0}});
            g_escape = p.get();              // 逃逸
            s += p->payload[0];
        }
        g_sink = s;
        return ms(a, Clock::now());
    });
    std::printf("alloc_1M_escape,raw_new,%.3f\n", e_raw);
    std::printf("alloc_1M_escape,make_unique,%.3f,ratio=%.2f\n", e_uni, e_uni / e_raw);

    // ---- 1) 分配+释放 1M 个 32B 对象 ----
    double t_raw = median5([&] {
        auto a = Clock::now();
        long long s = 0;
        for (int i = 0; i < N; ++i) {
            Node* p = new Node{{i, 0, 0, 0}};
            s += p->payload[0];
            delete p;
        }
        g_sink = s;
        return ms(a, Clock::now());
    });
    double t_uni = median5([&] {
        auto a = Clock::now();
        long long s = 0;
        for (int i = 0; i < N; ++i) {
            auto p = std::make_unique<Node>(Node{{i, 0, 0, 0}});
            s += p->payload[0];
        }
        g_sink = s;
        return ms(a, Clock::now());
    });
    double t_shn = median5([&] {
        auto a = Clock::now();
        long long s = 0;
        for (int i = 0; i < N; ++i) {
            std::shared_ptr<Node> p(new Node{{i, 0, 0, 0}});  // 两次堆分配
            s += p->payload[0];
        }
        g_sink = s;
        return ms(a, Clock::now());
    });
    double t_shm = median5([&] {
        auto a = Clock::now();
        long long s = 0;
        for (int i = 0; i < N; ++i) {
            auto p = std::make_shared<Node>(Node{{i, 0, 0, 0}});  // 单次合并分配
            s += p->payload[0];
        }
        g_sink = s;
        return ms(a, Clock::now());
    });
    std::printf("alloc_1M,raw_new,%.3f\n", t_raw);
    std::printf("alloc_1M,make_unique,%.3f,ratio=%.2f\n", t_uni, t_uni / t_raw);
    std::printf("alloc_1M,shared_new,%.3f,ratio=%.2f\n", t_shn, t_shn / t_raw);
    std::printf("alloc_1M,make_shared,%.3f,ratio=%.2f\n", t_shm, t_shm / t_raw);

    // ---- 2) 传递开销：拷贝 shared_ptr（lock inc/dec）vs 传引用 ----
    auto sp = std::make_shared<Node>(Node{{7, 0, 0, 0}});
    const int R = 50'000'000;
    double t_cp = median5([&] {
        auto a = Clock::now();
        long long s = 0;
        for (int i = 0; i < R; ++i) {
            std::shared_ptr<Node> c = sp;  // 原子 ++/--
            s += c->payload[0];
        }
        g_sink = s;
        return ms(a, Clock::now());
    });
    double t_rf = median5([&] {
        auto a = Clock::now();
        long long s = 0;
        const std::shared_ptr<Node>& r = sp;
        for (int i = 0; i < R; ++i) {
            s += r->payload[0];
            g_sink = s;  // 每轮写 volatile 防合并
        }
        return ms(a, Clock::now());
    });
    std::printf("pass_50M,copy_shared,%.3f\n", t_cp);
    std::printf("pass_50M,by_ref,%.3f,ratio=%.2f\n", t_rf, t_cp / t_rf);

    // ---- 3) weak_ptr::lock 的成本（CAS 循环）----
    std::weak_ptr<Node> wp = sp;
    const int W = 20'000'000;
    double t_wl = median5([&] {
        auto a = Clock::now();
        long long s = 0;
        for (int i = 0; i < W; ++i) {
            if (auto c = wp.lock()) s += c->payload[0];
        }
        g_sink = s;
        return ms(a, Clock::now());
    });
    std::printf("weak_lock_20M,lock,%.3f\n", t_wl);
    return 0;
}
