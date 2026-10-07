// sample_B069
// [redacted]
// severity: medium
// [redacted]
// expected_verdict: catch
// [redacted]
// (authoritative annotation in sample_B069.json)

#include <cstdio>
int main(){
  char buf[8] = {0};
  int* p = (int*)(buf + 1); /* [redacted]*/
  *p = *p + 1;
  std::printf("%d\n", *p);
  return 0;
}
