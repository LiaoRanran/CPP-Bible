// C++20/23 <format> 自定义格式化器 — 真实可编译实证 (GCC 15.3.0, -std=c++26 -O2)
// 目的：验证 std::formatter 特化与 format_to 展开指令（std::print 在本 MinGW 构建
// 因 libstdc++ 未导出 __open_terminal 链接失败，故用 format 等价展示格式化机制）。
#include <format>
#include <cstdio>

struct Point { int x, y; };

template <>
struct std::formatter<Point> {
    constexpr auto parse(std::format_parse_context& ctx) { return ctx.begin(); }
    auto format(const Point& p, std::format_context& ctx) const {
        return std::format_to(ctx.out(), "({}, {})", p.x, p.y);
    }
};

int main() {
    auto s = std::format("p={}", Point{3, 4});
    std::printf("%s\n", s.c_str());
    return 0;
}
