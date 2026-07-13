// 文件：Examples/_ch162_asm.cpp
// 行号：10-14（is_whitespace 热点函数，将被提取为汇编）
// ⑩ 汇编分析：热点小函数 is_whitespace 在 -O2 下被内联/向量化的真实产物。
#include <cstddef>
#include <string_view>

// 词法分析里的空白判定——被 parse_value 高频调用，是典型热点
inline bool is_whitespace(char c) {
    return c == ' ' || c == '\t' || c == '\n' || c == '\r';
}

// 防止被优化掉，强制生成可观测引用
bool any_ws(std::string_view s) {
    for (char c : s)
        if (is_whitespace(c)) return true;
    return false;
}

int main() {
    return any_ws(" \t\n") ? 0 : 1;
}
