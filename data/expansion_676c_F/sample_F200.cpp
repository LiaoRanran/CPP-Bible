#include <cstdio>
register int* gp asm("rbx");
int main(){
  static int x = 5; gp = &x;  // <<PLANTED-DEFECT>> 全局寄存器变量（GCC 扩展）误用 rbx
  std::printf("%d\n", *gp);
  return 0;
}
