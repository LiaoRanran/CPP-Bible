// sample_B033
// defect_type: integer_overflow
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: ubsan
// (authoritative annotation in sample_B033.json)

#include <cstdio>
int main(){
  volatile int n = 13;
  volatile int f = 1;
  for (volatile int k = 2; k <= n; k++){ f = f * k; /*DEFECT: factorial overflow */ }
  std::printf("%d\n", (int)f);
  return 0;
}