// 676c-D: planted C++ standard-library defect candidate (generated)
// SPDX-License-Identifier: Apache-2.0
#include <memory>
#include <cstdio>
int main() {
  int* raw = new int(1);
  std::shared_ptr<int> a(raw);
  std::shared_ptr<int> b(raw); // <<PLANTED-DEFECT>> 多 shared_ptr 共享裸指针（补充）
  std::printf("%d\n", *a);
  return 0;
}
