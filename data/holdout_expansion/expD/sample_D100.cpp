// 676c-D: planted C++ standard-library defect candidate (generated)
// SPDX-License-Identifier: Apache-2.0
#include <string>
#include <string_view>
#include <cstdio>
int main() {
  std::string s = "zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz";
  std::string_view sv(s.data(), s.size());
  s.append("wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww");  // 必然触发 realloc，旧缓冲被释放
  unsigned long sum = 0;
  for (char ch : sv) sum += (unsigned char)ch; // <<PLANTED-DEFECT>> 遍历悬垂的 string_view（读取已释放缓冲）
  std::printf("%lu\n", sum);
  return 0;
}
