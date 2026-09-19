// D5 Wave 4 benchmark: ch116 完美转发 — push_back vs emplace_back 的诚实测量
// 编译: g++ -O2 -std=c++23 -o bench.exe _bench_d5_116_forwarding.cpp
// 设计要点(反炒作): 对可移动类型(string), push_back(临时) = 构造临时 + 一次 O(1) 移动,
//   emplace_back = 原位构造 — 差距只有"一次移动", 预期很小。emplace 真正的收益点:
//   (a) 避免只有拷贝构造的类型产生深拷贝; (b) 多参原位构造(如 pair)避免中间对象。
#include <iostream>
#include <chrono>
#include <vector>
#include <string>
#include <utility>
#include <cstdint>

static volatile long long g_esc = 0;

int main() {
    const int N = 5'000'000;
    const char* s64 = "0123456789012345678901234567890123456789012345678901234567890123"; // 64 字符, 超 SSO 必堆
    auto ms = [](auto a, auto b) { return std::chrono::duration<double, std::milli>(b - a).count(); };

    // 1) push_back(const char*) : 隐式构造临时 string + move
    auto t0 = std::chrono::steady_clock::now();
    { std::vector<std::string> v; v.reserve(N);
      for (int i = 0; i < N; ++i) v.push_back(s64);
      g_esc += static_cast<long long>(v.back().size()); }
    auto t1 = std::chrono::steady_clock::now();

    // 2) emplace_back(const char*) : 原位构造
    { std::vector<std::string> v; v.reserve(N);
      for (int i = 0; i < N; ++i) v.emplace_back(s64);
      g_esc += static_cast<long long>(v.back().size()); }
    auto t2 = std::chrono::steady_clock::now();

    // 3) push_back(lvalue string) : 深拷贝
    { std::string src(s64);
      std::vector<std::string> v; v.reserve(N);
      for (int i = 0; i < N; ++i) v.push_back(src);
      g_esc += static_cast<long long>(v.back().size()); }
    auto t3 = std::chrono::steady_clock::now();

    // 4) pair 场景: push_back(make_pair(...)) vs emplace_back(i, s64)
    { std::vector<std::pair<int, std::string>> v; v.reserve(N);
      for (int i = 0; i < N; ++i) v.push_back(std::make_pair(i, std::string(s64)));
      g_esc += static_cast<long long>(v.back().second.size()); }
    auto t4 = std::chrono::steady_clock::now();
    { std::vector<std::pair<int, std::string>> v; v.reserve(N);
      for (int i = 0; i < N; ++i) v.emplace_back(i, s64);
      g_esc += static_cast<long long>(v.back().second.size()); }
    auto t5 = std::chrono::steady_clock::now();

    std::cout << "push_back_cstr       " << ms(t0, t1) << " ms\n";
    std::cout << "emplace_back_cstr    " << ms(t1, t2) << " ms\n";
    std::cout << "push_back_lvalue     " << ms(t2, t3) << " ms\n";
    std::cout << "pair_push_make_pair  " << ms(t3, t4) << " ms\n";
    std::cout << "pair_emplace         " << ms(t4, t5) << " ms\n";
    std::cout << "esc=" << g_esc << "\n";
    return 0;
}
