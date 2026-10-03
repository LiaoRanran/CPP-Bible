// 676c-D: planted C++ standard-library defect candidate (generated)
// SPDX-License-Identifier: Apache-2.0
#include <functional>
#include <memory>
#include <cstdio>
struct Widget {
  int v = 7;
  std::function<int()> bind() { return [this]() { return v; }; } // <<PLANTED-DEFECT>> 捕获 this(2)
};
int main() {
  std::function<int()> f;
  { auto w = std::make_unique<Widget>(); f = w->bind(); }
  std::printf("%d\n", f());
  return 0;
}
