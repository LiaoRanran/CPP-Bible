// Examples/_atom_align_pad.cpp
// 服务 ATOM-MEM-ALIGN-001：结构体成员按自身对齐要求排列，编译器插入 padding，sizeof 含 padding。
// 证伪"成员紧密排列、无填充"。
#include <iostream>
#include <cstddef>

struct Padded { char a; int b; };     // a 对齐 1、b 对齐 4 => b 前插 3 字节 padding

int main() {
    std::cout << "sizeof(Padded)=" << sizeof(Padded) << "\n";                       // 8
    std::cout << "offsetof a=" << offsetof(Padded, a) << "\n";                       // 0
    std::cout << "offsetof b=" << offsetof(Padded, b) << "\n";                       // 4（中间 3 字节 padding）
    std::cout << "padding bytes=" << (sizeof(Padded) - sizeof(char) - sizeof(int)) << "\n";  // 3
    return 0;
}
