// 676c 扩样-A: planted C++ defect candidate (generated sample)
// SPDX-License-Identifier: Apache-2.0
#include <cstdio>
int main() {
  int b[4] = {0};
  int v = b[6]; // <<PLANTED-DEFECT>> out-of-bounds: read stack index 6 (size 4)
  (void)v;
  return 0;
}
