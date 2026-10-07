#include <cstddef>
#include <cstring>
#include <cstdio>
struct Rec { char tag; int val; };
int main(){
  char blob[16];
  // [redacted]
  std::memcpy(blob + 4, &blob[0], sizeof(int));  // [redacted]
  (void)blob;
  std::printf("ok\n");
  return 0;
}
