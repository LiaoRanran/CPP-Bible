// 文件：Examples/_ch161_fix4.cpp
// 主题：⑤ 自定义 std::format formatter —— 为用户类型提供 {} 格式化
#include <cstdio>
#include <format>
#include <string>

struct Point { int x, y; };

template <>
struct std::formatter<Point> : std::formatter<std::string> {
    auto format(const Point& p, std::format_context& ctx) const {
        return std::formatter<std::string>::format(
            std::format("({}, {})", p.x, p.y), ctx);
    }
};

int main() {
    Point p{3, 4};
    std::string s = std::format("p={}", p);
    std::printf("%s\n", s.c_str());
    return 0;
}
