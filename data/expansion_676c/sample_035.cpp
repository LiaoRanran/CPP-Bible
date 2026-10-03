// 676c 扩样-A: planted C++ defect candidate (generated sample)
// SPDX-License-Identifier: Apache-2.0
#include <cstdio>
#include <cstring>
int main() {
  char dst[4];
  char src[9] = "abcdefgh";
  __builtin_memcpy(dst, src, 9); // <<PLANTED-DEFECT>> out-of-bounds: memcpy 9 bytes into 4-byte dst
  return 0;
}
