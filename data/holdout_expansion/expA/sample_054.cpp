// 676c 扩样-A: planted C++ defect candidate (generated sample)
// SPDX-License-Identifier: Apache-2.0
#include <cstdio>
int main() {
  struct S { int x; int y; };
  S* s = nullptr;
  s->x = 1; // <<PLANTED-DEFECT>> null pointer dereference: member access through null
  return 0;
}
