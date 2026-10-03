// 676c-D: planted C++ standard-library defect candidate (generated)
// SPDX-License-Identifier: Apache-2.0
#include <vector>
#include <cstdio>
int main() {
  std::vector<bool> vb(3, false);
  auto bit = vb[1];  // 代理对象持有指向位字的指针
  for (int k = 0; k < 88; ++k) vb.push_back(true);  // 位数超过一机器字，必然重分配
  bool b = bit; // <<PLANTED-DEFECT>> vector<bool> 代理引用在重分配后悬垂
  std::printf("%d\n", (int)b);
  return 0;
}
