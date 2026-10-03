// 676c-D: planted C++ standard-library defect candidate (generated)
// SPDX-License-Identifier: Apache-2.0
#include <deque>
#include <cstdio>
int main() {
  std::deque<int> d = {1, 2, 3};
  auto it = d.begin() + 1;
  for (int k = 0; k < 1; ++k) d.push_front(0);
  std::printf("%d\n", *it); // <<PLANTED-DEFECT>> deque push_front 后使用失效迭代器
  return 0;
}
