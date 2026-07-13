// 文件：Examples/_ch162_utf8.cpp
// 行号：8-20（UTF-8 合法性校验函数）
// ⑫ UTF-8 处理：解析前应校验字节序列是合法 UTF-8（简化版 DFA）。
#include <cstdint>
#include <iostream>
#include <string>
#include <string_view>

// 返回 true 表示 s 是合法 UTF-8（覆盖 1/2/3/4 字节序列）
bool is_valid_utf8(std::string_view s) {
    size_t i = 0;
    while (i < s.size()) {
        unsigned char c = s[i];
        int extra = 0;
        if      (c < 0x80)       extra = 0;
        else if ((c & 0xE0) == 0xC0) extra = 1;
        else if ((c & 0xF0) == 0xE0) extra = 2;
        else if ((c & 0xF8) == 0xF0) extra = 3;
        else return false;                  // 非法首字节
        if (i + extra >= s.size()) return false;
        for (int k = 1; k <= extra; ++k)
            if ((s[i + k] & 0xC0) != 0x80) return false; // 续字节非法
        i += extra + 1;
    }
    return true;
}

int main() {
    std::string ok  = "\xe4\xb8\xad\xe6\x96\x87";      // "中文" 合法 UTF-8
    std::string bad = "\xe4\xb8";                       // 截断，非法
    std::cout << "合法序列 : " << is_valid_utf8(ok)  << "\n";
    std::cout << "截断序列 : " << is_valid_utf8(bad) << "\n";
    return 0;
}
