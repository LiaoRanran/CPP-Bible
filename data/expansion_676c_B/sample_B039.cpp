// sample_B039
// defect_type: integer_overflow
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: ubsan
// (authoritative annotation in sample_B039.json)

#include <cstdio>
int main(){
  volatile int x = 123456789;
  volatile int y = x * x; /*DEFECT: signed overflow (square) */
  std::printf("%d\n", (int)y);
  return 0;
}