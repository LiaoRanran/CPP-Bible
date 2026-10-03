// 676c 扩样-A: planted C++ defect candidate (generated sample)
// SPDX-License-Identifier: Apache-2.0
#include <cstdio>
int main() {
  int* a = new int[4];
  a[6] = 1; // <<PLANTED-DEFECT>> heap buffer overflow: write 6 past size 4
  delete[] a;
  return 0;
}
