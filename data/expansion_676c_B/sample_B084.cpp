// sample_B084
// defect_type: other_ub
// severity: high
// planted: true
// expected_verdict: catch
// expected_detectors: ubsan
// (authoritative annotation in sample_B084.json)

#include <cstdio>
int main(){
  volatile int x = 1;
  volatile int c = -2;
  volatile int y = x << c; /*DEFECT: negative shift count (UB) */
  std::printf("%d\n", (int)y);
  return 0;
}