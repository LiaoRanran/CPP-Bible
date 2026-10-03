// sample_B099
// defect_type: other_ub
// severity: low
// planted: true
// expected_verdict: miss
// expected_detectors: ubsan
// (authoritative annotation in sample_B099.json)

#include <cstdio>
union U { int i; double d; };
int main(){
  U u; u.d = 3.14;
  int x = u.i; /*DEFECT: inactive union member read (UB); aligned, no runtime trap */
  std::printf("%d\n", x);
  return 0;
}