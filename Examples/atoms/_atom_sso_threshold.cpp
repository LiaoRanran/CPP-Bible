// Examples/_atom_sso_threshold.cpp
// 服务 ATOM-MEM-PERF-002：SSO 阈值实测（libstdc++ 15 字节）。
// 论断：std::string 短于阈值的字符串存对象内部缓冲，零堆分配；达到阈值才落堆。
// 方法：计数分配器（经模板在 exe 内实例化，观测通路必达）逐一测 len 0..24 的分配次数；
//       另用全局 operator new 计数对 std::string（默认 allocator）交叉验证（basic_string 是
//       模板、在 exe 内实例化，operator new 钩子可达；EV-MEM-028 的 DLL 假阴性只影响库内
//       非模板代码，不影响本夹具）。
#include <string>
#include <iostream>
#include <new>
#include <cstdlib>
#include <cstddef>

volatile long g_allocs = 0;
void* operator new(size_t n) { g_allocs = g_allocs + 1; return std::malloc(n); }
void operator delete(void* p) noexcept { std::free(p); }
void operator delete(void* p, size_t) noexcept { std::free(p); }

template <class T>
struct CountAlloc {
    using value_type = T;
    CountAlloc() = default;
    template <class U> CountAlloc(const CountAlloc<U>&) noexcept {}
    T* allocate(std::size_t n) {
        // 计数统一由 ::operator new 钩子承担（此处若再手动 +1 会双重计数）
        return static_cast<T*>(::operator new(n * sizeof(T)));
    }
    void deallocate(T* p, std::size_t) noexcept { ::operator delete(p); }
    template <class U> bool operator==(const CountAlloc<U>&) const noexcept { return true; }
    template <class U> bool operator!=(const CountAlloc<U>&) const noexcept { return false; }
};
using S = std::basic_string<char, std::char_traits<char>, CountAlloc<char>>;

std::size_t allocs_for(std::size_t len) {
    g_allocs = 0;
    { S s(len, 'x'); }                     // 构造 + 析构：分配次数可观测
    long c = g_allocs;
    return (std::size_t)c;
}

int main() {
    std::size_t first_heap = 0;
    for (std::size_t len = 0; len <= 24; ++len) {
        std::size_t a = allocs_for(len);
        if (a > 0 && first_heap == 0) first_heap = len;
        if (len == 0 || len == 14 || len == 15 || len == 16 || len == 22 || len == 23)
            std::cout << "len=" << len << " allocs=" << a << "\n";
    }
    std::cout << "sso: max_zero_alloc_len=" << (first_heap - 1)
              << " first_heap_len=" << first_heap << "\n";

    // 交叉验证：std::string（默认 allocator）经 operator new 钩子测阈值
    g_allocs = 0; { std::string t(15, 'x'); }
    long a15 = g_allocs;
    g_allocs = 0; { std::string t(16, 'x'); }
    long a16 = g_allocs;
    std::cout << "std-string: len=15 allocs=" << a15 << " len=16 allocs=" << a16 << "\n";
    return 0;
}
