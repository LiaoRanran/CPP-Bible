// sample_B040
// defect_type: integer_overflow
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: ubsan
// (authoritative annotation in sample_B040.json)

#include <cstdio>
int main(){
  volatile int a = -2000000000;
  volatile int b = a - 1000000000; /*DEFECT: signed overflow in subtraction (negative side) */
  std::printf("%d\n", (int)b);
  return 0;
}