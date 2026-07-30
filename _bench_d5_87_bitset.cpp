// D5 Wave 4 benchmark: ch87 bitset — bitset / vector<bool> / vector<char> 三种"位集合"的真实差价
// 编译: g++ -O2 -std=c++23 -o bench.exe _bench_d5_87_bitset.cpp
// 场景: (a) 1000 万次随机置位; (b) 全量 count 统计 1 的个数 (重复 10 遍放大信号)
#include <iostream>
#include <chrono>
#include <bitset>
#include <vector>
#include <random>
#include <algorithm>
#include <cstdint>

static volatile long long g_esc = 0;
constexpr std::size_t NBITS = 100'000'000;   // 1 亿位: bitset=12.5MB, vector<char>=100MB
static std::bitset<NBITS> bs;                // 静态存储, 避免栈溢出

int main() {
    const int SETS = 10'000'000;
    const int REP = 10;
    std::mt19937_64 rng(42);
    auto ms = [](auto a, auto b) { return std::chrono::duration<double, std::milli>(b - a).count(); };

    std::vector<std::size_t> pos(SETS);
    for (auto& p : pos) p = rng() % NBITS;

    std::vector<bool> vb(NBITS);
    std::vector<char> vc(NBITS, 0);

    // (a) 随机置位
    auto t0 = std::chrono::steady_clock::now();
    for (auto p : pos) bs.set(p);
    auto t1 = std::chrono::steady_clock::now();
    for (auto p : pos) vb[p] = true;
    auto t2 = std::chrono::steady_clock::now();
    for (auto p : pos) vc[p] = 1;
    auto t3 = std::chrono::steady_clock::now();

    // (b) count x10
    long long c1 = 0, c2 = 0, c3 = 0;
    auto t4 = std::chrono::steady_clock::now();
    for (int r = 0; r < REP; ++r) c1 += static_cast<long long>(bs.count());
    auto t5 = std::chrono::steady_clock::now();
    for (int r = 0; r < REP; ++r) c2 += std::count(vb.begin(), vb.end(), true);
    auto t6 = std::chrono::steady_clock::now();
    for (int r = 0; r < REP; ++r) c3 += std::count(vc.begin(), vc.end(), char(1));
    auto t7 = std::chrono::steady_clock::now();

    g_esc = c1 + c2 + c3;
    std::cout << "set_bitset       " << ms(t0, t1) << " ms\n";
    std::cout << "set_vector_bool  " << ms(t1, t2) << " ms\n";
    std::cout << "set_vector_char  " << ms(t2, t3) << " ms\n";
    std::cout << "count_bitset_x10      " << ms(t4, t5) << " ms\n";
    std::cout << "count_vector_bool_x10 " << ms(t5, t6) << " ms\n";
    std::cout << "count_vector_char_x10 " << ms(t6, t7) << " ms\n";
    std::cout << "esc=" << g_esc << " (c1=" << c1 << " c2=" << c2 << " c3=" << c3 << ")\n";
    return 0;
}
