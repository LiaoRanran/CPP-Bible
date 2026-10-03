// sample_B096
// defect_type: other_ub
// severity: low
// planted: true
// expected_verdict: miss
// expected_detectors: ubsan
// (authoritative annotation in sample_B096.json)

#include <cstdio>
int main(){
  int a[3] = {0};
  int i = 0;
  a[i] = i++ * 2; /*DEFECT: unsequenced: i used and modified in same full-expression (UB) */
  std::printf("%d\n", a[0]);
  return 0;
}