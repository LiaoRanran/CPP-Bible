// sample_B077
// defect_type: type_punning
// severity: low
// planted: true
// expected_verdict: miss
// expected_detectors: ubsan
// (authoritative annotation in sample_B077.json)

#include <cstdio>
int main(){
  long L = 5;
  float* fp = (float*)&L; /*DEFECT: long->float strict-aliasing pun (UB); aligned, no trap */
  float x = *fp;
  std::printf("%f\n", x);
  return 0;
}