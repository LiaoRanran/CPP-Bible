// 676c-D: planted C++ standard-library defect candidate (generated)
// SPDX-License-Identifier: Apache-2.0
#include <vector>
#include <cstdio>
int main() {
  std::vector<int> v;
  int x = v.back(); // <<PLANTED-DEFECT>> 空容器调用 back()
  std::printf("%d\n", x);
  return 0;
}
