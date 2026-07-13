#include <vector>
#include <algorithm>
#include <random>
#include <chrono>
#include <iostream>

using clk = std::chrono::steady_clock;

int main() {
    const int N = 500'000;
    const int M = 20'000;
    std::vector<int> base(N);
    std::mt19937 rng(20240708);
    std::uniform_int_distribution<int> dist(0, N * 10);
    for (int i = 0; i < N; ++i) base[i] = dist(rng);

    // --- 场景1：构建（make_heap vs sort）---
    {
        std::vector<int> v = base;
        auto t0 = clk::now();
        std::make_heap(v.begin(), v.end());
        auto t1 = clk::now();
        std::cout << "make_heap N=" << N << " : "
                  << std::chrono::duration<double, std::micro>(t1 - t0).count()
                  << " us\n";
    }
    {
        std::vector<int> v = base;
        auto t0 = clk::now();
        std::sort(v.begin(), v.end());
        auto t1 = clk::now();
        std::cout << "sort      N=" << N << " : "
                  << std::chrono::duration<double, std::micro>(t1 - t0).count()
                  << " us\n";
    }

    // --- 场景2：Top-K 提取（pop_heap 重复 vs 排序后顺序读）---
    {
        std::vector<int> v = base;
        std::make_heap(v.begin(), v.end());
        auto t0 = clk::now();
        for (int k = 0; k < M; ++k) {
            std::pop_heap(v.begin(), v.end() - k);
        }
        auto t1 = clk::now();
        std::cout << "pop_heap  Top-" << M << " : "
                  << std::chrono::duration<double, std::micro>(t1 - t0).count()
                  << " us\n";
    }
    {
        std::vector<int> v = base;
        std::sort(v.begin(), v.end(), std::greater<int>());
        auto t0 = clk::now();
        volatile int sink = 0;
        for (int k = 0; k < M; ++k) sink = v[k];
        (void)sink;
        auto t1 = clk::now();
        std::cout << "sorted-read Top-" << M << " : "
                  << std::chrono::duration<double, std::micro>(t1 - t0).count()
                  << " us\n";
    }

    // --- 场景3：成员查询（堆上线性扫描 vs 排序后 binary_search）---
    {
        std::vector<int> v = base;
        std::make_heap(v.begin(), v.end());
        auto t0 = clk::now();
        int hits = 0;
        for (int k = 0; k < M; ++k) {
            int q = base[k];
            if (std::find(v.begin(), v.end(), q) != v.end()) ++hits;
        }
        auto t1 = clk::now();
        std::cout << "heap-linearsearch M=" << M << " : "
                  << std::chrono::duration<double, std::micro>(t1 - t0).count()
                  << " us (hits=" << hits << ")\n";
    }
    {
        std::vector<int> v = base;
        std::sort(v.begin(), v.end());
        auto t0 = clk::now();
        int hits = 0;
        for (int k = 0; k < M; ++k) {
            int q = base[k];
            if (std::binary_search(v.begin(), v.end(), q)) ++hits;
        }
        auto t1 = clk::now();
        std::cout << "sorted-bsearch M=" << M << " : "
                  << std::chrono::duration<double, std::micro>(t1 - t0).count()
                  << " us (hits=" << hits << ")\n";
    }
    return 0;
}
