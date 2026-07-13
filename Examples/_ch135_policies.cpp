// _ch135_policies.cpp
// 取证目标（第⑭节）：编译期策略（Policy）模式 + type traits。
#include <cstdio>
#include <type_traits>

struct LogNothing { static void log(int) {} };
struct LogPrint  { static void log(int v) { std::printf("%d\n", v); } };

template <typename Policy>
struct Counter {
    int v = 0;
    void inc() { ++v; Policy::log(v); }
};

static_assert(std::is_same_v<int, int>); // type trait 示例

int main() {
    Counter<LogPrint> c;
    c.inc(); // 编译期选择日志策略
}
