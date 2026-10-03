// 676c 扩样-A: planted C++ defect candidate (generated sample)
// SPDX-License-Identifier: Apache-2.0
#include <cstdio>
int main() {
  int a = 10;
  int r = a / 0; // <<PLANTED-DEFECT>> undefined behavior: integer division by zero
  (void)r;
  return 0;
}
