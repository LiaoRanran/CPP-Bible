#include <memory>
int main(){
  std::unique_ptr<int> p(new int(5));
  std::unique_ptr<int> q = std::move(p);
  (void)*p; // <<PLANTED-DEFECT>> 解引用已移动走的 p（可能为 nullptr）
  return 0;
}

