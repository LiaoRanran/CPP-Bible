// Examples/_atom_unique_size.cpp
// 服务 ATOM-MEM-UNIQUE-001：std::unique_ptr 是零开销抽象——sizeof 等于裸指针。
#include <memory>
#include <iostream>
#include <cstddef>

struct Big { long long a[4]; };          // 32 字节堆对象（与 PERF-001 的 Value32 同尺寸，便于对照）

int main() {
    std::cout << "sizeof(unique_ptr<Big>)=" << sizeof(std::unique_ptr<Big>) << "\n";
    std::cout << "sizeof(Big*)=" << sizeof(Big*) << "\n";
    std::cout << "equal=" << (sizeof(std::unique_ptr<Big>) == sizeof(Big*)) << "\n";
    return 0;
}
