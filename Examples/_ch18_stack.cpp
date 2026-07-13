// _ch18_stack.cpp —— 栈保护示例
// parse 含局部数组 buf，且地址被使用（-fstack-protector-strong 会保护）。
#include <cstddef>

int parse(const char* s, std::size_t n) {
    char buf[64];
    for (std::size_t i = 0; i < n && i < sizeof(buf); ++i)
        buf[i] = s[i];
    return static_cast<int>(buf[0]);
}
