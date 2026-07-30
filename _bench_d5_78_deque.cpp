// D5 Wave 4 benchmark: ch78 deque — vector vs deque 的四项真实差价
// 编译: g++ -O2 -std=c++23 -o bench.exe _bench_d5_78_deque.cpp
// 场景: push_back(无 reserve) / 顺序遍历求和 / 随机下标访问 / 头部插入(规模缩小防 O(N^2))
#include <iostream>
#include <chrono>
#include <vector>
#include <deque>
#include <random>
#include <cstdint>

static volatile long long g_esc = 0;

int main() {
    const int N = 2'000'000;
    std::mt19937 rng(42);
    auto ms = [](auto a, auto b) { return std::chrono::duration<double, std::milli>(b - a).count(); };

    std::vector<int> data(N);
    for (auto& x : data) x = static_cast<int>(rng());

    // 1) push_back
    auto t0 = std::chrono::steady_clock::now();
    std::vector<int> v; for (int i = 0; i < N; ++i) v.push_back(data[i]);
    auto t1 = std::chrono::steady_clock::now();
    std::deque<int> d;  for (int i = 0; i < N; ++i) d.push_back(data[i]);
    auto t2 = std::chrono::steady_clock::now();

    // 2) 顺序遍历
    long long s1 = 0; for (int x : v) s1 += x;
    auto t3 = std::chrono::steady_clock::now();
    long long s2 = 0; for (int x : d) s2 += x;
    auto t4 = std::chrono::steady_clock::now();

    // 3) 随机下标访问 (同一下标序列)
    std::vector<int> idx(N);
    for (auto& x : idx) x = static_cast<int>(rng() % N);
    auto t5 = std::chrono::steady_clock::now();
    long long s3 = 0; for (int i : idx) s3 += v[i];
    auto t6 = std::chrono::steady_clock::now();
    long long s4 = 0; for (int i : idx) s4 += d[i];
    auto t7 = std::chrono::steady_clock::now();

    // 4) 头部插入 (M=100K, vector 是 O(N^2) 故规模独立)
    const int M = 100'000;
    auto t8 = std::chrono::steady_clock::now();
    std::deque<int> df; for (int i = 0; i < M; ++i) df.push_front(data[i]);
    auto t9 = std::chrono::steady_clock::now();
    std::vector<int> vf; for (int i = 0; i < M; ++i) vf.insert(vf.begin(), data[i]);
    auto t10 = std::chrono::steady_clock::now();

    g_esc = s1 + s2 + s3 + s4 + v.size() + d.size() + df.front() + vf.front();
    std::cout << "vector_push_back   " << ms(t0, t1) << " ms\n";
    std::cout << "deque_push_back    " << ms(t1, t2) << " ms\n";
    std::cout << "vector_traverse    " << ms(t2, t3) << " ms\n";
    std::cout << "deque_traverse     " << ms(t3, t4) << " ms\n";
    std::cout << "vector_random_idx  " << ms(t5, t6) << " ms\n";
    std::cout << "deque_random_idx   " << ms(t6, t7) << " ms\n";
    std::cout << "deque_push_front(100K)   " << ms(t8, t9) << " ms\n";
    std::cout << "vector_insert_begin(100K) " << ms(t9, t10) << " ms\n";
    std::cout << "esc=" << g_esc << "\n";
    return 0;
}
