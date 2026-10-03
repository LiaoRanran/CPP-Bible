#include <string>
int main(){
  std::string s = "hello";
  std::string t = std::move(s);
  if (s.empty()) { (void)0; } // <<PLANTED-DEFECT>> 使用已移动对象 s（有效但处于未指定状态）
  return 0;
}

