// 676c-D: planted C++ standard-library defect candidate (generated)
// SPDX-License-Identifier: Apache-2.0
#include <string>
#include <string_view>
#include <cstdio>
int main() {
  std::string_view sv = std::string("temp2");
  std::printf("%.*s\n", (int)sv.size(), sv.data()); // <<PLANTED-DEFECT>> 使用悬垂的 string_view（临时串已析构）
  return 0;
}
