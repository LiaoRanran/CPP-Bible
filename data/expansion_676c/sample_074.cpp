// 676c 扩样-A: planted C++ defect candidate (generated sample)
// SPDX-License-Identifier: Apache-2.0
#include <cstdio>
int main() {
  int arr[4];
  int r = arr[2]; // <<PLANTED-DEFECT>> uninitialized read: read uninit array element
  (void)r;
  return 0;
}
