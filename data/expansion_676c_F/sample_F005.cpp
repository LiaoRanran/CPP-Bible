#include <cstdint>
#include <cstdio>
int main(){
  char buffer[64] = {0};
  double* p = reinterpret_cast<double*>(buffer + 5);  // 未对齐指针
  double v = *p;  // <<PLANTED-DEFECT>> 未对齐读取（UB）
  (void)v;
  std::printf("ok\n");
  return 0;
}
