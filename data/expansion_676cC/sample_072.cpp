#include <cstdio>
struct B { virtual void vf(){ printf("B\n"); } virtual ~B(){} };
struct D : B { void vf() override { printf("D\n"); } };
int main(){
  D d;
  B b = d; // <<PLANTED-DEFECT>> 对象切片：b 仅含 B 子对象
  b.vf();  // 输出 B 而非 D
  return 0;
}

