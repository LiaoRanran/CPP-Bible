// sample_B037
// defect_type: integer_overflow
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: ubsan
// (authoritative annotation in sample_B037.json)

#include <cstdio>
int main(){
  volatile int a = -100000;
  volatile int b = 100000;
  volatile int c = a * b; /*DEFECT: signed overflow (neg*pos large) */
  std::printf("%d\n", (int)c);
  return 0;
}