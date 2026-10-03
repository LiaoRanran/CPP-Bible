#include <vector>
int main(){
  std::vector<int> v{1,2,3};
  std::vector<int> w = std::move(v);
  (void)v.size(); // <<PLANTED-DEFECT>> 使用已移动对象 v（size() 结果未指定）
  return 0;
}

