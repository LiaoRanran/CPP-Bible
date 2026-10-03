// sample_B076
// defect_type: type_punning
// severity: low
// planted: true
// expected_verdict: miss
// expected_detectors: ubsan
// (authoritative annotation in sample_B076.json)

#include <cstdio>
int main(){
  double d = 3.0;
  int* ip = (int*)&d; /*DEFECT: double->int strict-aliasing pun (UB); aligned, no trap */
  int x = *ip;
  std::printf("%d\n", x);
  return 0;
}