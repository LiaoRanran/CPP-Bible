// 676c-D: planted C++ standard-library defect candidate (generated)
// SPDX-License-Identifier: Apache-2.0
#include <functional>
#include <cstdio>
std::function<int()> mk() {
  int y = 5;
  auto f = [&]() { return y + 3; }; // <<PLANTED-DEFECT>> 默认引用捕获局部变量(3)
  return f;
}
int main() {
  auto g = mk();
  std::printf("%d\n", g());
  return 0;
}
