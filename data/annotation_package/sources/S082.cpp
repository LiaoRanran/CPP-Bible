// [redacted]
// SPDX-License-Identifier: Apache-2.0
#include <cstdio>
#include <cstring>
int main() {
  char dst[4];
  char src[9] = "abcdefgh";
  __builtin_memcpy(dst, src, 9); // [redacted]
  return 0;
}
