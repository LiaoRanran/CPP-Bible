// sample_B082
// defect_type: other_ub
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: ubsan
// (authoritative annotation in sample_B082.json)

#include <cstdio>
int main(){
  volatile int b = 0;
  int c = 5 % b; /*DEFECT: modulo by zero (UB) */
  std::printf("%d\n", c);
  return 0;
}