#include <utility>
struct Bx { int val; };
int main(){
  Bx a{1};
  a = std::move(a); // <<PLANTED-DEFECT>> 自移动（self-move）：对象移动给自身
  (void)a;
  return 0;
}

