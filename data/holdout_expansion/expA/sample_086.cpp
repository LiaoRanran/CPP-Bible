// 676c 扩样-A: planted C++ defect candidate (generated sample)
// SPDX-License-Identifier: Apache-2.0
#include <cstdio>
int main() {
  int r = 1 << (-5); // <<PLANTED-DEFECT>> undefined behavior: negative shift exponent -5
  (void)r;
  return 0;
}
