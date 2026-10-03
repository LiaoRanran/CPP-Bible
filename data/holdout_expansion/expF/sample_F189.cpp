#include <cstdio>
int main(){
  int a = 1, b = 2, r = 0;
  // 内联汇编修改了内存/寄存器却未声明 clobber，编译器可能错误优化
  asm volatile("addl %1, %0" : "+r"(r) : "r"(a));  // <<PLANTED-DEFECT>> 缺失 memory/寄存器 clobber 声明
  r += b;
  std::printf("%d\n", r);
  return 0;
}
