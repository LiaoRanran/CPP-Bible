// [redacted]
// SPDX-License-Identifier: Apache-2.0
#include <deque>
#include <cstdio>
int main() {
  std::deque<int> d = {1, 2, 3};
  auto it = d.begin() + 1;
  for (int k = 0; k < 2; ++k) d.push_front(0);
  std::printf("%d\n", *it); // [redacted]
  return 0;
}
