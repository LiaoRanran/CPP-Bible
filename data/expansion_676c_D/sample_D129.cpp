// 676c-D: planted C++ standard-library defect candidate (generated)
// SPDX-License-Identifier: Apache-2.0
#include <vector>
#include <numeric>
#include <cstdio>
int main() {
  std::vector<double> v = {0.1, 0.2, 0.3};
  int sum = std::accumulate(v.begin(), v.end(), 0); // <<PLANTED-DEFECT>> 以 int 为初始值累加 double（截断,3）
  std::printf("%d\n", sum);  // 应为 0 而非 0.6
  return 0;
}
