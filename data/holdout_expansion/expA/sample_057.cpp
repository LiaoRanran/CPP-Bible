// 676c 扩样-A: planted C++ defect candidate (generated sample)
// SPDX-License-Identifier: Apache-2.0
#include <cstdio>
int main() {
  int** pp = nullptr;
  (*pp)[0] = 1; // <<PLANTED-DEFECT>> null pointer dereference: double deref of null
  return 0;
}
