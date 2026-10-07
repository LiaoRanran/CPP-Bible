// sample_B094
// [redacted]
// severity: low
// [redacted]
// expected_verdict: miss
// [redacted]
// (authoritative annotation in sample_B094.json)

#include <cstdio>
int main(){
  int i = 0;
  int a[3];
  a[i++] = i++ + i++; /* [redacted]*/
  std::printf("%d\n", a[0]);
  return 0;
}
