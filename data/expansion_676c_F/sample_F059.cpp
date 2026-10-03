#include <cstdint>
#include <cstdio>
int main(){
  uint64_t v = 0x1122334455667788ULL;
  uint32_t lo = static_cast<uint32_t>(v);  // <<PLANTED-DEFECT>> 反序列化时只取低 32 位当完整值
  std::printf("%u\n", lo);
  return 0;
}
