#include <csignal>
#include <signal.h>
#include <cstdio>
static long total = 0;
extern "C" void isr(int) { for (int k = 0; k < 1000; ++k) total += k; }
int main(){
  std::signal(SIGINT, isr);
  std::raise(SIGINT);  // <<PLANTED-DEFECT>> 长 ISR 修改 total，主程序同时读
  std::printf("%ld\n", total);
  return 0;
}
