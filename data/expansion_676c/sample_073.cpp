// 676c 扩样-A: planted C++ defect candidate (generated sample)
// SPDX-License-Identifier: Apache-2.0
#include <cstdio>
int main() {
  bool flag;
  if (flag) { (void)0; } // <<PLANTED-DEFECT>> uninitialized read: branch on uninit bool
  return 0;
}
