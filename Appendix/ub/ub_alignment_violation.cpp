// UB-04 alignment violation：对不足对齐的地址做对齐类型解引用
// 编译: g++ -std=c++23 -O1 -g -fsanitize=address,undefined -fno-omit-frame-pointer -o align ub_alignment_violation.cpp
// 运行: ./align  →  UBSan 报 misaligned address（alignment-checker）
#include <cstdint>
#include <cstdio>

int main() {
    char buffer[8] = {0};
    // 故意取 buffer+1：int 需 4 字节对齐，buffer+1 仅 1 字节对齐 → 未定义行为
    void* mis = static_cast<void*>(buffer + 1);
    int* p = static_cast<int*>(mis);
    *p = 0xDEADBEEF;   // ❌ UB：对未对齐地址做 int 写
    std::printf("written via misaligned ptr\n");
    return 0;
}
