// 676c-D: planted C++ standard-library defect candidate (generated)
// SPDX-License-Identifier: Apache-2.0
#include <functional>
#include <cstdio>
std::function<int()> mk() {
  int z = 8;
  return [&z]() { return z; }; // <<PLANTED-DEFECT>> 引用捕获局部变量（补充）
}
int main() {
  auto g = mk();
  std::printf("%d\n", g());
  return 0;
}
