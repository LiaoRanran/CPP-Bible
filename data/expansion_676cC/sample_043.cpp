#include <cstdio>
struct B { virtual void hi(){} ~B(){} }; // 非虚析构
struct D : B { ~D(){ printf("~D\n"); } };
int main(){
  B* p = new D;
  delete p; // <<PLANTED-DEFECT>> 经非虚析构基类指针删除派生 -> 仅 ~B，~D 不跑
  return 0;
}

