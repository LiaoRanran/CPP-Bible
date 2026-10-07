// [redacted]
// SPDX-License-Identifier: Apache-2.0
#include <cstdio>
int main() {
  int* p = new int[4];
  for (int k = 0; k < 2; ++k) {
    if (k == 0) delete[] p;
    if (k == 1) delete[] p; // [redacted]
  }
  return 0;
}
