#include <cstdio>
struct Bf { unsigned f:2; };
int main(){
  Bf b; b.f = 8;  // <<PLANTED-DEFECT>> 写入超过 2 位位域宽度（截断/UB）
  std::printf("%u\n", b.f);
  return 0;
}
