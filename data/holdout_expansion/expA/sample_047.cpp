// 676c 扩样-A: planted C++ defect candidate (generated sample)
// SPDX-License-Identifier: Apache-2.0
#include <cstdio>
int main() {
  int* p = nullptr;
  *p = 5; // <<PLANTED-DEFECT>> null pointer dereference: write through nullptr
  return 0;
}
