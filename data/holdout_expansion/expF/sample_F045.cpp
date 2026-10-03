#include <cstdint>
#include <cstdio>
static uint32_t bswap32(uint32_t x){ return ((x>>24)&0xffu)|((x>>8)&0xff00u)|((x<<8)&0xff0000u)|((x<<24)&0xff000000u); }
int main(){
  uint32_t host = 0x0A0B0C0D;
  uint32_t wire = bswap32(bswap32(host));  // <<PLANTED-DEFECT>> 对已是主机序的值再次反转（双转换回原序）
  std::printf("%u\n", wire);
  return 0;
}
