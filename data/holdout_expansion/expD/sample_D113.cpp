// 676c-D: planted C++ standard-library defect candidate (generated)
// SPDX-License-Identifier: Apache-2.0
#include <vector>
#include <algorithm>
#include <cstdio>
int main() {
  std::vector<int> v = {1, 2, 3, 2, 1};
  std::remove(v.begin(), v.end(), 2); // <<PLANTED-DEFECT>> 忘记 erase（remove-erase 惯用法缺失,3）
  std::printf("%zu\n", v.size());  // 仍为 5，含残留元素
  return 0;
}
