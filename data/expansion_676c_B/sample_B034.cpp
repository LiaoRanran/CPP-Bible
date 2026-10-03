// sample_B034
// defect_type: integer_overflow
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: ubsan
// (authoritative annotation in sample_B034.json)

#include <cstdio>
int main(){
  volatile int x = 2000000000;
  volatile int y = x * 2 + 3; /*DEFECT: signed overflow (combined) */
  std::printf("%d\n", (int)y);
  return 0;
}