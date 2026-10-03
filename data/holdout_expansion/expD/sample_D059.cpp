// 676c-D: planted C++ standard-library defect candidate (generated)
// SPDX-License-Identifier: Apache-2.0
#include <variant>
#include <cstdio>
int main() {
  std::variant<int, double> v = 3;
  double d = std::get<double>(v); // <<PLANTED-DEFECT>> 从持有 int 的 variant 取 double
  std::printf("%f\n", d);
  return 0;
}
