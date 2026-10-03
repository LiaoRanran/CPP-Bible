#include <cstdint>
#include <cstdio>
int main(){
  uint32_t x = 1u;
  uint32_t y = x << 35;  // <<PLANTED-DEFECT>> 无符号左移超出位宽（UB）
  std::printf("%u\n", y);
  return 0;
}
