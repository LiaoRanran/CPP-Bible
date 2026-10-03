#include <cstdint>
#include <cstdio>
int main(){
  char buffer[64] = {0};
  short* p = reinterpret_cast<short*>(buffer + 1);  // 未对齐指针
  short v = *p;  // <<PLANTED-DEFECT>> 未对齐读取（UB）
  (void)v;
  std::printf("ok\n");
  return 0;
}
