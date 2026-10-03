// 676c-D: planted C++ standard-library defect candidate (generated)
// SPDX-License-Identifier: Apache-2.0
#include <string>
#include <string_view>
#include <cstdio>
std::string_view leak() {
  std::string s = "local content";
  return std::string_view(s); // <<PLANTED-DEFECT>> 返回指向局部 string 的 string_view
}
int main() {
  auto sv = leak();
  std::printf("%.*s\n", (int)sv.size(), sv.data());
  return 0;
}
