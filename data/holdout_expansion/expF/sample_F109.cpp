#include <cstdio>
int main(){
  int x = 1;
  int y = x << -4;  // <<PLANTED-DEFECT>> 负移位量（UB）
  std::printf("%d\n", y);
  return 0;
}
