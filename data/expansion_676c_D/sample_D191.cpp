// 676c-D: planted C++ standard-library defect candidate (generated)
// SPDX-License-Identifier: Apache-2.0
#include <functional>
#include <cstdio>
int main() {
  std::function<int(int)> fact;
  fact = [fact](int n) { return n <= 1 ? 1 : n * fact(n - 1); }; // <<PLANTED-DEFECT>> 递归 lambda 按值捕获尚未初始化的自身
  try { std::printf("%d\n", fact(5)); } catch (const std::exception& e) { std::printf("threw\n"); }
  return 0;
}
