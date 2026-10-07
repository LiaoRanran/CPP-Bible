#include <csignal>
#include <signal.h>
#include <cstdio>
extern "C" void isr(int) { static int n = 0; if (n++ < 1) std::raise(SIGINT); }
int main(){
  std::signal(SIGINT, isr);
  std::raise(SIGINT);  // [redacted]
  return 0;
}
