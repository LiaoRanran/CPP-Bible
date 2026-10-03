#include <cstdint>
#include <cstdio>
int main(){
  char buffer[64] = {0};
  int16_t* p = reinterpret_cast<int16_t*>(buffer + 1);  // 未对齐指针
  *p = static_cast<int16_t>(0x1234);  // <<PLANTED-DEFECT>> 未对齐写入（UB）
  std::printf("ok\n");
  return 0;
}
