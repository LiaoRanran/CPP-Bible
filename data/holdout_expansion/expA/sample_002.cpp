// 676c 扩样-A: planted C++ defect candidate (generated sample)
// SPDX-License-Identifier: Apache-2.0
#include <cstdio>
int main() {
  int* p = new int[8];
  p[3] = 42;
  delete[] p;
  int v = p[3]; // <<PLANTED-DEFECT>> use-after-free: read freed heap slot
  (void)v;
  return 0;
}
