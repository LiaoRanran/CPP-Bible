// _bench_d5_122_pmr.cpp — ch122 D5: pmr 资源 vs 全局 new 小对象风暴
// g++ -O2 -std=c++17
#include <algorithm>
#include <chrono>
#include <cstdio>
#include <list>
#include <memory_resource>
#include <string>
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
    const int N = 200'000;

    // ---- 1) list<int> 节点风暴（每节点一次堆分配）----
    double t_std = median5([&] {
        auto a = Clock::now();
        std::list<int> l;
        for (int i = 0; i < N; ++i) l.push_back(i);
        long long s = 0;
        for (int x : l) s += x;
        g_sink = s;
        return ms(a, Clock::now());
    });
    double t_mono = median5([&] {
        auto a = Clock::now();
        std::pmr::monotonic_buffer_resource mbr;
        std::pmr::list<int> l(&mbr);
        for (int i = 0; i < N; ++i) l.push_back(i);
        long long s = 0;
        for (int x : l) s += x;
        g_sink = s;
        return ms(a, Clock::now());
    });
    double t_pool = median5([&] {
        auto a = Clock::now();
        std::pmr::unsynchronized_pool_resource pool;
        std::pmr::list<int> l(&pool);
        for (int i = 0; i < N; ++i) l.push_back(i);
        long long s = 0;
        for (int x : l) s += x;
        g_sink = s;
        return ms(a, Clock::now());
    });
    std::printf("list_200K,std_new,%.3f\n", t_std);
    std::printf("list_200K,pmr_monotonic,%.3f,speedup=%.2f\n", t_mono, t_std / t_mono);
    std::printf("list_200K,pmr_pool,%.3f,speedup=%.2f\n", t_pool, t_std / t_pool);

    // ---- 2) 重建循环：monotonic release 复用 vs 每轮 new/delete ----
    const int ROUNDS = 200, M = 10'000;
    double t_std2 = median5([&] {
        auto a = Clock::now();
        long long s = 0;
        for (int r = 0; r < ROUNDS; ++r) {
            std::list<int> l;
            for (int i = 0; i < M; ++i) l.push_back(i);
            s += l.back();
        }
        g_sink = s;
        return ms(a, Clock::now());
    });
    double t_mono2 = median5([&] {
        auto a = Clock::now();
        long long s = 0;
        std::pmr::monotonic_buffer_resource mbr;
        for (int r = 0; r < ROUNDS; ++r) {
            std::pmr::list<int> l(&mbr);
            for (int i = 0; i < M; ++i) l.push_back(i);
            s += l.back();
            l.clear();
            mbr.release();  // 一把梭清空，O(块数)
        }
        g_sink = s;
        return ms(a, Clock::now());
    });
    std::printf("rebuild_200x10K,std_new,%.3f\n", t_std2);
    std::printf("rebuild_200x10K,pmr_mono_release,%.3f,speedup=%.2f\n", t_mono2, t_std2 / t_mono2);

    // ---- 3) pmr::string 向量（小串 SSO 内不分配 → pmr 无收益的反例）----
    const int NS = 500'000;
    double t_sstd = median5([&] {
        auto a = Clock::now();
        std::vector<std::string> v;
        v.reserve(NS);
        for (int i = 0; i < NS; ++i) v.emplace_back("short");  // 5 字符，SSO
        g_sink = (long long)v.back().size();
        return ms(a, Clock::now());
    });
    double t_spmr = median5([&] {
        auto a = Clock::now();
        std::pmr::monotonic_buffer_resource mbr;
        std::pmr::vector<std::pmr::string> v(&mbr);
        v.reserve(NS);
        for (int i = 0; i < NS; ++i) v.emplace_back("short");
        g_sink = (long long)v.back().size();
        return ms(a, Clock::now());
    });
    std::printf("sso_str_500K,std,%.3f\n", t_sstd);
    std::printf("sso_str_500K,pmr_mono,%.3f,speedup=%.2f\n", t_spmr, t_sstd / t_spmr);
    return 0;
}
