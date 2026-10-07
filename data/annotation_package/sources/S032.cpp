// [redacted]
// SPDX-License-Identifier: Apache-2.0
#include <functional>
#include <cstdio>
std::function<int()> mk() {
  int z = 8;
  return [&z]() { return z; }; // [redacted]
}
int main() {
  auto g = mk();
  std::printf("%d\n", g());
  return 0;
}
