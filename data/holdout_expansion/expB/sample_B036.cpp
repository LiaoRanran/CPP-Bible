// sample_B036
// defect_type: integer_overflow
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: ubsan
// (authoritative annotation in sample_B036.json)

#include <cstdio>
int main(){
  volatile int a = 1500000000;
  volatile int b = 3;
  volatile int c = (a + b) * 2; /*DEFECT: signed overflow in parenthesized expr */
  std::printf("%d\n", (int)c);
  return 0;
}