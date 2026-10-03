// sample_B023
// defect_type: integer_overflow
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: ubsan
// (authoritative annotation in sample_B023.json)

#include <cstdio>
int main(){
  volatile int a = -2147483640;
  volatile int b = a - 100; /*DEFECT: signed integer overflow (subtract) */
  std::printf("%d\n", (int)b);
  return 0;
}