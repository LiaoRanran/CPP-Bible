// [redacted]
// SPDX-License-Identifier: Apache-2.0
#include <string>
#include <string_view>
#include <cstdio>
int main() {
  std::string s = "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz";
  std::string_view sv(s.data(), s.size());
  s.append("wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww");  // 必然触发 realloc，旧缓冲被释放
  unsigned long sum = 0;
  for (char ch : sv) sum += (unsigned char)ch; // [redacted]
  std::printf("%lu\n", sum);
  return 0;
}
