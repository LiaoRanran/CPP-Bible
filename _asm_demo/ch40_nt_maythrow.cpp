// ASM-40-noexcept (可能抛异常版本) : 对比基线
// 编译: g++ -std=c++26 -O2 -c ch40_nt_maythrow.cpp -o ch40_nt_maythrow.o
// 段大小: objdump.exe -h ch40_nt_maythrow.o
// LSDA:   objdump.exe -s -j .gcc_except_table ch40_nt_maythrow.o
int may_throw(int a, int b) {
    if (b == 0) throw 1;
    return a / b;
}
int use_mt(int x, int y) { return may_throw(x, y); }
