// 676c 扩样-A: planted C++ defect candidate (generated sample)
// SPDX-License-Identifier: Apache-2.0
#include <cstdio>
#include <cstring>
int main() {
  char dst[8];
  char src[13] = "abcdefghijkl";
  __builtin_memcpy(dst, src, 13); // <<PLANTED-DEFECT>> out-of-bounds: memcpy 13 bytes into 8-byte dst
  return 0;
}
