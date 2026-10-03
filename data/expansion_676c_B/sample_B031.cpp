// sample_B031
// defect_type: integer_overflow
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: ubsan
// (authoritative annotation in sample_B031.json)

#include <cstdio>
int main(){
  volatile int sum = 0;
  volatile int x = 2000000000;
  sum = sum + x + x; /*DEFECT: signed overflow in summation */
  std::printf("%d\n", (int)sum);
  return 0;
}