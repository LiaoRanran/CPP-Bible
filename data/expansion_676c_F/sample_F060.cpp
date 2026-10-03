#include <cstdint>
#include <cstdio>
struct Bits { unsigned a:4; unsigned b:4; unsigned c:8; unsigned d:16; };
int main(){
  Bits f; f.a=1; f.b=2; f.c=3; f.d=4;
  unsigned char* p = reinterpret_cast<unsigned char*>(&f);  // <<PLANTED-DEFECT>> 假设位域字节布局（端序/位序依赖实现）
  std::printf("%02X\n", p[0]);
  return 0;
}
