// 676c-D: planted C++ standard-library defect candidate (generated)
// SPDX-License-Identifier: Apache-2.0
#include <vector>
#include <algorithm>
#include <cstdio>
int main() {
  std::vector<int> a = {3, 1, 2}, b = {6, 4, 5}, out(6);
  std::merge(a.begin(), a.end(), b.begin(), b.end(), out.begin()); // <<PLANTED-DEFECT>> merge 输入区间未排序
  std::printf("%zu\n", out.size());
  return 0;
}
