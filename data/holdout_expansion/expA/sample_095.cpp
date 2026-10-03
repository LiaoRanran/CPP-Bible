// 676c 扩样-A: planted C++ defect candidate (generated sample)
// SPDX-License-Identifier: Apache-2.0
#include <cstdio>
int main() {
  bool b = true;
  unsigned char* p = reinterpret_cast<unsigned char*>(&b);
  *p = 2;  // corrupt bool storage
  bool c = b; // <<PLANTED-DEFECT>> undefined behavior: load of invalid bool value (2)
  (void)c;
  return 0;
}
