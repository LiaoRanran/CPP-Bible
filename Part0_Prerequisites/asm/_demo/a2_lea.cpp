// a2_lea.cpp — A2 有效地址计算（lea 的真正用途）
// 编译: g++ -std=c++23 -O2 -c -o a2_lea.o a2_lea.cpp
// 反汇编: objdump -d -M intel a2_lea.o
char* g(char* base, long i) {
    return base + i * 4 + 8;   // 期望 lea rax,[rdi+rcx*4+8]
}
