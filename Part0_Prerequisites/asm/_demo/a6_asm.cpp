// a6_asm.cpp — A6 内联汇编演示（仅保留干净、可验证的例子）
// rdtsc 读 CPU 时间戳计数器：x86 专属，结果 64 位落在 edx:eax，约束 "=A"
// 编译运行: g++ -std=c++23 -O2 a6_asm.cpp -o a6_asm.exe && ./a6_asm.exe
// 反汇编: objdump -d -M intel a6_asm.o
#include <cstdint>
#include <cstdio>

uint64_t rdtsc() {
    uint64_t t;
    __asm__ __volatile__ ("rdtsc" : "=A"(t));
    return t;
}

int main() {
    uint64_t a = rdtsc();
    int sink = 0;
    for (int i = 0; i < 1000; ++i) sink += i;   // 一段无意义工作（防止被优化掉）
    uint64_t b = rdtsc();
    printf("rdtsc: 前=%llu 后=%llu 增量=%llu (sink=%d)\n",
           (unsigned long long)a, (unsigned long long)b,
           (unsigned long long)(b - a), sink);
    return 0;
}
