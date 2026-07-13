// 文件：Examples/_ch161_antipattern.cpp
// 取证：g++ -std=c++20 -O2 真实编译运行（本机）；演示"热路径拼接字符串"反模式成本
#include <chrono>
#include <cstdio>
#include <sstream>
#include <string>

// ⑰ 反模式：在热路径用 std::ostringstream 拼接，即使该级别被关闭也会付出构建成本
std::string build_slow(int id, double v) {
    std::ostringstream os;
    os << "id=" << id << " val=" << v << " extra=" << (id * 2);
    return os.str();
}

int main() {
    const int N = 200'000;
    auto t0 = std::chrono::steady_clock::now();
    volatile std::size_t sink = 0;
    for (int i = 0; i < N; ++i) {
        // 即使日志级别关闭，字符串仍被构建（反模式）
        std::string s = build_slow(i, i * 1.5);
        sink += s.size();
    }
    auto t1 = std::chrono::steady_clock::now();
    double ms = std::chrono::duration<double, std::milli>(t1 - t0).count();
    std::printf("built %d strings in %.1f ms (sink=%zu)\n", N, ms, (std::size_t)sink);
    return 0;
}
