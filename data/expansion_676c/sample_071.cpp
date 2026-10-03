// 676c 扩样-A: planted C++ defect candidate (generated sample)
// SPDX-License-Identifier: Apache-2.0
#include <cstdio>
int main() {
  auto use = [](int v) { (void)v; };
  int t;
  use(t); // <<PLANTED-DEFECT>> uninitialized read: pass uninit var to function
  return 0;
}
