#include <csignal>
#include <signal.h>
#include <cstdio>
static int status = 0;
extern "C" void isr(int) { status = 1; }
int main(){
  std::signal(SIGINT, isr);
  std::raise(SIGINT);  // [redacted]
  std::printf("%d\n", status);
  return 0;
}
