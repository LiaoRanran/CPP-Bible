// 676c 扩样-A: planted C++ defect candidate (generated sample)
// SPDX-License-Identifier: Apache-2.0
#include <cstdio>
int main() {
  int b[32] = {0};
  int v = b[34]; // <<PLANTED-DEFECT>> out-of-bounds: read stack index 34 (size 32)
  (void)v;
  return 0;
}
