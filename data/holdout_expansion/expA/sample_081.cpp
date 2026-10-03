// 676c 扩样-A: planted C++ defect candidate (generated sample)
// SPDX-License-Identifier: Apache-2.0
#include <cstdio>
int main() {
  int r = 1 << 40; // <<PLANTED-DEFECT>> undefined behavior: shift exponent 40 too large for 32-bit int
  (void)r;
  return 0;
}
