#include <cstdio>
int main(){
  register int r4 = 4;  // <<PLANTED-DEFECT>> register 关键字（C++17 弃用、C++20 移除）
  std::printf("%d\n", r4);
  return 0;
}
