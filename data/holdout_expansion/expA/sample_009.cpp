// 676c 扩样-A: planted C++ defect candidate (generated sample)
// SPDX-License-Identifier: Apache-2.0
#include <cstdio>
int main() {
  struct Rec { int a; double b; };
  Rec* r = new Rec{1, 2.0};
  delete r;
  r->a = 7; // <<PLANTED-DEFECT>> use-after-free: write through freed struct pointer
  (void)r;
  return 0;
}
