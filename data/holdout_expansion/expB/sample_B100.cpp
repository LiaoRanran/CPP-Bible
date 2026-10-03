// sample_B100
// defect_type: other_ub
// severity: low
// planted: true
// expected_verdict: miss
// expected_detectors: ubsan
// (authoritative annotation in sample_B100.json)

#include <cstdio>
int main(){
  int i = 0x3f800000;
  float f = *(float*)&i; /*DEFECT: strict-aliasing (UB); aligned, no runtime trap */
  std::printf("%f\n", f);
  return 0;
}