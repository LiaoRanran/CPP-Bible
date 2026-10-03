#include <cstdio>
struct B { virtual void vf(){ printf("B\n"); } virtual ~B(){} };
struct D : B { void vf() override { printf("D\n"); } };
int main(){
  B* p = new D;
  delete p;          // 释放
  p->vf();           // <<PLANTED-DEFECT>> 释放后经基类指针调用虚函数（UAF）
  return 0;
}

