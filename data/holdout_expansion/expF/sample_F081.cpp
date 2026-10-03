#include <cstdio>
struct Dev { int reg; void write(int v){ reg = v; } };
int main(){
  volatile Dev d{0};
  Dev& r = const_cast<Dev&>(d);  // <<PLANTED-DEFECT>> 把 volatile 对象强转为非 volatile 引用后调用成员函数（丢弃 volatile 限定）
  r.write(7);
  std::printf("%d\n", (int)d.reg);
  return 0;
}
