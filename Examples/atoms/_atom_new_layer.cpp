// Examples/_atom_new_layer.cpp
// 服务 ATOM-MEM-NEW-001：new/delete 是两层——new = operator new(分配) + 构造；delete = 析构 + operator delete(释放)。
// 用全局重载的计数 + 构造/析构标志把"两层"变成可观测输出。
#include <new>
#include <iostream>
#include <cstdlib>

volatile long g_alloc = 0, g_dealloc = 0;     // volatile：防折叠（M2 §5）
volatile int  g_ctor = 0, g_dtor = 0;
void* operator new(std::size_t n) { g_alloc = g_alloc + 1; return std::malloc(n); }
// -O2 优先调用"带尺寸的 delete"(operator delete(void*, size_t))，必须两者都重载才能观测到释放
void operator delete(void* p) noexcept { g_dealloc = g_dealloc + 1; std::free(p); }
void operator delete(void* p, std::size_t) noexcept { g_dealloc = g_dealloc + 1; std::free(p); }

struct Box { Box() { g_ctor = g_ctor + 1; } ~Box() { g_dtor = g_dtor + 1; } };

int main() {
    {
        Box* p = new Box();                        // 分配 + 构造
        asm volatile("" : : "r"(p) : "memory");    // 强制指针逃逸，阻止 new/delete 配对消除（allocation elision）
        std::cout << "after new: alloc=" << g_alloc << " ctor=" << g_ctor << "\n";   // 1, 1
        delete p;                                  // 析构 + 释放
        asm volatile("" : : "r"(p) : "memory");
        std::cout << "after delete: dealloc=" << g_dealloc << " dtor=" << g_dtor << "\n"; // 1, 1
    }
    return 0;
}
