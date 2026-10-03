// 676c-D: planted C++ standard-library defect candidate (generated)
// SPDX-License-Identifier: Apache-2.0
#include <vector>
#include <cstdio>
int main() {
  std::vector<int> v(5, 1);
  auto it = v.begin() + 3;
  v.insert(v.begin(), 4);
  *it = 9; // <<PLANTED-DEFECT>> insert 后使用失效迭代器
  std::printf("%d\n", *it);
  return 0;
}
