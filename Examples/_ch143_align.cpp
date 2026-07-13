#include <cstddef>
#include <cstdio>

// ⑫ alignas 强制对齐：让对象落在缓存行/页边界，利于 SIMD 与避免 false sharing
struct Normal {
    char a;     // 1B
    int  b;     // 4B，需 4 对齐 -> 插入 3B padding
    short c;    // 2B
};

struct Aligned {
    alignas(64) char a;   // 强制 64B 对齐（与缓存行同宽）
    int  b;
    short c;
};

int main() {
    std::printf("Normal  : sizeof=%zu alignof=%zu\n", sizeof(Normal),  alignof(Normal));
    std::printf("Aligned : sizeof=%zu alignof=%zu\n", sizeof(Aligned), alignof(Aligned));
    return 0;
}
