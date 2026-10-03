// 676c 扩样-A: planted C++ defect candidate (generated sample)
// SPDX-License-Identifier: Apache-2.0
#include <cstdio>
int main() {
  int b[8] = {0};
  for (int i = 0; i <= 8; ++i) { b[i] = i; } // <<PLANTED-DEFECT>> out-of-bounds: loop writes index 8 (size 8)
  return 0;
}
