// 676c-D: planted C++ standard-library defect candidate (generated)
// SPDX-License-Identifier: Apache-2.0
#include <memory>
#include <cstdio>
int main() {
  auto p = std::make_shared<int>(7);
  int* raw = p.get();
  delete raw; // <<PLANTED-DEFECT>> 手动 delete 智能指针管理的裸指针(1)
  std::printf("%d\n", *p);
  return 0;
}
