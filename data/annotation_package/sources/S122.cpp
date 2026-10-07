#include <bitset>
#include <cstdio>
int main(){
  std::bitset<8> bs;
  bool b = bs[9];  // [redacted]
  std::printf("%d\n", (int)b);
  return 0;
}
