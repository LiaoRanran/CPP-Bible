// D5 Wave 4 benchmark: ch97 search — 同为查找, sorted vector / set / unordered_set 的真实差价
// 编译: g++ -O2 -std=c++23 -o bench.exe _bench_d5_97_search.cpp
// 设计要点: lower_bound 与 set::find 同为 O(log n), 但隐式数组二分是缓存友好的地址计算,
//   红黑树查找是逐层指针追逐(每层≈一次 cache miss)。unordered O(1) 作参照。
#include <iostream>
#include <chrono>
#include <vector>
#include <set>
#include <unordered_set>
#include <algorithm>
#include <random>
#include <cstdint>

static volatile long long g_esc = 0;

int main() {
    const int N = 4'000'000;
    const int Q = 2'000'000;
    std::mt19937_64 rng(42);
    auto ms = [](auto a, auto b) { return std::chrono::duration<double, std::milli>(b - a).count(); };

    std::vector<long long> keys(N);
    for (auto& k : keys) k = static_cast<long long>(rng());
    std::vector<long long> sorted = keys;
    std::sort(sorted.begin(), sorted.end());
    std::set<long long> st(keys.begin(), keys.end());
    std::unordered_set<long long> us(keys.begin(), keys.end());

    std::vector<long long> queries(Q);
    for (int i = 0; i < Q; ++i) queries[i] = keys[rng() % N];   // 全命中查询

    auto t0 = std::chrono::steady_clock::now();
    long long h1 = 0;
    for (auto q : queries) {
        auto it = std::lower_bound(sorted.begin(), sorted.end(), q);
        if (it != sorted.end() && *it == q) h1++;
    }
    auto t1 = std::chrono::steady_clock::now();
    long long h2 = 0;
    for (auto q : queries) h2 += (st.find(q) != st.end());
    auto t2 = std::chrono::steady_clock::now();
    long long h3 = 0;
    for (auto q : queries) h3 += (us.find(q) != us.end());
    auto t3 = std::chrono::steady_clock::now();

    g_esc = h1 + h2 + h3;
    std::cout << "vector_lower_bound " << ms(t0, t1) << " ms\n";
    std::cout << "set_find           " << ms(t1, t2) << " ms\n";
    std::cout << "unordered_find     " << ms(t2, t3) << " ms\n";
    std::cout << "esc=" << g_esc << " (h=" << h1 << "/" << h2 << "/" << h3 << ")\n";
    return 0;
}
