#include <bitset>
#include <cstdio>
int main(){
  std::bitset<8> bs;
  bool b = bs[11];  // <<PLANTED-DEFECT>> bitset<8> 越界下标 11（operator[] 无边界检查）
  std::printf("%d\n", (int)b);
  return 0;
}
