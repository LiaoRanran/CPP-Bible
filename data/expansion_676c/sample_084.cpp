// 676c 扩样-A: planted C++ defect candidate (generated sample)
// SPDX-License-Identifier: Apache-2.0
#include <cstdio>
int main() {
  int r = 1 << (-1); // <<PLANTED-DEFECT>> undefined behavior: negative shift exponent -1
  (void)r;
  return 0;
}
