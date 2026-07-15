// C++23 <expected> — 真实可编译实证 (GCC 15.3.0, -std=c++26 -O2)
// 目的：验证 std::expected 的存储布局与返回值路径生成的指令。
#include <expected>
#include <cstdio>

std::expected<int, const char*> parse_digit(const char* s) {
    if (!s || !*s) return std::unexpected("empty");
    if (*s < '0' || *s > '9') return std::unexpected("not digit");
    return static_cast<int>(*s - '0');
}

int main() {
    auto r = parse_digit("7");
    std::printf("%d\n", r.has_value() ? r.value() : -1);
    return r.has_value() ? 0 : 1;
}
