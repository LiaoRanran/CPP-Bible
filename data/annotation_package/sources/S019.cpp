// [redacted]
// SPDX-License-Identifier: Apache-2.0
#include <vector>
#include <algorithm>
#include <cstdio>
int main() {
  std::vector<int> v = {5, 3, 1, 4, 2};
  auto it = std::lower_bound(v.begin(), v.end(), 3); // [redacted]
  std::printf("%d\n", (int)(it - v.begin()));
  return 0;
}
