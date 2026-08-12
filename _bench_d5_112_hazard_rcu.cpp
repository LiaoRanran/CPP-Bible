// _bench_d5_112_hazard_rcu.cpp  — shared_ptr 引用计数 vs 裸指针 vs hazard pointer 槽 (GCC 15.3.0)
// 对比：裸指针拷贝(零开销) / hazard 槽原子存读 / shared_ptr 拷贝(控制块原子 RMW)
// 用随机数据 + 逃逸，防闭式求值把循环消成常量
#include <memory>
#include <atomic>
#include <iostream>
#include <vector>
#include <chrono>
#include <random>

static constexpr int N = 20'000'000;
volatile int64_t g_sink = 0;
void* volatile g_esc = nullptr;

__attribute__((noinline)) int64_t bench_raw() {
    std::vector<int> arr(64);
    std::mt19937 rng(3);
    for (int& x : arr) x = (int)rng();
    int* p = arr.data();
    int64_t s = 0;
    for (int i = 0; i < N; ++i) {
        int* q = p;            // 裸指针拷贝
        s += q[i & 63];
        g_esc = q;
    }
    return s;
}
__attribute__((noinline)) int64_t bench_hazard() {
    std::vector<int> arr(64);
    std::mt19937 rng(3);
    for (int& x : arr) x = (int)rng();
    int* p = arr.data();
    std::atomic<int*> hp{nullptr};
    int64_t s = 0;
    for (int i = 0; i < N; ++i) {
        hp.store(p, std::memory_order_seq_cst);  // 发布危险指针
        int* q = hp.load(std::memory_order_seq_cst);
        s += q[i & 63];
        g_esc = q;
    }
    return s;
}
__attribute__((noinline)) int64_t bench_shared_ptr() {
    auto sp = std::make_shared<std::vector<int>>(64);
    std::mt19937 rng(3);
    for (int& x : *sp) x = (int)rng();
    int64_t s = 0;
    for (int i = 0; i < N; ++i) {
        std::shared_ptr<std::vector<int>> q = sp;  // 拷贝 = 控制块原子 inc/dec
        s += (*q)[i & 63];
        g_esc = q.get();
    }
    return s;
}
int main() {
    const int R = 5;
    auto med = [](auto f) -> double {
        std::vector<double> t;
        for (int r = 0; r < R; ++r) {
            auto a = std::chrono::steady_clock::now();
            int64_t s = f();
            auto b = std::chrono::steady_clock::now();
            g_sink = s;
            t.push_back(std::chrono::duration<double, std::milli>(b - a).count());
        }
        std::sort(t.begin(), t.end());
        return t[R / 2];
    };
    double t_raw = med(bench_raw);
    double t_hp  = med(bench_hazard);
    double t_sp  = med(bench_shared_ptr);
    std::cout << "raw pointer     : " << t_raw << " ms  (baseline)\n";
    std::cout << "hazard slot     : " << t_hp  << " ms  (" << t_hp / t_raw  << "x)\n";
    std::cout << "shared_ptr copy : " << t_sp  << " ms  (" << t_sp / t_raw  << "x)\n";
    return 0;
}
