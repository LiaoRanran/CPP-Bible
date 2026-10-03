// 676c 扩样-A: planted C++ defect candidate (generated sample)
// SPDX-License-Identifier: Apache-2.0
#include <cstdio>
#include <cstring>
int main() {
  int* a = new int[8];
  a[9] = 7; // <<PLANTED-DEFECT>> out-of-bounds: write heap index 9 (size 8)
  delete[] a;
  return 0;
}
