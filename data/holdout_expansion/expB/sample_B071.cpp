// sample_B071
// defect_type: type_punning
// severity: low
// planted: true
// expected_verdict: miss
// expected_detectors: ubsan
// (authoritative annotation in sample_B071.json)

#include <cstdio>
int main(){
  int i = 0x3f800000;
  float f = *(float*)&i; /*DEFECT: strict-aliasing punning (UB); UBSan cannot trap at -O0/-O2 */
  std::printf("%f\n", f);
  return 0;
}