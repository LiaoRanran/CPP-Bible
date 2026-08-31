#include <string>
#include <vector>
#include <utility>
#include <chrono>
#include <cassert>
#include <iostream>

int main() {
    // 探测本实现 SSO 容量（运行期打印，非 assert 固定值）
    std::cout << "SSO capacity (string().capacity()) = "
              << std::string().capacity() << std::endl;

    const int N = 200'000;            // 构造 2M / 10，CI 秒级
    volatile long sink = 0;

    auto build = [](int len) {
        std::string s;
        s.reserve(len);
        for (int i = 0; i < len; ++i) s.push_back(char('a' + (i % 26)));
        return s;
    };

    // 构造对照：SSO 上限 vs 首个堆分配
    auto t0 = std::chrono::steady_clock::now();
    for (int i = 0; i < N; ++i) { auto s = build(15); sink += s.size(); }
    auto t1 = std::chrono::steady_clock::now();
    for (int i = 0; i < N; ++i) { auto s = build(16); sink += s.size(); }
    auto t2 = std::chrono::steady_clock::now();
    std::cout << "build len15 ms = "
              << std::chrono::duration<double, std::milli>(t1 - t0).count()
              << std::endl;
    std::cout << "build len16 ms = "
              << std::chrono::duration<double, std::milli>(t2 - t1).count()
              << std::endl;

    // 拷贝对照
    const int M = 100'000;
    std::vector<std::string> src15(M, std::string(15, 'x'));
    std::vector<std::string> src16(M, std::string(16, 'x'));
    std::vector<std::string> dst15, dst16;
    dst15.reserve(M); dst16.reserve(M);
    auto t3 = std::chrono::steady_clock::now();
    for (auto& s : src15) dst15.push_back(s);
    auto t4 = std::chrono::steady_clock::now();
    for (auto& s : src16) dst16.push_back(s);
    auto t5 = std::chrono::steady_clock::now();
    assert(dst15.size() == M && dst16.size() == M);
    std::cout << "copy len15 ms = "
              << std::chrono::duration<double, std::milli>(t4 - t3).count()
              << std::endl;
    std::cout << "copy len16 ms = "
              << std::chrono::duration<double, std::milli>(t5 - t4).count()
              << std::endl;

    // 移动对照
    std::vector<std::string> m15(M, std::string(15, 'x'));
    std::vector<std::string> m64(M, std::string(64, 'x'));
    std::vector<std::string> o15, o64;
    o15.reserve(M); o64.reserve(M);
    auto t6 = std::chrono::steady_clock::now();
    for (auto& s : m15) o15.push_back(std::move(s));
    auto t7 = std::chrono::steady_clock::now();
    for (auto& s : m64) o64.push_back(std::move(s));
    auto t8 = std::chrono::steady_clock::now();
    assert(o15.size() == M && o64.size() == M);
    std::cout << "move len15 ms = "
              << std::chrono::duration<double, std::milli>(t7 - t6).count()
              << std::endl;
    std::cout << "move len64 ms = "
              << std::chrono::duration<double, std::milli>(t8 - t7).count()
              << std::endl;
    (void)sink;
    return 0;
}