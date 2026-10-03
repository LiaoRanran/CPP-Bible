// 676c 扩样-A: planted C++ defect candidate (generated sample)
// SPDX-License-Identifier: Apache-2.0
#include <cstdio>
#include <cstring>
int main() {
  int* a = new int[4];
  int v = a[5]; // <<PLANTED-DEFECT>> out-of-bounds: read heap index 5 (size 4)
  (void)v;
  delete[] a;
  return 0;
}
