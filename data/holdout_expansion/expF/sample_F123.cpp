#include <cstdio>
struct Bf { unsigned f:4; };
int main(){
  Bf b; b.f = 32;  // <<PLANTED-DEFECT>> 写入超过 4 位位域宽度（截断/UB）
  std::printf("%u\n", b.f);
  return 0;
}
