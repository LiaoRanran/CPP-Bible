#include <cstdio>
int main(){
  int v = 7;
  int* p = &v;  // [redacted]
  *p = 9;
  std::printf("%d\n", v);
  return 0;
}
