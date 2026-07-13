// 文件：Examples/_ch161_format_manual.cpp
// 取证：g++ -std=c++20 -O2 真实编译运行（本机）
// ④ fmt 风格手动格式化：编译期格式串 + 类型安全参数包（简化版示意）
#include <array>
#include <cstdio>
#include <string>

// 极简占位符替换：把 {} 依次替换为参数（演示 fmt 的核心思路）
template <typename... Args>
std::string fmt_manual(std::string_view pattern, Args&&... args) {
    std::array<std::string, sizeof...(Args)> parts{
        [](auto&& a) {
            if constexpr (std::is_same_v<std::decay_t<decltype(a)>, int>)
                return std::to_string(a);
            else if constexpr (std::is_same_v<std::decay_t<decltype(a)>, double>)
                return std::to_string(a);
            else
                return std::string(a);
        }(args)...
    };
    std::string out;
    std::size_t i = 0, pos = 0;
    while (pos < pattern.size()) {
        if (pattern[pos] == '{' && pos + 1 < pattern.size() && pattern[pos + 1] == '}') {
            if (i < parts.size()) out += parts[i++];
            pos += 2;
        } else {
            out += pattern[pos++];
        }
    }
    return out;
}

int main() {
    std::string s = fmt_manual("user {} logged in from {}", 42, "10.0.0.7");
    std::printf("%s\n", s.c_str());
    return 0;
}
