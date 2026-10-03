// 676c-D: planted C++ standard-library defect candidate (generated)
// SPDX-License-Identifier: Apache-2.0
#include <functional>
#include <cstdio>
std::function<int()> make() {
  int x = 42;
  return [&x]() { return x + 1; }; // <<PLANTED-DEFECT>> 引用捕获局部变量，返回后悬垂(1)
}
int main() {
  auto f = make();
  std::printf("%d\n", f());
  return 0;
}
