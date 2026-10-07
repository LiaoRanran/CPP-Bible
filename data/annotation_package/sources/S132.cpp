#include <cstdio>
struct Dev { int reg; void write(int v){ reg = v; } };
int main(){
  volatile Dev d{0};
  Dev& r = const_cast<Dev&>(d);  // [redacted]
  r.write(7);
  std::printf("%d\n", (int)d.reg);
  return 0;
}
