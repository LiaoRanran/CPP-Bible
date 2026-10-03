#include <cstdio>
int main(){
  register int r6 = 6;  // <<PLANTED-DEFECT>> register 关键字（C++17 弃用、C++20 移除）
  std::printf("%d\n", r6);
  return 0;
}
