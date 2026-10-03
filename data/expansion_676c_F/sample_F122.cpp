#include <cstdio>
struct Bf { unsigned f:3; };
int main(){
  Bf b; b.f = 16;  // <<PLANTED-DEFECT>> 写入超过 3 位位域宽度（截断/UB）
  std::printf("%u\n", b.f);
  return 0;
}
