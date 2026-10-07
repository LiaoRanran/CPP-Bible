// [redacted]
// SPDX-License-Identifier: Apache-2.0
#include <cstdio>
int main() {
  int* a = new int[4];
  int v = a[6]; // [redacted]
  (void)v;
  delete[] a;
  return 0;
}
