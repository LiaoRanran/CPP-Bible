#include <cstdio>
struct B { void f(){ printf("B\n"); } };
struct D : B { void f(int){ printf("D\n"); } }; // 名字隐藏（非 virtual）
int main(){
  D d;
  d.B::f(); // <<PLANTED-DEFECT>> 开发者误以为会调用 D 的 f，实则基类版本（隐藏导致歧义/误用）
  d.f(1);
  return 0;
}

