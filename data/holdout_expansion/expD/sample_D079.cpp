// 676c-D: planted C++ standard-library defect candidate (generated)
// SPDX-License-Identifier: Apache-2.0
#include <string>
#include <cstdio>
int main() {
  std::string s(200, 'a');  // 堆分配
  char* p = s.data();
  p[380] = 'X'; // <<PLANTED-DEFECT>> 通过 data() 指针越界写（超出缓冲）
  std::printf("%zu\n", s.size());
  return 0;
}
