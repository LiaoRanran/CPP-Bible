#include <cstdio>
int main(){
  volatile int mmio = 0;
  int* p = const_cast<int*>(reinterpret_cast<volatile int*>(&mmio));  // <<PLANTED-DEFECT>> 去掉 volatile 限定
  *p = 1;
  std::printf("%d\n", (int)mmio);
  return 0;
}
