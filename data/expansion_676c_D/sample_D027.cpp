// 676c-D: planted C++ standard-library defect candidate (generated)
// SPDX-License-Identifier: Apache-2.0
#include <vector>
#include <cstdio>
int main() {
  std::vector<int> v = {1, 2, 3};
  for (int x : v) { (void)x; v.push_back(1); } // <<PLANTED-DEFECT>> range-for 内 push_back 使迭代器失效
  std::printf("%zu\n", v.size());
  return 0;
}
