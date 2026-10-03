#include <cstdio>
struct Bf { unsigned f:5; };
int main(){
  Bf b; b.f = 64;  // <<PLANTED-DEFECT>> 写入超过 5 位位域宽度（截断/UB）
  std::printf("%u\n", b.f);
  return 0;
}
