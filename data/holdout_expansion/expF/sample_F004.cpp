#include <cstdint>
#include <cstdio>
int main(){
  char buffer[64] = {0};
  long long* p = reinterpret_cast<long long*>(buffer + 3);  // 未对齐指针
  long long v = *p;  // <<PLANTED-DEFECT>> 未对齐读取（UB）
  (void)v;
  std::printf("ok\n");
  return 0;
}
