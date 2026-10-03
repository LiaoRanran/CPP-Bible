#include <utility>
struct Gg { int k; };
int main(){
  Gg a{1};
  a = std::move(a); // <<PLANTED-DEFECT>> 自移动（self-move）：对象移动给自身
  (void)a;
  return 0;
}

