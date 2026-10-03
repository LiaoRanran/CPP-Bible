// 676c-D: planted C++ standard-library defect candidate (generated)
// SPDX-License-Identifier: Apache-2.0
#include <vector>
#include <cstdio>
struct Holder {
  std::vector<int> v = {1, 2, 3};
  int read_bad() {
    auto it = v.begin();
    v.push_back(4);
    return *it; // <<PLANTED-DEFECT>> 成员函数内 push_back 后使用失效迭代器
  }
};
int main() {
  Holder h;
  std::printf("%d\n", h.read_bad());
  return 0;
}
