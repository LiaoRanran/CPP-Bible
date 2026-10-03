// 676c-D: planted C++ standard-library defect candidate (generated)
// SPDX-License-Identifier: Apache-2.0
#include <vector>
#include <cstdio>
int main() {
  std::vector<int> v = {1, 2, 3};
  auto e = v.end();
  v.insert(v.begin(), 1);
  std::printf("%d\n", (int)(v.end() == e)); // <<PLANTED-DEFECT>> 比较失效的 end() 迭代器
  return 0;
}
