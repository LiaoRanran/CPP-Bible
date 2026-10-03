// sample_B081
// defect_type: other_ub
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: ubsan
// (authoritative annotation in sample_B081.json)

#include <cstdio>
int main(){
  volatile int b = 0;
  int c = 5 / b; /*DEFECT: division by zero (UB) */
  std::printf("%d\n", c);
  return 0;
}