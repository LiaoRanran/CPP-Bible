// 676c 扩样-A: planted C++ defect candidate (generated sample)
// SPDX-License-Identifier: Apache-2.0
#include <cstdio>
#include <cstring>
int main() {
  int* a = new int[32];
  a[33] = 7; // <<PLANTED-DEFECT>> out-of-bounds: write heap index 33 (size 32)
  delete[] a;
  return 0;
}
