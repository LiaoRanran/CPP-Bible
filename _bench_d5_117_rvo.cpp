// D5 Wave 3 benchmark: ch117 RVO/NRVO 与拷贝消除 — 返回值到底拷贝了几次
// 编译: g++ -O2 -std=c++23 -o bench.exe _bench_d5_117_rvo.cpp
// 设计要点(修正版): NRVO 消除的是"局部对象 -> 返回槽"的那次拷贝, 不是构造本身;
//   若把三种返回形态都放在"每次迭代构造 1M 元素"的循环里, 构造成本会淹没一切差异.
//   因此本版用五个正交场景, 以"纯构造"与"纯深拷贝"为标尺:
//   construct_only        : 循环内直接构造 Big (基线, 代价 = 1M fill)
//   nrvo_return           : Big c = make_nrvo();       构造发生在函数内, NRVO -> 应 ≈ construct_only
//   move_return_movable   : return std::move(b) 且类型可移动 -> 构造 + O(1) 移动, 应 ≈ construct_only
//   copy_return_copyonly  : return std::move(b) 但类型只有拷贝构造(未声明移动) ->
//                           "std::move 反优化"经典陷阱: 静默退化为深拷贝, 应 ≈ 2x construct_only
//   pure_copy             : Big c = base; 纯深拷贝标尺 (1M 元素逐元素复制)
#include <iostream>
#include <chrono>
#include <vector>
#include <cstdint>
#include <utility>

static volatile long long g_esc = 0;

struct Big {                       // 可移动: 移动 = O(1) 指针交换
    std::vector<int> v;
    Big() : v(1'000'000, 7) {}
    Big(const Big&) = default;
    Big(Big&&) noexcept = default;
};

struct BigCopyOnly {               // 只声明拷贝构造 -> 移动构造不被隐式生成
    std::vector<int> v;
    BigCopyOnly() : v(1'000'000, 7) {}
    BigCopyOnly(const BigCopyOnly& o) : v(o.v) {}   // 深拷贝
    // 无移动构造: std::move(b) 在重载决议中落回 const& -> 深拷贝
};

Big         make_nrvo()        { Big b;         return b; }             // NRVO: 零拷贝
Big         make_move()        { Big b;         return std::move(b); }  // 禁 NRVO, O(1) 移动
BigCopyOnly make_move_copyonly(){ BigCopyOnly b; return std::move(b); } // 陷阱: 退化为深拷贝

int main() {
    const int N = 2'000;
    Big base;                      // pure_copy 的 long-lived 源

    auto ms = [](auto a, auto b) { return std::chrono::duration<double, std::milli>(b - a).count(); };

    auto t0 = std::chrono::steady_clock::now();
    int64_t s1 = 0;
    for (int i = 0; i < N; ++i) { Big b; s1 += b.v[i % 1000]; }
    auto t1 = std::chrono::steady_clock::now();

    int64_t s2 = 0;
    for (int i = 0; i < N; ++i) { Big c = make_nrvo(); s2 += c.v[i % 1000]; }
    auto t2 = std::chrono::steady_clock::now();

    int64_t s3 = 0;
    for (int i = 0; i < N; ++i) { Big c = make_move(); s3 += c.v[i % 1000]; }
    auto t3 = std::chrono::steady_clock::now();

    int64_t s4 = 0;
    for (int i = 0; i < N; ++i) { BigCopyOnly c = make_move_copyonly(); s4 += c.v[i % 1000]; }
    auto t4 = std::chrono::steady_clock::now();

    int64_t s5 = 0;
    for (int i = 0; i < N; ++i) { Big c = base; s5 += c.v[i % 1000]; }
    auto t5 = std::chrono::steady_clock::now();

    g_esc = s1 + s2 + s3 + s4 + s5;
    std::cout << "construct_only       " << ms(t0, t1) << " ms\n";
    std::cout << "nrvo_return          " << ms(t1, t2) << " ms\n";
    std::cout << "move_return_movable  " << ms(t2, t3) << " ms\n";
    std::cout << "copy_return_copyonly " << ms(t3, t4) << " ms\n";
    std::cout << "pure_copy            " << ms(t4, t5) << " ms\n";
    std::cout << "esc=" << g_esc << "\n";
    return 0;
}
