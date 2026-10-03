// 676c 扩样-A: planted C++ defect candidate (generated sample)
// SPDX-License-Identifier: Apache-2.0
#include <cstdio>
int main() {
  int* p = new int[4];
  for (int k = 0; k < 2; ++k) {
    if (k == 0) delete[] p;
    if (k == 1) delete[] p; // <<PLANTED-DEFECT>> double-free at loop iteration 1
  }
  return 0;
}
