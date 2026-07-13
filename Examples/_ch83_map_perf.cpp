// Examples/_ch83_map_perf.cpp
// 真实基准：std::map vs 排序 vector(flat_map 近似) vs std::unordered_map
// 编译: g++ -O2 -std=c++23 -m64 _ch83_map_perf.cpp -o _ch83_map_perf
//
// 目的：为 ch83_map.md 的"实证替换"提供本机真值，替换 ~N 估算：
//   - 红黑树节点真实大小（节点大小行 / 三 STL 对比表）
//   - map / flat_map / unordered_map 的 find / insert / traverse 真实延迟
//   - 三者的真实内存占用（1M int,int）
// 平台：MinGW GCC 13.1.0 -O2，TSC 2.395 GHz（本机校准，见 _ch120_coroutine_perf）。
//
// 注意：flat_map 插入是 O(N) 移位，与容器大小线性相关；故插入基准在固定
// 中等规模(INS_BASE=20k)下测量，避免 O(N^2) 失控，并标注其大小相关性。
//
// 节点大小测量改用 std::pmr counting_resource —— 不再覆写全局 operator new，
// 避免运行时早期分配 use-before-init 崩溃（上一版 rc=127 即此因）。
#include <iostream>
#include <vector>
#include <map>
#include <unordered_map>
#include <algorithm>
#include <random>
#include <chrono>
#include <cstdint>
#include <cstddef>
#include <memory_resource>
#include <new>
#include <x86intrin.h>

static inline uint64_t rdtsc() { return __rdtsc(); }

// pmr 资源：记录单次分配的最大块（即红黑树节点大小）
struct counting_resource : std::pmr::memory_resource {
    std::size_t max_block = 0;
    std::size_t total = 0;
    void* do_allocate(std::size_t bytes, std::size_t align) override {
        if (bytes > max_block) max_block = bytes;
        total += bytes;
        return ::operator new(bytes, std::align_val_t{align});
    }
    void do_deallocate(void* p, std::size_t bytes, std::size_t align) override {
        ::operator delete(p, std::align_val_t{align});
    }
    bool do_is_equal(const memory_resource& o) const noexcept override { return this == &o; }
};

// noinline 锚点：防止 -O2 把基准循环整体消除
[[gnu::noinline]] int probe_map_find(const std::map<int,int>& m, int k) {
    auto it = m.find(k);
    return it == m.end() ? 0 : it->second;
}
[[gnu::noinline]] int probe_flat_find(const std::vector<std::pair<int,int>>& v, int k) {
    auto it = std::lower_bound(v.begin(), v.end(), std::pair<int,int>{k, 0});
    if (it != v.end() && it->first == k) return it->second;
    return 0;
}
[[gnu::noinline]] int probe_umap_find(const std::unordered_map<int,int>& m, int k) {
    auto it = m.find(k);
    return it == m.end() ? 0 : it->second;
}

