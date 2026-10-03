// 676c 扩样-A: planted C++ defect candidate (generated sample)
// SPDX-License-Identifier: Apache-2.0
#include <cstdio>
int main() {
  int* p = new int[8];
  p[4] = 42;
  delete[] p;
  p[4] = 99; // <<PLANTED-DEFECT>> use-after-free: write freed heap slot
  return 0;
}
