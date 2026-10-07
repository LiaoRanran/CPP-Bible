// [redacted]
// SPDX-License-Identifier: Apache-2.0
#include <unordered_map>
#include <cstdio>
int main() {
  std::unordered_map<int, int> m;
  m[1] = 10;
  auto it = m.find(1);
  for (int k = 2; k < 2 + 3 * 50; ++k) m[k] = k;
  std::printf("%d\n", it->second); // [redacted]
  return 0;
}
