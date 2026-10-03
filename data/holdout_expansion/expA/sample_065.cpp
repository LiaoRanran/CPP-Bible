// 676c 扩样-A: planted C++ defect candidate (generated sample)
// SPDX-License-Identifier: Apache-2.0
#include <cstdio>
int main() {
  int b;
  if (b > 100) { (void)1; } // <<PLANTED-DEFECT>> uninitialized read: compare uninit var
  return 0;
}
