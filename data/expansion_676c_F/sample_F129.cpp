#include <cstdio>
enum Flags { A = 1, B = 2, C = 4 };
int main(){
  Flags f = static_cast<Flags>(A | C | 0x80000000u);  // <<PLANTED-DEFECT>> 枚举与无符号混合位或（底层类型不确定）
  std::printf("%d\n", (int)f);
  return 0;
}
