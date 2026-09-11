// Examples/_atom_sso_size.cpp
// 服务 ATOM-MEM-PERF-002：本实现（libstdc++）的 sizeof(std::string) 与 SSO 容量实测。
// 论断：SSO 是实现内建（标准只保证语义，不要求 SSO）——libstdc++：sizeof=32、空串 capacity=15；
//       libc++/MSVC 数值不同（24/22 与 32/15，文档值，M2 边界），Clang 列由 CI 回填。
// 注意：static_assert 锚定的是 libstdc++ 实现细节（卡内 artifact_compiler 已声明归属）。
#include <string>
#include <iostream>
#include <new>
#include <cstdlib>

volatile long g_allocs = 0;
void* operator new(size_t n) { g_allocs = g_allocs + 1; return std::malloc(n); }
void operator delete(void* p) noexcept { std::free(p); }
void operator delete(void* p, size_t) noexcept { std::free(p); }

static_assert(sizeof(std::string) == 32,
              "libstdc++ layout: 32 bytes (union of SSO buffer and heap pointer)");

int main() {
    std::string s;
    std::size_t cap0 = s.capacity();

    g_allocs = 0; { std::string t(15, 'x'); }   // 恰好塞进 SSO 缓冲
    long a15 = g_allocs;
    g_allocs = 0; { std::string t(16, 'x'); }   // 超过 SSO → 落堆
    long a16 = g_allocs;

    std::cout << "sizeof(std::string)=" << sizeof(std::string) << "\n";
    std::cout << "empty capacity=" << cap0 << " (SSO buffer chars)\n";
    std::cout << "len=15 allocs=" << a15 << " len=16 allocs=" << a16 << "\n";
    return 0;
}
