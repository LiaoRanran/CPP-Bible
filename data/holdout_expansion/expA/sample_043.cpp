// 676c 扩样-A: planted C++ defect candidate (generated sample)
// SPDX-License-Identifier: Apache-2.0
#include <cstdio>
int main() {
  int b[16] = {0};
  for (int i = 0; i <= 16; ++i) { b[i] = i; } // <<PLANTED-DEFECT>> out-of-bounds: loop writes index 16 (size 16)
  return 0;
}
