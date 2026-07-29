// _bench_d5_79_list.cpp — ch79 D5: list vs vector 遍历 + Stroustrup 有序插入
// g++ -O2 -std=c++17
#include <algorithm>
#include <chrono>
#include <cstdio>
#include <list>
#include <random>
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

int main() {
    std::mt19937 rng(42);

    // ---- 1) 顺序遍历求和：N=1M int ----
    const int N = 1'000'000;
    std::vector<int> v(N);
    for (auto& x : v) x = (int)(rng() & 0xFFFF);
    std::list<int> l(v.begin(), v.end());

    double tv = median5([&] {
        auto a = Clock::now();
        long long s = 0;
        for (int x : v) s += x;
        g_sink = s;
        return ms(a, Clock::now());
    });
    double tl = median5([&] {
        auto a = Clock::now();
        long long s = 0;
        for (int x : l) s += x;
        g_sink = s;
        return ms(a, Clock::now());
    });
    std::printf("traverse_1M,vector,%.3f\n", tv);
    std::printf("traverse_1M,list,%.3f,ratio=%.2f\n", tl, tl / tv);

    // ---- 1b) 打乱堆序后的 list 遍历（真实碎片化场景）----
    // 用大量插删打乱 list 节点在堆上的局部性
    std::list<int> lfrag;
    {
        std::vector<std::list<int>> pool(64);
        for (int i = 0; i < N; ++i) pool[rng() % 64].push_back((int)(rng() & 0xFFFF));
        for (auto& p : pool) lfrag.splice(lfrag.end(), p);
    }
    double tlf = median5([&] {
        auto a = Clock::now();
        long long s = 0;
        for (int x : lfrag) s += x;
        g_sink = s;
        return ms(a, Clock::now());
    });
    std::printf("traverse_1M,list_frag,%.3f,ratio=%.2f\n", tlf, tlf / tv);

    // ---- 2) Stroustrup 有序插入：N=20000 随机数，线性查找插入位 ----
    const int M = 20'000;
    std::vector<int> data(M);
    for (auto& x : data) x = (int)rng();

    double tvi = median5([&] {
        auto a = Clock::now();
        std::vector<int> s;
        s.reserve(M);
        for (int x : data) {
            auto it = s.begin();
            while (it != s.end() && *it < x) ++it;  // 线性查找（与 list 同规则）
            s.insert(it, x);
        }
        g_sink = s.back();
        return ms(a, Clock::now());
    });
    double tli = median5([&] {
        auto a = Clock::now();
        std::list<int> s;
        for (int x : data) {
            auto it = s.begin();
            while (it != s.end() && *it < x) ++it;
            s.insert(it, x);
        }
        g_sink = s.back();
        return ms(a, Clock::now());
    });
    std::printf("ordered_insert_20K,vector,%.3f\n", tvi);
    std::printf("ordered_insert_20K,list,%.3f,ratio=%.2f\n", tli, tli / tvi);

    // ---- 3) 已知位置中部插入：list O(1) 真正赢的场景 ----
    const int K = 100'000;
    double tvm = median5([&] {
        std::vector<int> s(K, 7);
        auto a = Clock::now();
        for (int i = 0; i < 10'000; ++i) s.insert(s.begin() + (long)s.size() / 2, i);
        g_sink = s[K / 2];
        return ms(a, Clock::now());
    });
    double tlm = median5([&] {
        std::list<int> s(K, 7);
        auto mid = std::next(s.begin(), K / 2);  // 预先持有迭代器
        auto a = Clock::now();
        for (int i = 0; i < 10'000; ++i) s.insert(mid, i);
        g_sink = *mid;
        return ms(a, Clock::now());
    });
    std::printf("mid_insert_10K_known_pos,vector,%.3f\n", tvm);
    std::printf("mid_insert_10K_known_pos,list,%.3f,ratio=%.2f\n", tlm, tvm / tlm);
    return 0;
}
