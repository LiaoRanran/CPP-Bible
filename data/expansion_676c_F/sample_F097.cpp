#include <cstdio>
int main(){
  volatile int cache = 42;  // <<PLANTED-DEFECT>> 对普通变量滥用 volatile（无 MMIO/信号场景）
  std::printf("%d\n", cache);
  return 0;
}
