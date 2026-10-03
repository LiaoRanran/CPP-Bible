// 676c-D: planted C++ standard-library defect candidate (generated)
// SPDX-License-Identifier: Apache-2.0
#include <cstdio>
int main() {
  int x = 1;
  auto f = [=]() mutable { x = 99; }; // <<PLANTED-DEFECT>> 按值捕获后修改副本(2)
  f();
  std::printf("%d\n", x);  // 仍为 1
  return 0;
}
