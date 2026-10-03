// sample_B022
// defect_type: integer_overflow
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: ubsan
// (authoritative annotation in sample_B022.json)

#include <cstdio>
int main(){
  volatile int a = 46341;
  volatile int b = a * a; /*DEFECT: signed integer overflow (multiply) */
  std::printf("%d\n", (int)b);
  return 0;
}