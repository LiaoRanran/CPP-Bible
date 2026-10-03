// 676c-D: planted C++ standard-library defect candidate (generated)
// SPDX-License-Identifier: Apache-2.0
#include <vector>
#include <cstdio>
int main() {
  std::vector<int> v = {1, 2, 3};
  int x = v[8]; // <<PLANTED-DEFECT>> operator[] 越界访问
  std::printf("%d\n", x);
  return 0;
}
