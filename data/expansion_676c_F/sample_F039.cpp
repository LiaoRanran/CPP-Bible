#include <cstdint>
#include <cstdio>
int main(){
  unsigned char raw[8] = {0x12, 0x34, 0x56, 0x78, 0, 0, 0, 0};
  uint32_t net = *reinterpret_cast<uint32_t*>(raw);  // <<PLANTED-DEFECT>> 未调用 ntohl/ntohs
  std::printf("%u\n", static_cast<unsigned>(net));
  return 0;
}
