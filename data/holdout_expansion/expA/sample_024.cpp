// 676c 扩样-A: planted C++ defect candidate (generated sample)
// SPDX-License-Identifier: Apache-2.0
#include <cstdio>
int main() {
  int b[4] = {0};
  int v = b[7]; // <<PLANTED-DEFECT>> stack buffer overflow: read 7 past size 4
  (void)v;
  return 0;
}
