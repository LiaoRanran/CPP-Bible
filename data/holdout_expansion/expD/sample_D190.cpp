// 676c-D: planted C++ standard-library defect candidate (generated)
// SPDX-License-Identifier: Apache-2.0
#include <functional>
#include <cstdio>
std::function<int()> mk() {
  int* p = new int(3);
  auto f = [p]() { return *p; }; // <<PLANTED-DEFECT>> 按值捕获指针，但指针所指对象稍后释放(3)
  delete p;
  return f;
}
int main() {
  auto g = mk();
  std::printf("%d\n", g());
  return 0;
}
