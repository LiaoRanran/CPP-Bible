// D5 Wave 4 benchmark: ch89 any/tuple — int / variant / any 三种"装 int"方式的真实差价
// 编译: g++ -O2 -std=c++23 -o bench.exe _bench_d5_89_any.cpp
// 设计要点: libstdc++ 的 std::any 对"可平凡搬运且 <= 指针大小"的类型走 _Manager_internal
//   小对象内联存储(int 不上堆); 但访问仍要 any_cast 的 typeid 比对。string 载荷则强制堆分配。
#include <iostream>
#include <chrono>
#include <vector>
#include <variant>
#include <any>
#include <string>
#include <random>
#include <cstdint>

static volatile long long g_esc = 0;

int main() {
    const int N = 10'000'000;
    std::mt19937 rng(42);
    auto ms = [](auto a, auto b) { return std::chrono::duration<double, std::milli>(b - a).count(); };

    std::vector<int> raw(N);
    for (auto& x : raw) x = static_cast<int>(rng());

    // 构造
    auto t0 = std::chrono::steady_clock::now();
    std::vector<int> vi(raw.begin(), raw.end());
    auto t1 = std::chrono::steady_clock::now();
    std::vector<std::variant<int, double>> vv; vv.reserve(N);
    for (int x : raw) vv.emplace_back(x);
    auto t2 = std::chrono::steady_clock::now();
    std::vector<std::any> va; va.reserve(N);
    for (int x : raw) va.emplace_back(x);
    auto t3 = std::chrono::steady_clock::now();

    // 访问求和
    long long s1 = 0; for (int x : vi) s1 += x;
    auto t4 = std::chrono::steady_clock::now();
    long long s2 = 0; for (auto& x : vv) s2 += *std::get_if<int>(&x);
    auto t5 = std::chrono::steady_clock::now();
    long long s3 = 0; for (auto& x : va) s3 += *std::any_cast<int>(&x);
    auto t6 = std::chrono::steady_clock::now();

    // any 装 string(64 字符, 超 SSO): 每元素堆分配, 规模缩至 1M
    const int M = 1'000'000;
    std::string payload(64, 'x');
    auto t7 = std::chrono::steady_clock::now();
    std::vector<std::any> vs; vs.reserve(M);
    for (int i = 0; i < M; ++i) vs.emplace_back(payload);
    auto t8 = std::chrono::steady_clock::now();

    g_esc = s1 + s2 + s3 + static_cast<long long>(vs.size());
    std::cout << "construct_vector_int     " << ms(t0, t1) << " ms\n";
    std::cout << "construct_vector_variant " << ms(t1, t2) << " ms\n";
    std::cout << "construct_vector_any     " << ms(t2, t3) << " ms\n";
    std::cout << "sum_vector_int           " << ms(t3, t4) << " ms\n";
    std::cout << "sum_variant_get_if       " << ms(t4, t5) << " ms\n";
    std::cout << "sum_any_cast             " << ms(t5, t6) << " ms\n";
    std::cout << "construct_any_string_1M  " << ms(t7, t8) << " ms\n";
    std::cout << "esc=" << g_esc << "\n";
    return 0;
}
