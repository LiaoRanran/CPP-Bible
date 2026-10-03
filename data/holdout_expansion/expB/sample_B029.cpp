// sample_B029
// defect_type: integer_overflow
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: ubsan
// (authoritative annotation in sample_B029.json)

#include <cstdio>
int main(){
  volatile short s = 30000;
  volatile short t = s * 2; /*DEFECT: short overflow */
  std::printf("%d\n", (int)t);
  return 0;
}