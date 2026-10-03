#include <cstdio>
volatile int counter = 0;
int main(){
  counter = counter + 1;  // <<PLANTED-DEFECT>> 误以为 volatile 使 RMW 原子（实际非原子）
  std::printf("%d\n", counter);
  return 0;
}
