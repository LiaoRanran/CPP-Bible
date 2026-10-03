// 676c-D: planted C++ standard-library defect candidate (generated)
// SPDX-License-Identifier: Apache-2.0
#include <string>
#include <cstdio>
int main() {
  std::string s = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa";
  const char* p = s.c_str();
  s += " world";
  std::printf("%s\n", p); // <<PLANTED-DEFECT>> 修改后使用失效的 c_str() 指针
  return 0;
}
