#include <cstdio>
int main(){
  register int r1 = 1;  // <<PLANTED-DEFECT>> register 关键字（C++17 弃用、C++20 移除）
  std::printf("%d\n", r1);
  return 0;
}
