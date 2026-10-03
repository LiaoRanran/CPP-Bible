// sample_B073
// defect_type: type_punning
// severity: low
// planted: true
// expected_verdict: miss
// expected_detectors: ubsan
// (authoritative annotation in sample_B073.json)

#include <cstdio>
int main(){
  int i = 0;
  float f = reinterpret_cast<float&>(i); /*DEFECT: reinterpret_cast type pun (UB), no runtime trap */
  std::printf("%f\n", f);
  return 0;
}