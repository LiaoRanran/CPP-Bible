// 676c-D: planted C++ standard-library defect candidate (generated)
// SPDX-License-Identifier: Apache-2.0
#include <memory>
#include <cstdio>
int main() {
  std::unique_ptr<int> p(new int[7]); // <<PLANTED-DEFECT>> 用默认 delete 管理数组（应为 delete[]）
  int* raw = p.get(); raw[0] = 1;
  std::printf("%d\n", raw[0]);
  return 0;
}
