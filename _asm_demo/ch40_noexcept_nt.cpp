// ASM-40-noexcept : GCC 15.3.0 真机实证 —— noexcept 对异常处理表(.eh_frame / .gcc_except_table)体积的影响
// 两个翻译单元分别编译，对比异常处理元数据体积:
//   ch40_nt_maythrow.cpp : 可能抛异常
//   ch40_nt_noexcept.cpp : noexcept
// 编译: g++ -std=c++26 -O2 -c ch40_nt_*.cpp -o ch40_nt_*.o
// 段大小: objdump.exe -h ch40_nt_*.o
// LSDA 内容: objdump.exe -s -j .gcc_except_table ch40_nt_maythrow.o
