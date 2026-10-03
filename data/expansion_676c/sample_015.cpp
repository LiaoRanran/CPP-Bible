// 676c 扩样-A: planted C++ defect candidate (generated sample)
// SPDX-License-Identifier: Apache-2.0
#include <cstdio>
int main() {
  int* p = new int[4];
  bool again = true;
  delete[] p;
  if (again) {
    delete[] p; // <<PLANTED-DEFECT>> double-free inside branch
  }
  return 0;
}
