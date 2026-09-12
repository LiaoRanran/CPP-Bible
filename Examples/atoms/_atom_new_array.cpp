// Examples/_atom_new_array.cpp
// 服务 ATOM-MEM-NEW-001（第二卡）：new[]/delete[] 必须配对；nothrow 失败返回 nullptr 而非抛异常。
// new[] 调 operator new[]（一次）、delete[] 调 operator delete[]（一次）；内置类型数组不初始化。
#include <new>
#include <iostream>
#include <cstdlib>

volatile long g_a = 0, g_d = 0;                 // volatile：防折叠（M2 §5）
void* operator new[](std::size_t n) { g_a = g_a + 1; return std::malloc(n); }
void  operator delete[](void* p) noexcept { g_d = g_d + 1; std::free(p); }

int main() {
    int* a = new int[10];                        // 不初始化（内置类型；读取是 UB，故不读）
    std::cout << "array new[] calls=" << g_a << "\n";     // 1
    delete[] a;                                  // 必须 delete[]，不是 delete
    std::cout << "array delete[] calls=" << g_d << "\n";   // 1（配对）
    int* c = new (std::nothrow) int[100000000000LL];        // 约 400GB，必然失败
    std::cout << "nothrow huge returned null=" << (c == nullptr) << "\n";  // 1（不抛异常）
    if (c) delete[] c;
    return 0;
}
