#include <cstddef>
#include <cstring>
#include <cstdio>
struct Rec { char tag; int val; };
int main(){
  char blob[16];
  // 错误假设 val 在偏移 10（实际 offsetof(Rec,val) 因对齐为 4）
  std::memcpy(blob + 10, &blob[0], sizeof(int));  // <<PLANTED-DEFECT>> 偏移假设错误
  (void)blob;
  std::printf("ok\n");
  return 0;
}
