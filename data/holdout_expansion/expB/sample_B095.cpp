// sample_B095
// defect_type: other_ub
// severity: low
// planted: true
// expected_verdict: miss
// expected_detectors: ubsan
// (authoritative annotation in sample_B095.json)

#include <cstdio>
int f(int x, int y){ return x + y; }
int main(){
  volatile int i = 0;
  int r = f(i++, i++); /*DEFECT: unsequenced function args (UB); no runtime trap */
  std::printf("%d\n", r);
  return 0;
}