int main() {
    const int N = 1'000'000;
    const int M = 300'000;          // find / traverse 基准规模
    const double TSC_GHZ = 2.395;   // 本机校准
    std::mt19937 rng(20240711);
    std::uniform_int_distribution<int> dist(0, N * 20);

    std::vector<std::pair<int,int>> data(N);
    for (auto& p : data) p = {dist(rng), dist(rng)};

    // ---------- 1) 节点真实大小（libstdc++ std::map<int,int>）----------
    counting_resource res;
    {
        std::pmr::map<int,int> m(&res);
        m.insert({777, 888});       // 单次插入 -> 仅 1 个节点分配 -> max_block = 节点大小
    }
    std::size_t node = res.max_block;
    std::cout << "[node] std::map<int,int> node = " << node << " bytes "
              << "(libstdc++ _Rb_tree_node<pair<const int,int>>, pmr 实测)" << std::endl;

    // ---------- 2) 构建三种容器（N=1M，用于 find / traverse）----------
    std::map<int,int> mm;
    for (auto& p : data) mm.insert(p);

    std::vector<std::pair<int,int>> fv = data;
    std::sort(fv.begin(), fv.end());                 // flat_map 的真实用法：先攒后排序

    std::unordered_map<int,int> um;
    for (auto& p : data) um.insert(p);
    std::cout << "[build] 3 containers x 1M done" << std::endl;

    // ---------- 3) find 延迟（RDTSC，含 noinline 锚点）----------
    std::vector<int> q(M);
    for (int i = 0; i < M; ++i) q[i] = dist(rng);

    volatile int sink = 0;
    uint64_t t0, t1;

    t0 = rdtsc(); for (int i = 0; i < M; ++i) sink += probe_map_find(mm, q[i]);
    t1 = rdtsc();
    double map_find_ns  = (double)(t1 - t0) / M / TSC_GHZ;

    t0 = rdtsc(); for (int i = 0; i < M; ++i) sink += probe_flat_find(fv, q[i]);
    t1 = rdtsc();
    double flat_find_ns = (double)(t1 - t0) / M / TSC_GHZ;

    t0 = rdtsc(); for (int i = 0; i < M; ++i) sink += probe_umap_find(um, q[i]);
    t1 = rdtsc();
    double umap_find_ns = (double)(t1 - t0) / M / TSC_GHZ;
    std::cout << "[find] measured" << std::endl;

    // ---------- 4) traverse 延迟（每元素 ns，steady_clock）----------
    auto traverse_ns_per_elem = [&](auto&& measure) -> double {
        auto a = std::chrono::steady_clock::now();
        sink += measure();
        auto b = std::chrono::steady_clock::now();
        return std::chrono::duration<double, std::nano>(b - a).count() / N;
    };
    auto map_trav = [&]() { int s = 0; for (auto& kv : mm) s += kv.second; return s; };
    auto flat_trav= [&]() { int s = 0; for (auto& kv : fv) s += kv.second; return s; };
    double map_trav_ns  = traverse_ns_per_elem(map_trav);
    double flat_trav_ns = traverse_ns_per_elem(flat_trav);

    // ---------- 5) insert 平均延迟（固定小规模，避免 O(N^2)；flat 为 O(N) 移位，标注规模相关）----------
    const int INS_BASE = 20'000;
    const int INS_M    = 10'000;
    std::map<int,int> mm_i;            for (int i = 0; i < INS_BASE; ++i) mm_i.insert({i*2, i});
    std::unordered_map<int,int> um_i;  for (int i = 0; i < INS_BASE; ++i) um_i.insert({i*2, i});
    std::vector<std::pair<int,int>> fv_i;
    for (int i = 0; i < INS_BASE; ++i) fv_i.push_back({i*2, i});   // 已排序
    std::vector<int> q2(INS_M);
    for (int i = 0; i < INS_M; ++i) q2[i] = i*2 + 1;               // 与基线不重叠的新键

    auto insert_ns = [&](auto&& do_insert) -> double {
        auto a = std::chrono::steady_clock::now();
        do_insert();
        auto b = std::chrono::steady_clock::now();
        return std::chrono::duration<double, std::nano>(b - a).count() / INS_M;
    };
    double map_insert_ns  = insert_ns([&]() { for (int k : q2) mm_i.insert({k, k}); });
    double umap_insert_ns = insert_ns([&]() { for (int k : q2) um_i.insert({k, k}); });
    double flat_insert_ns = insert_ns([&]() {                 // O(N) 移位，规模相关
        for (int k : q2) {
            auto it = std::lower_bound(fv_i.begin(), fv_i.end(), std::pair<int,int>{k, 0});
            fv_i.insert(it, {k, k});
        }
    });
    std::cout << "[insert] measured (base=" << INS_BASE << ", add=" << INS_M << ")" << std::endl;

    // ---------- 6) 内存占用（稳态，N=1M 元素）----------
    double map_mem_MB  = (double)N * node / (1024.0 * 1024.0);
    double flat_mem_MB = (double)N * sizeof(std::pair<int,int>) / (1024.0 * 1024.0);
    // libstdc++ _Hash_node<int,int> ≈ 指针(8) + hash(8) + pair(8) = 24B；桶数组 N×8B
    double umap_node = 24.0;
    double umap_mem_MB = (double)N * (umap_node + 8.0) / (1024.0 * 1024.0);

    // ---------- 输出 ----------
    std::cout << "\n=== 实测（GCC 13.1 -O2, TSC " << TSC_GHZ << "GHz, N=" << N << ") ===" << std::endl;
    std::cout << "node_size_B      : " << node << std::endl;
    std::cout << "map_find_ns      : " << map_find_ns  << std::endl;
    std::cout << "flat_find_ns     : " << flat_find_ns << std::endl;
    std::cout << "umap_find_ns     : " << umap_find_ns << std::endl;
    std::cout << "map_insert_ns    : " << map_insert_ns  << "  (base=" << INS_BASE << ")" << std::endl;
    std::cout << "flat_insert_ns   : " << flat_insert_ns << "  (base=" << INS_BASE << ", O(N)移位)" << std::endl;
    std::cout << "umap_insert_ns   : " << umap_insert_ns << "  (base=" << INS_BASE << ")" << std::endl;
    std::cout << "map_trav_ns_elem : " << map_trav_ns  << std::endl;
    std::cout << "flat_trav_ns_elem: " << flat_trav_ns << std::endl;
    std::cout << "map_mem_MB       : " << map_mem_MB  << std::endl;
    std::cout << "flat_mem_MB      : " << flat_mem_MB << std::endl;
    std::cout << "umap_mem_MB      : " << umap_mem_MB << std::endl;
    std::cout << "[sink] " << sink << std::endl;   // 防止基准被整体消除
    return 0;
}
