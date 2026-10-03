// 676c 扩样-A: planted C++ defect candidate (generated sample)
// SPDX-License-Identifier: Apache-2.0
#include <cstdio>
int main() {
  int* p = new int[4];
  delete[] p;
  delete[] p; // <<PLANTED-DEFECT>> double-free: same pointer released twice
  return 0;
}
