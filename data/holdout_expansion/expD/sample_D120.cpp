// 676c-D: planted C++ standard-library defect candidate (generated)
// SPDX-License-Identifier: Apache-2.0
#include <algorithm>
#include <cstdio>
int main() {
  int a[6] = {1, 2, 3, 4, 5, 6};
  std::copy(a, a + 3, a + 4); // <<PLANTED-DEFECT>> 源与目标区间重叠
  std::printf("%d\n", a[5]);
  return 0;
}
