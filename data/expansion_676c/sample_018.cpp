// 676c 扩样-A: planted C++ defect candidate (generated sample)
// SPDX-License-Identifier: Apache-2.0
#include <cstdio>
int main() {
  int* a = new int[8];
  a[10] = 1; // <<PLANTED-DEFECT>> heap buffer overflow: write 10 past size 8
  delete[] a;
  return 0;
}
