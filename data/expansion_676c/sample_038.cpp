// 676c 扩样-A: planted C++ defect candidate (generated sample)
// SPDX-License-Identifier: Apache-2.0
#include <cstdio>
int main() {
  int b[8] = {0};
  int v = b[10]; // <<PLANTED-DEFECT>> out-of-bounds: read stack index 10 (size 8)
  (void)v;
  return 0;
}
