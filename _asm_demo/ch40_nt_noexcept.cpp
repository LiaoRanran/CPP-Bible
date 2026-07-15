// ASM-40-noexcept (noexcept 版本) : 预期消除 .gcc_except_table / 缩短 .eh_frame
// 编译: g++ -std=c++26 -O2 -c ch40_nt_noexcept.cpp -o ch40_nt_noexcept.o
// 段大小: objdump.exe -h ch40_nt_noexcept.o
// LSDA:   objdump.exe -s -j .gcc_except_table ch40_nt_noexcept.o
int no_throw(int a, int b) noexcept {
    return a / b;
}
int use_nt(int x, int y) { return no_throw(x, y); }
