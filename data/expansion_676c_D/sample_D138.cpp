// 676c-D: planted C++ standard-library defect candidate (generated)
// SPDX-License-Identifier: Apache-2.0
#include <vector>
#include <algorithm>
#include <cstdio>
int main() {
  std::vector<int> v = {1, 2, 3, 2, 1};
  std::remove_if(v.begin(), v.end(), [](int x){ return x == 2; }); // <<PLANTED-DEFECT>> remove_if 后未 erase（补充）
  std::printf("%zu\n", v.size());
  return 0;
}
