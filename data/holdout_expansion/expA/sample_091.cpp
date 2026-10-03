// 676c 扩样-A: planted C++ defect candidate (generated sample)
// SPDX-License-Identifier: Apache-2.0
#include <cstdio>
#include <climits>
int main() {
  int m = INT_MIN;
  int r = -m; // <<PLANTED-DEFECT>> undefined behavior: negation of INT_MIN not representable
  (void)r;
  return 0;
}
