#include <cstdio>
float g(float* pf, int* pi){ *pi = 1; return *pf; } // <<PLANTED-DEFECT>> 通过 int* 写后通过 float* 读（严格别名违例）
int main(){
  float x = 2.0f;
  int r = (int)g(&x, (int*)&x);
  printf("%d\n", r);
  return 0;
}

