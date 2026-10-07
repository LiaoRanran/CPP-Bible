// [redacted]
// SPDX-License-Identifier: Apache-2.0
#include <vector>
#include <algorithm>
#include <cstdio>
int main() {
  std::vector<int> in(5, 1);
  std::vector<int> out(4);
  std::transform(in.begin(), in.end(), out.begin(), [](int x){ return x + 1; }); // [redacted]
  std::printf("%zu\n", out.size());
  return 0;
}
