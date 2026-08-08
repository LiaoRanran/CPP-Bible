// _bench_d5_ch84_set_multiset.cpp
// 红黑树有序集合 (set/multiset) vs 排序数组的性能权衡
// 编译: g++ -O2 -std=c++23 _bench_d5_ch84_set_multiset.cpp -o _bench_d5_ch84
// 环境: AMD Ryzen 9 7940HX, GCC 15.3.0 (MinGW-w64), 5轮取中位

#include <set>
#include <vector>
#include <algorithm>
#include <chrono>
#include <iostream>
#include <random>
#include <cstdint>

// volatile sink: 防止优化器消除整个循环
static volatile long long g_sink = 0;

// 计时辅助: 返回毫秒
template<typename F>
static long long time_ms(F&& func) {
    using namespace std::chrono;
    auto t0 = high_resolution_clock::now();
    func();
    auto t1 = high_resolution_clock::now();
    return duration_cast<milliseconds>(t1 - t0).count();
}

// 取5轮中位数
template<typename F>
static long long median5(F&& func) {
    long long results[5];
    for (int i = 0; i < 5; ++i) {
        results[i] = time_ms(func);
    }
    std::sort(results, results + 5);
    return results[2];  // 中位数
}

int main() {
    // 数据量: 1,000,000 个 int
    constexpr int N = 1'000'000;
    // 查询次数: 1,000,000 次
    constexpr int Q = 1'000'000;

    // 生成随机数据
    std::mt19937 rng(42);
    std::vector<int> data(N);
    for (int i = 0; i < N; ++i) data[i] = i;
    std::shuffle(data.begin(), data.end(), rng);

    // 查询键: 混合命中与未命中
    std::vector<int> queries(Q);
    std::mt19937 qrng(123);
    for (int i = 0; i < Q; ++i) {
        queries[i] = static_cast<int>(qrng() % (N * 2));
    }

    std::cout << "=== ch84 set/multiset vs sorted vector 性能基准 ===" << std::endl;
    std::cout << "数据量 N = " << N << ", 查询数 Q = " << Q << std::endl;
    std::cout << std::endl;

    // ================================================================
    // 场景1: multiset 逐个插入 + 查询 vs sorted vector + lower_bound
    // 模拟"批量构建后查询"场景
    // ================================================================
    {
        std::cout << "--- 场景1: multiset 插入+查询 vs sorted vector+lower_bound ---" << std::endl;

        // 1a: multiset 逐个插入
        auto t_ms_insert = median5([&]() {
            std::multiset<int> ms;
            for (int i = 0; i < N; ++i) ms.insert(data[i]);
            g_sink = g_sink + ms.size();
        });
        std::cout << "multiset 插入 " << N << " 个元素: " << t_ms_insert << " ms" << std::endl;

        // 1b: multiset 查询 (在已构建的 multiset 上)
        std::multiset<int> ms_built;
        for (int i = 0; i < N; ++i) ms_built.insert(data[i]);
        auto t_ms_query = median5([&]() {
            long long sum = 0;
            for (int i = 0; i < Q; ++i) {
                auto it = ms_built.find(queries[i]);
                if (it != ms_built.end()) sum += *it;
            }
            g_sink = g_sink + sum;
        });
        std::cout << "multiset 查询 " << Q << " 次: " << t_ms_query << " ms" << std::endl;

        // 1c: vector push_back + sort + unique (批量构建)
        auto t_vec_build = median5([&]() {
            std::vector<int> v;
            v.reserve(N);
            for (int i = 0; i < N; ++i) v.push_back(data[i]);
            std::sort(v.begin(), v.end());
            v.erase(std::unique(v.begin(), v.end()), v.end());
            g_sink = g_sink + (long long)v.size();
        });
        std::cout << "vector push_back+sort+unique " << N << " 个: " << t_vec_build << " ms" << std::endl;

        // 1d: vector 查询 (lower_bound on sorted vector)
        std::vector<int> v_built;
        v_built.reserve(N);
        for (int i = 0; i < N; ++i) v_built.push_back(data[i]);
        std::sort(v_built.begin(), v_built.end());
        v_built.erase(std::unique(v_built.begin(), v_built.end()), v_built.end());
        auto t_vec_query = median5([&]() {
            long long sum = 0;
            for (int i = 0; i < Q; ++i) {
                auto it = std::lower_bound(v_built.begin(), v_built.end(), queries[i]);
                if (it != v_built.end() && *it == queries[i]) sum += *it;
            }
            g_sink = g_sink + sum;
        });
        std::cout << "vector lower_bound 查询 " << Q << " 次: " << t_vec_query << " ms" << std::endl;

        std::cout << std::endl;
    }

    // ================================================================
    // 场景2: set::find vs sorted vector::binary_search (纯查询性能)
    // ================================================================
    {
        std::cout << "--- 场景2: set::find vs sorted vector::binary_search ---" << std::endl;

        // 构建 set 和 sorted vector (用相同数据, 已排序)
        std::set<int> s;
        for (int i = 0; i < N; ++i) s.insert(data[i]);
        std::vector<int> sv(data.begin(), data.end());
        std::sort(sv.begin(), sv.end());
        sv.erase(std::unique(sv.begin(), sv.end()), sv.end());

        // 2a: set::find
        auto t_set_find = median5([&]() {
            long long sum = 0;
            for (int i = 0; i < Q; ++i) {
                if (s.find(queries[i]) != s.end()) sum += queries[i];
            }
            g_sink = g_sink + sum;
        });
        std::cout << "set::find " << Q << " 次: " << t_set_find << " ms" << std::endl;

        // 2b: set::contains (C++20)
        auto t_set_contains = median5([&]() {
            long long sum = 0;
            for (int i = 0; i < Q; ++i) {
                if (s.contains(queries[i])) sum += queries[i];
            }
            g_sink = g_sink + sum;
        });
        std::cout << "set::contains " << Q << " 次: " << t_set_contains << " ms" << std::endl;

        // 2c: vector binary_search
        auto t_vec_bs = median5([&]() {
            long long sum = 0;
            for (int i = 0; i < Q; ++i) {
                if (std::binary_search(sv.begin(), sv.end(), queries[i])) sum += queries[i];
            }
            g_sink = g_sink + sum;
        });
        std::cout << "vector::binary_search " << Q << " 次: " << t_vec_bs << " ms" << std::endl;

        // 2d: vector lower_bound (等效查找)
        auto t_vec_lb = median5([&]() {
            long long sum = 0;
            for (int i = 0; i < Q; ++i) {
                auto it = std::lower_bound(sv.begin(), sv.end(), queries[i]);
                if (it != sv.end() && *it == queries[i]) sum += queries[i];
            }
            g_sink = g_sink + sum;
        });
        std::cout << "vector::lower_bound " << Q << " 次: " << t_vec_lb << " ms" << std::endl;

        std::cout << std::endl;
    }

    // ================================================================
    // 场景3: 逐个插入 vs 批量插入 (sort + unique) 的性能差异
    // ================================================================
    {
        std::cout << "--- 场景3: 逐个插入(set) vs 批量插入(vector+sort+unique) ---" << std::endl;

        // 3a: set 逐个插入 (每次 insert 触发红黑树平衡 + 节点分配)
        auto t_set_insert = median5([&]() {
            std::set<int> s;
            for (int i = 0; i < N; ++i) s.insert(data[i]);
            g_sink = g_sink + (long long)s.size();
        });
        std::cout << "set 逐个插入 " << N << " 个: " << t_set_insert << " ms" << std::endl;

        // 3b: multiset 逐个插入
        auto t_ms_insert = median5([&]() {
            std::multiset<int> ms;
            for (int i = 0; i < N; ++i) ms.insert(data[i]);
            g_sink = g_sink + (long long)ms.size();
        });
        std::cout << "multiset 逐个插入 " << N << " 个: " << t_ms_insert << " ms" << std::endl;

        // 3c: vector push_back + sort + unique
        auto t_vec_sort = median5([&]() {
            std::vector<int> v;
            v.reserve(N);
            for (int i = 0; i < N; ++i) v.push_back(data[i]);
            std::sort(v.begin(), v.end());
            v.erase(std::unique(v.begin(), v.end()), v.end());
            g_sink = g_sink + (long long)v.size();
        });
        std::cout << "vector push_back+sort+unique " << N << " 个: " << t_vec_sort << " ms" << std::endl;

        // 3d: set 从已排序区间构造 (range constructor)
        std::vector<int> sorted_data(data.begin(), data.end());
        std::sort(sorted_data.begin(), sorted_data.end());
        sorted_data.erase(std::unique(sorted_data.begin(), sorted_data.end()), sorted_data.end());
        auto t_set_range = median5([&]() {
            std::set<int> s(sorted_data.begin(), sorted_data.end());
            g_sink = g_sink + (long long)s.size();
        });
        std::cout << "set 从已排序区间构造 " << sorted_data.size() << " 个: " << t_set_range << " ms" << std::endl;

        std::cout << std::endl;
    }

    // ================================================================
    // 场景4: 有序遍历 — set 中序遍历 vs vector 顺序遍历
    // ================================================================
    {
        std::cout << "--- 场景4: 有序遍历 set vs vector ---" << std::endl;

        // 构建数据
        std::set<int> s;
        for (int i = 0; i < N; ++i) s.insert(data[i]);
        std::vector<int> v(s.begin(), s.end());  // 已排序

        // 4a: set 中序遍历 (指针追逐, 缓存不友好)
        auto t_set_iter = median5([&]() {
            long long sum = 0;
            for (int rep = 0; rep < 10; ++rep) {
                for (auto it = s.begin(); it != s.end(); ++it) {
                    sum += *it;
                }
            }
            g_sink = g_sink + sum;
        });
        std::cout << "set 中序遍历 " << N << " 个 x10 轮: " << t_set_iter << " ms" << std::endl;

        // 4b: vector 顺序遍历 (连续内存, 缓存友好)
        auto t_vec_iter = median5([&]() {
            long long sum = 0;
            for (int rep = 0; rep < 10; ++rep) {
                for (int i = 0; i < (int)v.size(); ++i) {
                    sum += v[i];
                }
            }
            g_sink = g_sink + sum;
        });
        std::cout << "vector 顺序遍历 " << v.size() << " 个 x10 轮: " << t_vec_iter << " ms" << std::endl;

        // 4c: set 用 for-range (同 4a 但语法不同)
        auto t_set_range = median5([&]() {
            long long sum = 0;
            for (int rep = 0; rep < 10; ++rep) {
                for (int x : s) {
                    sum += x;
                }
            }
            g_sink = g_sink + sum;
        });
        std::cout << "set for-range 遍历 " << N << " 个 x10 轮: " << t_set_range << " ms" << std::endl;

        std::cout << std::endl;
    }

    // ================================================================
    // 场景5: 节点分配开销 — set 内存占用 vs vector 内存占用
    // ================================================================
    {
        std::cout << "--- 场景5: 内存占用对比 ---" << std::endl;

        std::set<int> s;
        for (int i = 0; i < N; ++i) s.insert(data[i]);
        std::vector<int> v(s.begin(), s.end());

        std::cout << "set<int> 元素数: " << s.size() << std::endl;
        std::cout << "vector<int> 元素数: " << v.size() << std::endl;
        std::cout << "set<int> 对象大小: " << sizeof(s) << " bytes" << std::endl;
        std::cout << "vector<int> 对象大小: " << sizeof(v) << " bytes" << std::endl;
        std::cout << "vector capacity: " << v.capacity() << std::endl;
        // set 每节点 ~40 bytes (3 ptr + color + value + padding)
        // vector 每 int 4 bytes, 连续存储
        std::cout << "set 估算总内存 (每节点~40B): ~" << (s.size() * 40LL / 1024 / 1024) << " MB" << std::endl;
        std::cout << "vector 估算总内存: ~" << (v.capacity() * 4LL / 1024 / 1024) << " MB" << std::endl;
        std::cout << "内存膨胀比 (set/vector): ~" << (s.size() * 40LL) / (v.capacity() * 4LL) << "x" << std::endl;
        std::cout << std::endl;
    }

    std::cout << "=== 基准完成 ===" << std::endl;
    return 0;
}
