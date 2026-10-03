// 676c 扩样-A: planted C++ defect candidate (generated sample)
// SPDX-License-Identifier: Apache-2.0
#include <cstdio>
#include <cstring>
int main() {
  int* a = new int[16];
  int v = a[17]; // <<PLANTED-DEFECT>> out-of-bounds: read heap index 17 (size 16)
  (void)v;
  delete[] a;
  return 0;
}
