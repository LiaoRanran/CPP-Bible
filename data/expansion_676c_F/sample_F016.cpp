#include <cstdint>
#pragma pack(push, 1)
struct Packed {
  char c;
  int i;
};
#pragma pack(pop)
#include <cstdio>
int main(){
  Packed s;
  s.c = 1;
  s.i = 42;  // <<PLANTED-DEFECT>> 访问 packed 未对齐成员
  std::printf("%d\n", (int)s.c);
  return 0;
}
