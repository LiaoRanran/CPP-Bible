// 676c 扩样-A: planted C++ defect candidate (generated sample)
// SPDX-License-Identifier: Apache-2.0
#include <cstdio>
int main() {
  int b[16] = {0};
  int v = b[18]; // <<PLANTED-DEFECT>> out-of-bounds: read stack index 18 (size 16)
  (void)v;
  return 0;
}
