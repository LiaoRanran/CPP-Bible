// 676c-D: planted C++ standard-library defect candidate (generated)
// SPDX-License-Identifier: Apache-2.0
#include <deque>
#include <cstdio>
int main() {
  std::deque<int> d = {1, 2, 3};
  int x = d[10]; // <<PLANTED-DEFECT>> deque operator[] 越界
  std::printf("%d\n", x);
  return 0;
}
