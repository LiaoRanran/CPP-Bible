// C20 可编译 rdtsc：用 GCC 内联汇编实现（等价于 __rdtsc，无额外头文件）
#include <iostream>
#include <cstdint>
inline std::uint64_t rdtsc() {
    std::uint32_t lo = 0, hi = 0;
    asm volatile("rdtsc" : "=a"(lo), "=d"(hi));      // 读 TSC
    return (static_cast<std::uint64_t>(hi) << 32) | lo;
}
int main() {
    std::uint64_t a = rdtsc();
    volatile long long sink = 0; for (int i = 0; i < 100000; ++i) sink += i;
    std::uint64_t b = rdtsc();
    std::cout << "cost ~" << (b - a) << " cycles (sink=" << sink << ")\n";
    return 0;
}