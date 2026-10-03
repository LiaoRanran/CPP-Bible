#include <cstdint>
#include <cstdio>
int main(){
  unsigned char raw[8] = {0xAA, 0xBB, 0xCC, 0xDD, 0xEE, 0xFF, 0, 0};
  uint16_t v = *reinterpret_cast<uint16_t*>(raw + 1);  // <<PLANTED-DEFECT>> 偏移1的未对齐 + 端序混合误读
  std::printf("%llu\n", static_cast<unsigned long long>(v));
  return 0;
}
