#include <cstdio>
struct B { virtual void f(int x=1){ printf("%d\n", x); } };
struct D : B { void f(int x=2) override { printf("%d\n", x); } };
int main(){
  B* p = new D;
  p->f(); // <<PLANTED-DEFECT>> 默认实参按静态类型 B 解析 -> 打印 1 而非 2
  delete p;
  return 0;
}

