// 676c-D: planted C++ standard-library defect candidate (generated)
// SPDX-License-Identifier: Apache-2.0
#include <list>
#include <cstdio>
int main() {
  std::list<int> a = {1, 2, 3};
  auto it = a.begin();
  a.erase(a.begin());  // 节点被删除，it 悬垂
  std::printf("%d\n", *it); // <<PLANTED-DEFECT>> list erase 后使用已删除节点的迭代器
  return 0;
}
