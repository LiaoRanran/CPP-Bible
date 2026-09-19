// D5 Wave 3 benchmark: ch85 unordered_map/set — 哈希开链 vs 红黑树(map)
// 编译: g++ -O2 -std=c++23 -o bench.exe _bench_d5_85_unordered.cpp
// 目的: 量化 unordered_map 插入(是否 reserve 影响 rehash) 与 查找 相比 map 的代价.
#include <iostream>
#include <chrono>
#include <vector>
#include <unordered_map>
#include <map>
#include <random>
#include <cstdint>

static volatile long long g_esc = 0;

template <class F>
double bench(const char* name, F f, int rounds = 5) {
    double best = 1e18;
    for (int r = 0; r < rounds; ++r) {
        auto t0 = std::chrono::steady_clock::now();
        long long res = f();
        auto t1 = std::chrono::steady_clock::now();
        g_esc += res;
        double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
        if (ms < best) best = ms;
    }
    std::cout << name << ": " << best << " ms\n";
    return best;
}

int main() {
    const int N = 1'000'000;
    std::mt19937 rng(7);
    std::uniform_int_distribution<int> dist(0, 100'000'000);
    std::vector<int> keys(N);
    for (int i = 0; i < N; ++i) keys[i] = dist(rng);

    bench("umap_insert_noreserve", [&] {
        std::unordered_map<int, int> um;
        int64_t s = 0;
        for (int i = 0; i < N; ++i) { um[keys[i]] = i; s += (int64_t)um.size(); }
        return s;
    });
    bench("umap_insert_reserve", [&] {
        std::unordered_map<int, int> um;
        um.reserve(N);
        int64_t s = 0;
        for (int i = 0; i < N; ++i) { um[keys[i]] = i; s += (int64_t)um.size(); }
        return s;
    });
    bench("map_insert", [&] {
        std::map<int, int> m;
        int64_t s = 0;
        for (int i = 0; i < N; ++i) { m[keys[i]] = i; s += (int64_t)m.size(); }
        return s;
    });

    std::unordered_map<int, int> um;
    um.reserve(N);
    for (int i = 0; i < N; ++i) um[keys[i]] = i;
    std::map<int, int> m;
    for (int i = 0; i < N; ++i) m[keys[i]] = i;

    bench("umap_lookup", [&] {
        int64_t s = 0;
        for (int i = 0; i < N; ++i) s += um.find(keys[i])->second;
        return s;
    });
    bench("map_lookup", [&] {
        int64_t s = 0;
        for (int i = 0; i < N; ++i) s += m.find(keys[i])->second;
        return s;
    });

    std::cout << "esc=" << g_esc << "\n";
    return 0;
}
