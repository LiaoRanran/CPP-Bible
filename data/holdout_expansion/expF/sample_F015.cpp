#include <cstdint>
#include <cstdio>
int main(){
  char buffer[64] = {0};
  double* p = reinterpret_cast<double*>(buffer + 1);  // 未对齐指针
  *p = static_cast<double>(0x1234);  // <<PLANTED-DEFECT>> 未对齐写入（UB）
  std::printf("ok\n");
  return 0;
}
