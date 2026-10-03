#include <utility>
struct S{int x;};
int main(){
  S a{1}, b{2};
  b = std::move(a);
  a = std::move(b); // <<PLANTED-DEFECT>> 双移动：a、b 均处于已移动状态，逻辑混乱
  (void)a; (void)b;
  return 0;
}

