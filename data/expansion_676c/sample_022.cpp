// 676c 扩样-A: planted C++ defect candidate (generated sample)
// SPDX-License-Identifier: Apache-2.0
#include <cstdio>
int main() {
  int* a = new int[8];
  int v = a[10]; // <<PLANTED-DEFECT>> heap buffer overflow: read 10 past size 8
  (void)v;
  delete[] a;
  return 0;
}
