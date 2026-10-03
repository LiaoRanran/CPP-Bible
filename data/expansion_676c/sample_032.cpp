// 676c 扩样-A: planted C++ defect candidate (generated sample)
// SPDX-License-Identifier: Apache-2.0
#include <cstdio>
#include <cstring>
int main() {
  int* a = new int[16];
  a[17] = 7; // <<PLANTED-DEFECT>> out-of-bounds: write heap index 17 (size 16)
  delete[] a;
  return 0;
}
