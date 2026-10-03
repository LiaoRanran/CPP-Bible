// sample_B086
// defect_type: other_ub
// severity: high
// planted: true
// expected_verdict: miss
// expected_detectors: ubsan
// (authoritative annotation in sample_B086.json)

#include <cstdio>
int main(){
  volatile int x = 1;
  volatile int y = x << 31; /*DEFECT: left shift into sign bit (UB) */
  std::printf("%d\n", (int)y);
  return 0;
}