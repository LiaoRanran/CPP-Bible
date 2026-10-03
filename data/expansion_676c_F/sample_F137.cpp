#include <bitset>
#include <cstdio>
int main(){
  std::bitset<8> bs;
  bool b = bs[10];  // <<PLANTED-DEFECT>> bitset<8> 越界下标 10（operator[] 无边界检查）
  std::printf("%d\n", (int)b);
  return 0;
}
