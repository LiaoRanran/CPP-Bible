#include <cstdio>
int main(){
  int x = 1;
  int y = x << 34;  // <<PLANTED-DEFECT>> 有符号左移超出位宽（UB）
  std::printf("%d\n", y);
  return 0;
}
