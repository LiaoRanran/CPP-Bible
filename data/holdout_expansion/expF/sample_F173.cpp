#include <cstdio>
int main(){
  register int r2 = 2;  // <<PLANTED-DEFECT>> register 关键字（C++17 弃用、C++20 移除）
  std::printf("%d\n", r2);
  return 0;
}
