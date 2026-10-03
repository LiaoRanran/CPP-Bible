// 676c-D: planted C++ standard-library defect candidate (generated)
// SPDX-License-Identifier: Apache-2.0
#include <memory>
#include <cstdio>
int main() {
  int* raw = new int(42);
  std::shared_ptr<int> a(raw);
  std::shared_ptr<int> b(raw); // <<PLANTED-DEFECT>> 两个独立 shared_ptr 指向同一裸指针(1)
  std::printf("%d %d\n", *a, *b);
  return 0;
}
