// 676c 扩样-A: planted C++ defect candidate (generated sample)
// SPDX-License-Identifier: Apache-2.0
#include <cstdio>
#include <cstring>
int main() {
  int* a = new int[64];
  a[65] = 7; // <<PLANTED-DEFECT>> out-of-bounds: write heap index 65 (size 64)
  delete[] a;
  return 0;
}
