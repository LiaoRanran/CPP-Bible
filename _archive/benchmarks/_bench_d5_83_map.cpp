// _bench_d5_83_map.cpp — ch83 D5: map(红黑树) vs unordered_map(哈希) 插入/查找
// g++ -O2 -std=c++17
#include <algorithm>
#include <chrono>
#include <cstdio>
#include <map>
#include <random>
#include <string>
#include <unordered_map>
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
    std::mt19937_64 rng(42);
    const int N = 1'000'000;
    std::vector<long long> keys(N);
    for (auto& k : keys) k = (long long)rng();

    // ---- int 键：插入 ----
    double mi = median5([&] {
        auto a = Clock::now();
        std::map<long long, int> m;
        for (int i = 0; i < N; ++i) m.emplace(keys[i], i);
        g_sink = (long long)m.size();
        return ms(a, Clock::now());
    });
    double ui = median5([&] {
        auto a = Clock::now();
        std::unordered_map<long long, int> m;  // 不 reserve（含 rehash 成本，贴近默认用法）
        for (int i = 0; i < N; ++i) m.emplace(keys[i], i);
        g_sink = (long long)m.size();
        return ms(a, Clock::now());
    });
    double ur = median5([&] {
        auto a = Clock::now();
        std::unordered_map<long long, int> m;
        m.reserve(N);
        for (int i = 0; i < N; ++i) m.emplace(keys[i], i);
        g_sink = (long long)m.size();
        return ms(a, Clock::now());
    });
    std::printf("insert_1M_int,map,%.3f\n", mi);
    std::printf("insert_1M_int,umap,%.3f,ratio=%.2f\n", ui, mi / ui);
    std::printf("insert_1M_int,umap_reserve,%.3f,ratio=%.2f\n", ur, mi / ur);

    // ---- int 键：命中查找 ----
    std::map<long long, int> M;
    std::unordered_map<long long, int> U;
    U.reserve(N);
    for (int i = 0; i < N; ++i) { M.emplace(keys[i], i); U.emplace(keys[i], i); }
    std::vector<long long> probe = keys;
    std::shuffle(probe.begin(), probe.end(), rng);

    double mf = median5([&] {
        auto a = Clock::now();
        long long s = 0;
        for (auto k : probe) s += M.find(k)->second;
        g_sink = s;
        return ms(a, Clock::now());
    });
    double uf = median5([&] {
        auto a = Clock::now();
        long long s = 0;
        for (auto k : probe) s += U.find(k)->second;
        g_sink = s;
        return ms(a, Clock::now());
    });
    std::printf("find_1M_int,map,%.3f\n", mf);
    std::printf("find_1M_int,umap,%.3f,ratio=%.2f\n", uf, mf / uf);

    // ---- string 键（24 字符，超 SSO）：查找 ----
    const int NS = 200'000;
    std::vector<std::string> skeys(NS);
    for (int i = 0; i < NS; ++i) {
        char buf[32];
        std::snprintf(buf, sizeof buf, "key_%016llx_%04d", (unsigned long long)rng(), i);
        skeys[i] = buf;  // 长度 25 > 15，堆分配键
    }
    std::map<std::string, int> MS;
    std::unordered_map<std::string, int> US;
    US.reserve(NS);
    for (int i = 0; i < NS; ++i) { MS.emplace(skeys[i], i); US.emplace(skeys[i], i); }
    std::vector<const std::string*> sprobe;
    for (auto& s : skeys) sprobe.push_back(&s);
    std::shuffle(sprobe.begin(), sprobe.end(), rng);

    double msf = median5([&] {
        auto a = Clock::now();
        long long s = 0;
        for (auto* k : sprobe) s += MS.find(*k)->second;
        g_sink = s;
        return ms(a, Clock::now());
    });
    double usf = median5([&] {
        auto a = Clock::now();
        long long s = 0;
        for (auto* k : sprobe) s += US.find(*k)->second;
        g_sink = s;
        return ms(a, Clock::now());
    });
    std::printf("find_200K_str24,map,%.3f\n", msf);
    std::printf("find_200K_str24,umap,%.3f,ratio=%.2f\n", usf, msf / usf);

    // ---- 有序遍历：map 免费拿到，umap 需拷出排序 ----
    double mo = median5([&] {
        auto a = Clock::now();
        long long s = 0;
        for (auto& [k, v] : M) s += v;
        g_sink = s;
        return ms(a, Clock::now());
    });
    double uo = median5([&] {
        auto a = Clock::now();
        std::vector<std::pair<long long, int>> tmp(U.begin(), U.end());
        std::sort(tmp.begin(), tmp.end());
        long long s = 0;
        for (auto& [k, v] : tmp) s += v;
        g_sink = s;
        return ms(a, Clock::now());
    });
    std::printf("ordered_scan_1M,map,%.3f\n", mo);
    std::printf("ordered_scan_1M,umap_copy_sort,%.3f,ratio=%.2f\n", uo, uo / mo);
    return 0;
}
