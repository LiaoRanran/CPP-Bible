// 676c-D: planted C++ standard-library defect candidate (generated)
// SPDX-License-Identifier: Apache-2.0
#include <array>
#include <cstdio>
int main() {
  std::array<int, 3> a = {1, 2, 3};
  int x = a[6]; // <<PLANTED-DEFECT>> std::array 越界访问
  std::printf("%d\n", x);
  return 0;
}
