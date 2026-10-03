// 676c-D: planted C++ standard-library defect candidate (generated)
// SPDX-License-Identifier: Apache-2.0
#include <unordered_map>
#include <cstdio>
int main() {
  std::unordered_map<int, int> m;
  m[1] = 10;
  auto it = m.find(1);
  for (int k = 2; k < 2 + 1 * 50; ++k) m[k] = k;
  std::printf("%d\n", it->second); // <<PLANTED-DEFECT>> rehash 后使用失效迭代器
  return 0;
}
