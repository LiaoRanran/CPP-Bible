#include <cstdio>
struct Bf { unsigned f:6; };
int main(){
  Bf b; b.f = 128;  // <<PLANTED-DEFECT>> 写入超过 6 位位域宽度（截断/UB）
  std::printf("%u\n", b.f);
  return 0;
}
