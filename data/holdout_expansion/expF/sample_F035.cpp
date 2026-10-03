#include <cstddef>
#include <cstdio>
struct alignas(8) Big { double a; };
int main(){
  char tiny[8];
  Big* p = reinterpret_cast<Big*>(tiny);  // <<PLANTED-DEFECT>> 缓冲区仅 8 字节且未必 8 对齐
  p->a = 2.0;
  std::printf("%f\n", p->a);
  return 0;
}
