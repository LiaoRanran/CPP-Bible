#include <cstdio>
volatile int flag = 0;
int main(){
  // 线程 A 置 flag=1；线程 B 轮询 flag（volatile 不保证原子/可见性）
  flag = 1;  // <<PLANTED-DEFECT>> 用 volatile 充当同步原语，应为 std::atomic
  while (flag != 0) { break; }
  std::printf("%d\n", flag);
  return 0;
}
