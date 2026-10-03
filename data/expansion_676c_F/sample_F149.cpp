#include <csignal>
#include <signal.h>
#include <cstdio>
extern "C" void isr(int) { std::printf("irq!\n"); }
int main(){
  std::signal(SIGINT, isr);
  std::raise(SIGINT);  // <<PLANTED-DEFECT>> 在 ISR 中调用非异步信号安全函数 printf
  return 0;
}
