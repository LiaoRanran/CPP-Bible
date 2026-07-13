// _ch14_ubsan.cpp — 故意有符号整数溢出（UBSan 取证）
#include <cstdio>

int main() {
    int x = 2147483647;       // INT_MAX
    x += 1;                   // 有符号溢出：未定义行为
    std::printf("%d\n", x);
    return 0;
}
