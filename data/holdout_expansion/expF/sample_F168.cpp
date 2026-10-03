#include <csignal>
#include <csetjmp>
#include <cstdio>
static jmp_buf env;
extern "C" void isr(int) { std::longjmp(env, 1); }
int main(){
  if (setjmp(env) == 0) { std::signal(SIGINT, isr); std::raise(SIGINT); }
  // <<PLANTED-DEFECT>> 在 ISR 中 longjmp（跳过主程序栈帧析构，UB）
  std::printf("returned\n");
  return 0;
}
