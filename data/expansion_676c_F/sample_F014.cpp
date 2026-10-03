#include <cstdint>
#include <cstdio>
int main(){
  char buffer[64] = {0};
  short* p = reinterpret_cast<short*>(buffer + 3);  // 未对齐指针
  *p = static_cast<short>(0x1234);  // <<PLANTED-DEFECT>> 未对齐写入（UB）
  std::printf("ok\n");
  return 0;
}
