// 676c-D: planted C++ standard-library defect candidate (generated)
// SPDX-License-Identifier: Apache-2.0
#include <vector>
#include <cstdio>
int main() {
  std::vector<int> v = {1, 2, 3};
  auto it = v.begin();
  for (int k = 0; k < 1; ++k) v.push_back(k);
  *it = 42; // <<PLANTED-DEFECT>> 使用重新分配后失效的迭代器
  std::printf("%d\n", *it);
  return 0;
}
