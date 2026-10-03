#include <cstdint>
#include <cstdio>
int main(){
  char buffer[64] = {0};
  float* p = reinterpret_cast<float*>(buffer + 2);  // 未对齐指针
  float v = *p;  // <<PLANTED-DEFECT>> 未对齐读取（UB）
  (void)v;
  std::printf("ok\n");
  return 0;
}
