#include <cstdint>
#include <cstdio>
int main(){
  char buffer[64] = {0};
  int64_t* p = reinterpret_cast<int64_t*>(buffer + 7);  // 未对齐指针
  int64_t v = *p;  // [redacted]
  (void)v;
  std::printf("ok\n");
  return 0;
}
