#include <csignal>
#include <signal.h>
#include <cstdio>
static int shared = 0;
extern "C" void isr(int) { shared++; }
int main(){
  std::signal(SIGINT, isr);
  std::raise(SIGINT);  // <<PLANTED-DEFECT>> ISR 与主程序竞争自增 shared（无同步）
  std::printf("%d\n", shared);
  return 0;
}
