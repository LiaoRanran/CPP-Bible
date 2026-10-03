#include <map>
int main(){
  std::map<int,int> m{{1,2}};
  std::map<int,int> n = std::move(m);
  (void)m.empty(); // <<PLANTED-DEFECT>> 使用已移动对象 m
  return 0;
}

