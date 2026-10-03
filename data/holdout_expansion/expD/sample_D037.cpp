// 676c-D: planted C++ standard-library defect candidate (generated)
// SPDX-License-Identifier: Apache-2.0
#include <vector>
#include <cstdio>
int main() {
  std::vector<int> v;  // 空容器
  if (v.empty()) { int x = v.front(); // <<PLANTED-DEFECT>> 空容器调用 front()
    std::printf("%d\n", x); }
  return 0;
}
