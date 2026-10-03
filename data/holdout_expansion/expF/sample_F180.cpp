#include <cstdio>
int main(){
  register int r9 = 9;  // <<PLANTED-DEFECT>> register 关键字（C++17 弃用、C++20 移除）
  std::printf("%d\n", r9);
  return 0;
}
