#include <csignal>
#include <signal.h>
#include <cstdio>
struct Pkt { int len; char buf[16]; };
static Pkt g;
extern "C" void isr(int) { g.len = 16; for (int i=0;i<16;++i) g.buf[i]=(char)i; }
int main(){
  std::signal(SIGINT, isr);
  std::raise(SIGINT);  // <<PLANTED-DEFECT>> 主程序读取 ISR 更新的非原子结构体
  std::printf("%d\n", g.len);
  return 0;
}
