#include <cstdio>
int main(){
  int v = 7;
  int* p = &v;  // <<PLANTED-DEFECT>> 模拟“register 变量取地址”（强转制造别名误用）
  *p = 9;
  std::printf("%d\n", v);
  return 0;
}
