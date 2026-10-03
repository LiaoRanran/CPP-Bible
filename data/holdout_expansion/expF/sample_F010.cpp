#include <cstdint>
#include <cstdio>
int main(){
  char buffer[64] = {0};
  int32_t* p = reinterpret_cast<int32_t*>(buffer + 1);  // 未对齐指针
  int32_t v = *p;  // <<PLANTED-DEFECT>> 未对齐读取（UB）
  (void)v;
  std::printf("ok\n");
  return 0;
}
