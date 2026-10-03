// 676c-D: planted C++ standard-library defect candidate (generated)
// SPDX-License-Identifier: Apache-2.0
#include <memory>
#include <cstdio>
int main() {
  auto p = std::make_unique<int>(9);
  p.release(); // <<PLANTED-DEFECT>> release() 后未接管返回裸指针，内存泄漏
  std::printf("leaked\n");
  return 0;
}
