// 676c-D: planted C++ standard-library defect candidate (generated)
// SPDX-License-Identifier: Apache-2.0
#include <map>
#include <cstdio>
int main() {
  std::map<int, int> m;
  m[1] = 10; m[2] = 20; m[3] = 30;
  auto it = m.find(2);
  m.erase(it);
  std::printf("%d\n", it->second); // <<PLANTED-DEFECT>> 使用已被 erase 的迭代器(3)
  return 0;
}
