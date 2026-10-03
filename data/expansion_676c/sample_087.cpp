// 676c 扩样-A: planted C++ defect candidate (generated sample)
// SPDX-License-Identifier: Apache-2.0
#include <cstdio>
int main() {
  int x = 1;
  int r = x << 32; // <<PLANTED-DEFECT>> undefined behavior: shift by 32 equals width of int
  (void)r;
  return 0;
}
