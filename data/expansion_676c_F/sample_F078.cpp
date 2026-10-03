#include <cstdio>
int main(){
  int x = 0;
  volatile int* vp = reinterpret_cast<volatile int*>(&x);  // <<PLANTED-DEFECT>> 把非 volatile 对象当 volatile 访问
  *vp = 5;
  std::printf("%d\n", x);
  return 0;
}
