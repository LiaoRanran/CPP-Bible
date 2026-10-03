// 676c 扩样-A: planted C++ defect candidate (generated sample)
// SPDX-License-Identifier: Apache-2.0
#include <cstdio>
int main() {
  struct P { int a; int b; };
  P p;
  int r = p.a + p.b; // <<PLANTED-DEFECT>> uninitialized read: read uninit struct fields
  (void)r;
  return 0;
}
