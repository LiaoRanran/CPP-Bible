#include <cstdint>
#include <cstdio>
union Probe { uint32_t u; unsigned char b[4]; };
int main(){
  Probe p; p.u = 1;
  bool is_little = (p.b[0] == 1);  // <<PLANTED-DEFECT>> 用 union 双关读字节布局（严格别名 UB）
  std::printf("%d\n", (int)is_little);
  return 0;
}
