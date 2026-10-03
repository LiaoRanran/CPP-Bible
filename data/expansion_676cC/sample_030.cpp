#include <utility>
struct S{int x;};
int main(){
  S a{1};
  auto f = [&](){ return std::move(a); }; // 捕获引用后移动
  S b = f();
  S c = f(); // <<PLANTED-DEFECT>> 对同一对象二次移动（通过 lambda 捕获）
  (void)b; (void)c;
  return 0;
}

