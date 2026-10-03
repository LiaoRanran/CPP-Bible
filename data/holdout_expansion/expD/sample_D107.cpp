// 676c-D: planted C++ standard-library defect candidate (generated)
// SPDX-License-Identifier: Apache-2.0
#include <vector>
#include <algorithm>
#include <cstdio>
int main() {
  std::vector<int> v = {3, 1, 4, 1, 5, 9, 2, 6};
  std::sort(v.begin(), v.end(), [](int a, int b) { return (a % 2) < (b % 2); }); // <<PLANTED-DEFECT>> 比较器违反严格弱序(非传递,2)
  std::printf("%d\n", (int)v.size());
  return 0;
}
