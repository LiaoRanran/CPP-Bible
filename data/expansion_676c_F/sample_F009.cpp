#include <cstdint>
#include <cstdio>
int main(){
  char buffer[64] = {0};
  int* p = reinterpret_cast<int*>(buffer + 5);  // 未对齐指针
  *p = static_cast<int>(0x1234);  // <<PLANTED-DEFECT>> 未对齐写入（UB）
  std::printf("ok\n");
  return 0;
}
