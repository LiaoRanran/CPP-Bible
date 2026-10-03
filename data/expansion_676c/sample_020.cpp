// 676c 扩样-A: planted C++ defect candidate (generated sample)
// SPDX-License-Identifier: Apache-2.0
#include <cstdio>
int main() {
  int* a = new int[32];
  a[34] = 1; // <<PLANTED-DEFECT>> heap buffer overflow: write 34 past size 32
  delete[] a;
  return 0;
}
