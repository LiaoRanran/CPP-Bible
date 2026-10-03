// 676c-D: planted C++ standard-library defect candidate (generated)
// SPDX-License-Identifier: Apache-2.0
#include <string>
#include <cstdio>
int main() {
  std::string s = "abc";
  std::string t = s.substr(5, 1); // <<PLANTED-DEFECT>> substr(pos>size) 抛 out_of_range
  std::printf("%s\n", t.c_str());
  return 0;
}
