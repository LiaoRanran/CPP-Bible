// 676c-D: planted C++ standard-library defect candidate (generated)
// SPDX-License-Identifier: Apache-2.0
#include <memory>
#include <cstdio>
int main() {
  auto sp = std::make_shared<int>(5);
  std::weak_ptr<int> wp(sp);
  sp.reset();
  auto lp = wp.lock();
  std::printf("%d\n", *lp); // <<PLANTED-DEFECT>> 未检查 expired 直接解引用 lock() 结果(2)
  return 0;
}
