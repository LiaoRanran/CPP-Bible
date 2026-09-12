// Examples/_atom_align_ctrl.cpp
// 服务 ATOM-MEM-ALIGN-001（第二卡）：alignas 提升对齐；按字节 memcpy 安全搬运结构体（避开对齐/类型双关 UB）。
// 反例（不运行）：用 reinterpret_cast 强转指针对齐/类型双关是 UB——只注释，留作证伪条件文本。
#include <iostream>
#include <cstddef>
#include <cstring>

struct Aligned { alignas(16) int x; };   // 整体对齐提升到 16
static_assert(alignof(Aligned) == 16, "alignas 控制对齐");

int main() {
    std::cout << "alignof(Aligned)=" << alignof(Aligned) << "\n";    // 16
    std::cout << "sizeof(Aligned)=" << sizeof(Aligned) << "\n";      // 16（int 4 + 12 padding）
    Aligned s; s.x = 7;
    unsigned char buf[sizeof(Aligned)];
    std::memcpy(buf, &s, sizeof(Aligned));   // 安全：按字节搬，不触发对齐/类型双关
    Aligned t;
    std::memcpy(&t, buf, sizeof(Aligned));
    std::cout << "memcpy roundtrip x=" << t.x << "\n";   // 7
    // 反例（UB，不运行）：int bad = *(int*)((char*)&s + 1);  // 未对齐地址 + 类型双关 => UB
    return 0;
}
