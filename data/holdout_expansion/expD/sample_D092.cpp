// 676c-D: planted C++ standard-library defect candidate (generated)
// SPDX-License-Identifier: Apache-2.0
#include <cstdio>
int main() {
  char* p = (char*)"hello";
  p[3] = 'X'; // <<PLANTED-DEFECT>> 修改字符串字面量（只读段）
  std::printf("%s\n", p);
  return 0;
}
