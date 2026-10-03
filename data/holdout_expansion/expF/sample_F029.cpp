#include <type_traits>
#include <cstdio>
struct Payload { double x; };
int main(){
  std::aligned_storage<32, 4> buf;  // align 仅 4，但 Payload 需 8
  Payload* p = reinterpret_cast<Payload*>(&buf);  // <<PLANTED-DEFECT>> 对齐不足
  p->x = 1.0;
  std::printf("%f\n", p->x);
  return 0;
}
