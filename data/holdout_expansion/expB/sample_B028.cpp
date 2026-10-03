// sample_B028
// defect_type: integer_overflow
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: ubsan
// (authoritative annotation in sample_B028.json)

#include <cstdio>
int main(){
  volatile signed char c = 120;
  volatile signed char d = c + 20; /*DEFECT: signed char overflow */
  std::printf("%d\n", (int)d);
  return 0;
}