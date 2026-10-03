#include <cstdio>
int main(){
  unsigned m = (1 << 8) - 1;  // 本意取低 8 位
  unsigned v = 0xFF00; unsigned lo = v & m;  // <<PLANTED-DEFECT>> 掩码宽度/位置错误导致取错位
  std::printf("%u\n", lo);
  return 0;
}
