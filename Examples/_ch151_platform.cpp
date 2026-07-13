// ⑮ 平台差异：sizeof / 对齐 / 指针宽度随平台变化 [平台]
// 见 Examples/_ch151_platform.cpp
#include <cstdio>
#include <cstddef>

struct Pad { char c; int i; double d; };
struct Packed { char c; int i; double d; } __attribute__((packed));

int main() {
    std::printf("platform: x86_64\n");
    std::printf("  sizeof(void*)=%zu  sizeof(long)=%zu  sizeof(size_t)=%zu\n",
                sizeof(void*), sizeof(long), sizeof(size_t));
    std::printf("  alignof(double)=%zu  sizeof(Pad)=%zu  sizeof(Packed)=%zu\n",
                alignof(double), sizeof(Pad), sizeof(Packed));
    std::printf("  note: 32-bit build 上 sizeof(void*)=4，指针型基准数字会不同\n");
    return 0;
}
