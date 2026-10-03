// 676c 扩样-A: planted C++ defect candidate (generated sample)
// SPDX-License-Identifier: Apache-2.0
#include <cstdio>
int main() {
  int z;
  int r = z + 7; // <<PLANTED-DEFECT>> uninitialized read: arithmetic on uninit var
  (void)r;
  return 0;
}
