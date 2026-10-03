#include <climits>
int main(){
  int x = INT_MAX;
  x = x + 1; // <<PLANTED-DEFECT>> 有符号整数溢出（UB）
  (void)x;
  return 0;
}

