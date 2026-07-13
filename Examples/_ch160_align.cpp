// 文件：Examples/_ch160_align.cpp
// 行号：1
// 对齐分配：alignas / alignof 与 std::align 的真实取证（MinGW GCC 13.1 -O2）
#include <cstddef>
#include <cstdio>
#include <cstring>
#include <memory>

struct alignas(64) CacheLinePadded {  // [经验] 缓存行对齐避免 false sharing
    int value;
    char pad[64 - sizeof(int)];
};

int main() {
    std::printf("alignof(int)            = %zu\n", alignof(int));
    std::printf("alignof(max_align_t)    = %zu\n", alignof(std::max_align_t));
    std::printf("alignof(CacheLinePadded)= %zu\n", alignof(CacheLinePadded));
    std::printf("sizeof(CacheLinePadded) = %zu\n", sizeof(CacheLinePadded));

    // std::align：在一段缓冲区中按 64 对齐取 n 字节
    constexpr size_t buf_size = 256;
    alignas(std::max_align_t) static unsigned char buf[buf_size];
    void* ptr = buf;
    size_t space = buf_size;                 // [实现] std::align 要求非 const 引用
    void* aligned = std::align(64, 32, ptr, space);
    std::printf("std::align -> %p (aligned64=%s)\n",
                aligned, ((reinterpret_cast<uintptr_t>(aligned) % 64) == 0) ? "yes" : "no");
    std::memset(aligned, 0, 32);
    return 0;
}
