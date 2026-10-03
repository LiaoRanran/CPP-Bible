// 676c 扩样-A: planted C++ defect candidate (generated sample)
// SPDX-License-Identifier: Apache-2.0
#include <cstdio>
int main() {
  int r = 1 << 55; // <<PLANTED-DEFECT>> undefined behavior: shift exponent 55 too large for 32-bit int
  (void)r;
  return 0;
}
