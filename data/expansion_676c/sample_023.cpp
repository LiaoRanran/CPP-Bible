// 676c 扩样-A: planted C++ defect candidate (generated sample)
// SPDX-License-Identifier: Apache-2.0
#include <cstdio>
int main() {
  int b[4] = {0};
  b[7] = 1; // <<PLANTED-DEFECT>> stack buffer overflow: write 7 past size 4
  return 0;
}
