#include <cstdio>
struct B { virtual ~B(){ vf(); } virtual void vf(){ printf("B\n"); } };
struct D : B { void vf() override { printf("D\n"); } };
int main(){ D d; return 0; } // <<PLANTED-DEFECT>> 析构期间调用虚函数 -> 调用 B::vf

