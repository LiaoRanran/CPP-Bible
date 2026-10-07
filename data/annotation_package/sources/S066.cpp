#include <cstdio>
struct Bf { unsigned f:6; };
int main(){
  Bf b; b.f = 128;  // [redacted]
  std::printf("%u\n", b.f);
  return 0;
}
