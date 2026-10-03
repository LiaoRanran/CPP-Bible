// 676c-D: planted C++ standard-library defect candidate (generated)
// SPDX-License-Identifier: Apache-2.0
#include <vector>
#include <algorithm>
#include <cstdio>
int main() {
  std::vector<int> v = {1, 1, 2, 2, 3, 3};
  std::unique(v.begin(), v.end()); // <<PLANTED-DEFECT>> unique 后未 erase
  std::printf("%zu\n", v.size());
  return 0;
}
