#include <cstdio>
int main(){
  volatile const int ro = 0;  // <<PLANTED-DEFECT>> volatile const 仅阻止编译器优化而非硬件写保护
  std::printf("%d\n", ro);
  return 0;
}
