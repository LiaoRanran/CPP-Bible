// 676c 扩样-A: planted C++ defect candidate (generated sample)
// SPDX-License-Identifier: Apache-2.0
#include <cstdio>
int main() {
  int* p = new int[8];
  p[0] = 42;
  delete[] p;
  int v = p[0]; // <<PLANTED-DEFECT>> use-after-free: read freed heap slot
  (void)v;
  return 0;
}
