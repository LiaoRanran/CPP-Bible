// _bench_d5_06_stringview.cpp — C++17 std::string_view：免拷贝分词 vs std::string::substr (GCC 13.1.0 MinGW)
// 复现旗标：g++ -O2 -std=c++20 -Wall -Wextra
#include <iostream>
#include <string>
#include <string_view>
#include <chrono>
#include <vector>
#include <algorithm>

volatile int64_t g_sink = 0;

static std::string make_hay(int words, int wlen) {
    std::string s;
    s.reserve(size_t(words) * (wlen + 1));
    for (int i = 0; i < words; ++i) {
        for (int j = 0; j < wlen; ++j) s += 'a';
        s += ' ';
    }
    return s;
}

__attribute__((noinline)) double bench_substr() {
    std::vector<double> t;
    const int R = 10;
    const int WORDS = 150'000, WLEN = 64;
    for (int r = 0; r < R; ++r) {
        std::string h = make_hay(WORDS, WLEN);
        auto a = std::chrono::steady_clock::now();
        size_t cnt = 0, pos = 0;
        while (true) {
            size_t sp = h.find(' ', pos);
            std::string tok = (sp == std::string::npos) ? h.substr(pos) : h.substr(pos, sp - pos);
            cnt += tok.size();
            if (sp == std::string::npos) break;
            pos = sp + 1;
        }
        auto b = std::chrono::steady_clock::now();
        g_sink += (int64_t)cnt;
        t.push_back(std::chrono::duration<double, std::milli>(b - a).count());
    }
    std::sort(t.begin(), t.end());
    return t[R / 2];
}

__attribute__((noinline)) double bench_sv() {
    std::vector<double> t;
    const int R = 10;
    const int WORDS = 150'000, WLEN = 64;
    for (int r = 0; r < R; ++r) {
        std::string h = make_hay(WORDS, WLEN);
        auto a = std::chrono::steady_clock::now();
        size_t cnt = 0, pos = 0;
        while (true) {
            size_t sp = h.find(' ', pos);
            size_t len = (sp == std::string::npos) ? h.size() - pos : sp - pos;
            std::string_view tok(h.data() + pos, len);   // 仅引用，无分配无拷贝
            cnt += tok.size();
            if (sp == std::string::npos) break;
            pos = sp + 1;
        }
        auto b = std::chrono::steady_clock::now();
        g_sink += (int64_t)cnt;
        t.push_back(std::chrono::duration<double, std::milli>(b - a).count());
    }
    std::sort(t.begin(), t.end());
    return t[R / 2];
}

int main() {
    double s = bench_substr();
    double v = bench_sv();
    std::cout << "substr (每次拷贝 token) : " << s << " ms\n";
    std::cout << "string_view (零拷贝引用) : " << v << " ms  (" << s / v << "x faster)\n";
    return 0;
}
