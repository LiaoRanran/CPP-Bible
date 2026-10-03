#include <cstdint>
#include <cstdio>
int main(){
  double d = 3.14159;
  uint64_t bits = *reinterpret_cast<uint64_t*>(&d);  // <<PLANTED-DEFECT>> 浮点位的端序未处理即跨网络发送
  std::printf("%llu\n", static_cast<unsigned long long>(bits));
  return 0;
}
