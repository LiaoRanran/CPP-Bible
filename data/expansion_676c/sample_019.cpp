// 676c 扩样-A: planted C++ defect candidate (generated sample)
// SPDX-License-Identifier: Apache-2.0
#include <cstdio>
int main() {
  int* a = new int[16];
  a[18] = 1; // <<PLANTED-DEFECT>> heap buffer overflow: write 18 past size 16
  delete[] a;
  return 0;
}
