// 676c-D: planted C++ standard-library defect candidate (generated)
// SPDX-License-Identifier: Apache-2.0
#include <memory>
#include <cstdio>
struct Node {
  std::shared_ptr<Node> next;
};
int main() {
  auto a = std::make_shared<Node>();
  auto b = std::make_shared<Node>();
  a->next = b; b->next = a; // <<PLANTED-DEFECT>> shared_ptr 循环引用导致泄漏(4)
  std::printf("leak\n");
  return 0;
}
