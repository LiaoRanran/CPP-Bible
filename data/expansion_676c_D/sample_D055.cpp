// 676c-D: planted C++ standard-library defect candidate (generated)
// SPDX-License-Identifier: Apache-2.0
#include <optional>
#include <cstdio>
int main() {
  std::optional<int> o;
  int x = *o; // <<PLANTED-DEFECT>> 从空 optional 解引用
  std::printf("%d\n", x);
  return 0;
}
