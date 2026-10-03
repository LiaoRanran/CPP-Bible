// 676c 扩样-A: planted C++ defect candidate (generated sample)
// SPDX-License-Identifier: Apache-2.0
#include <cstdio>
int main() {
  auto get = []() -> int* { return nullptr; };
  int* p = get();
  *p = 3; // <<PLANTED-DEFECT>> null pointer dereference: deref returned nullptr
  return 0;
}
