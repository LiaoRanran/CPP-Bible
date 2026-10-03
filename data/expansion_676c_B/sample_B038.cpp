// sample_B038
// defect_type: integer_overflow
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: ubsan
// (authoritative annotation in sample_B038.json)

#include <cstdio>
int main(){
  volatile int a = 2147483640;
  volatile int b = a - (-10); /*DEFECT: signed overflow in subtract (neg operand) */
  std::printf("%d\n", (int)b);
  return 0;
}