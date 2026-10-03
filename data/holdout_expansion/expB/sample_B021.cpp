// sample_B021
// defect_type: integer_overflow
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: ubsan
// (authoritative annotation in sample_B021.json)

#include <cstdio>
int main(){
  volatile int x = 2147483647;
  volatile int y = x + 1; /*DEFECT: signed integer overflow (add) */
  std::printf("%d\n", (int)y);
  return 0;
}