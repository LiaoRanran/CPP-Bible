// 676c-D: planted C++ standard-library defect candidate (generated)
// SPDX-License-Identifier: Apache-2.0
#include <vector>
#include <algorithm>
#include <cstdio>
int main() {
  std::vector<int> v = {5, 3, 1, 4, 2};
  auto it = std::lower_bound(v.begin(), v.end(), 3); // <<PLANTED-DEFECT>> 在未排序区间使用 lower_bound(2)
  std::printf("%d\n", (int)(it - v.begin()));
  return 0;
}
