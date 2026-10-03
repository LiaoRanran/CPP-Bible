#include <cstdio>
int main(){
  register int r5 = 5;  // <<PLANTED-DEFECT>> register 关键字（C++17 弃用、C++20 移除）
  std::printf("%d\n", r5);
  return 0;
}
