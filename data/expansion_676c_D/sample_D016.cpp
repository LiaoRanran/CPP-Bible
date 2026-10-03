// 676c-D: planted C++ standard-library defect candidate (generated)
// SPDX-License-Identifier: Apache-2.0
#include <vector>
#include <cstdio>
int main() {
  std::vector<int> v = {10, 20, 30, 40};
  auto it = v.begin() + 4;
  v.erase(v.begin());
  std::printf("%d\n", *it); // <<PLANTED-DEFECT>> erase 后使用失效迭代器(无 realloc)
  return 0;
}
