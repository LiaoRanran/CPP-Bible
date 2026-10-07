// sample_B036
// [redacted]
// severity: high
// [redacted]
// expected_verdict: catch
// [redacted]
// (authoritative annotation in sample_B036.json)

#include <cstdio>
int main(){
  volatile int a = 1500000000;
  volatile int b = 3;
  volatile int c = (a + b) * 2; /* [redacted]*/
  std::printf("%d\n", (int)c);
  return 0;
}
