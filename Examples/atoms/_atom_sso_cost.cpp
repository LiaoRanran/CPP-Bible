// Examples/_atom_sso_cost.cpp
// 服务 ATOM-MEM-PERF-002：SSO vs 堆分配的操作代价（分配次数口径，非墙钟——墙钟不可复现，
// 沿 EV-MEM-008 先例把"性能差"量化为确定性的分配计数差）。
// 论断：短字符串（≤阈值）拷贝/赋值零分配（只搬对象内缓冲）；长字符串同样的操作每次都要
//       分配一次堆；短+短拼接一旦越阈，也立即落堆 1 次。
#include <string>
#include <iostream>
#include <new>
#include <cstdlib>

volatile long g_allocs = 0;
void* operator new(size_t n) { g_allocs = g_allocs + 1; return std::malloc(n); }
void operator delete(void* p) noexcept { std::free(p); }
void operator delete(void* p, size_t) noexcept { std::free(p); }

int main() {
    std::string sshort(10, 'a');    // 短：SSO 区内
    std::string slong(100, 'b');    // 长：堆上

    long a0 = g_allocs;
    { std::string c = sshort; }
    long short_copy = g_allocs - a0;

    a0 = g_allocs;
    { std::string c = slong; }
    long long_copy = g_allocs - a0;

    a0 = g_allocs;
    { std::string c; c = slong; }
    long long_assign = g_allocs - a0;

    a0 = g_allocs;
    { std::string c = sshort + sshort; }   // 10+10=20 字符 > 阈值 15 → 结果落堆
    long concat = g_allocs - a0;

    std::cout << "copy short(len=10): allocs=" << short_copy << "\n";
    std::cout << "copy long (len=100): allocs=" << long_copy << "\n";
    std::cout << "assign long: allocs=" << long_assign << "\n";
    std::cout << "concat 10+10=20chars: allocs=" << concat << "\n";
    return 0;
}
