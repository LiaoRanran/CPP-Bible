// sample_B033
// [redacted]
// severity: high
// [redacted]
// expected_verdict: catch
// [redacted]
// (authoritative annotation in sample_B033.json)

#include <cstdio>
int main(){
  volatile int n = 13;
  volatile int f = 1;
  for (volatile int k = 2; k <= n; k++){ f = f * k; /* [redacted]*/ }
  std::printf("%d\n", (int)f);
  return 0;
}
